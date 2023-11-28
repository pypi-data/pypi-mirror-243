"""The module responsible for operating tgcf in live mode."""

import logging
import re
import sys
from typing import Union
import asyncio

from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.custom.message import Message

from test_tele import config, const
from test_tele import storage as st
from test_tele.bot import get_events
from test_tele.config import CONFIG, get_SESSION
from test_tele.plugins import apply_plugins
from test_tele.utils import clean_session_files, send_message


async def new_message_handler(event: Union[Message, events.Album, events.NewMessage]) -> None:
    """Process new incoming messages."""
    chat_id = event.chat_id

    if chat_id not in config.from_to:
        return
    
    if event.grouped_id != None:
        logging.info(f"Album tetep kedetesi sebagai new message {chat_id}")
        return

    logging.info(f"New message received in {chat_id}")
    message = event.message

    event_uid = st.EventUid(event)

    length = len(st.stored)
    exceeding = length - const.KEEP_LAST_MANY

    if exceeding > 0:
        for key in st.stored:
            del st.stored[key]
            break

    dest = config.from_to.get(chat_id)
    rpl = config.reply_to[chat_id]

    tm = await apply_plugins(message)
    if not tm:
        return

    if event.is_reply:
        r_event = st.DummyEvent(chat_id, event.reply_to_msg_id)
        r_event_uid = st.EventUid(r_event)
        
    st.stored[event_uid] = {}
    for i, d in enumerate(dest):
        if event.is_reply and r_event_uid in st.stored:
            tm.reply_to = st.stored.get(r_event_uid).get(d)
        if rpl and rpl[i] != 0 and not event.is_reply:
            tm.reply_to = rpl[i]
        fwded_msg = await send_message(d, tm)
        st.stored[event_uid].update({d: fwded_msg})

        # if CONFIG.plugins.special.check and CONFIG.plugins.special.download:
        #     link_regex = re.compile(r"https?://\S+")
        #     link = re.findall(link_regex, tm.text)
        #     if link:
        #         tm.reply_to = st.stored.get(event_uid).get(d)
        #         tm.text = link[0]
        #         await start_download(d, tm)
    tm.clear()


async def edited_message_handler(event) -> None:
    """Handle message edits."""
    message = event.message

    chat_id = event.chat_id

    if chat_id not in config.from_to:
        return

    logging.info(f"Message edited in {chat_id}")

    event_uid = st.EventUid(event)

    tm = await apply_plugins(message)

    if not tm:
        return

    fwded_msgs = st.stored.get(event_uid)

    if fwded_msgs:
        for _, msg in fwded_msgs.items():
            if config.CONFIG.live.delete_on_edit == message.text:
                await msg.delete()
                await message.delete()
            else:
                await msg.edit(tm.text)
        return

    dest = config.from_to.get(chat_id)
    rpl = config.reply_to[chat_id]

    for i, d in enumerate(dest):
        if rpl and rpl[i] != 0:
            tm.reply_to = rpl[i]
        await send_message(d, tm)
    tm.clear()


async def deleted_message_handler(event):
    """Handle message deletes."""
    chat_id = event.chat_id
    if chat_id not in config.from_to:
        return

    logging.info(f"Message deleted in {chat_id}")

    event_uid = st.EventUid(event)
    fwded_msgs = st.stored.get(event_uid)
    if fwded_msgs:
        for _, msg in fwded_msgs.items():
            await msg.delete()
        return


ALL_EVENTS = {
    "new": (new_message_handler, events.NewMessage()),
    "edited": (edited_message_handler, events.MessageEdited()),
    "deleted": (deleted_message_handler, events.MessageDeleted()),
}


## ================================================ Pyrogram

import os

from dotenv import load_dotenv
from test_tele.bot.gelbooru import inline_gelbooru, callback

load_dotenv()

from pyrogram import Client
from pyrogram.types import InlineQuery

session_string_user = StringSession(CONFIG.login.SESSION_STRING)
api_id = CONFIG.login.API_ID
api_hash = CONFIG.login.API_HASH
bot_token = CONFIG.login.BOT_TOKEN


async def run_pyrogram(): 
    app = Client("my_account", api_id=api_id, api_hash=api_hash, in_memory=True, bot_token=bot_token)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    @app.on_inline_query()
    async def gelbooru_inline_handler(client, inline_query: InlineQuery):
        """Handle inline query for gelbooru search"""
        await inline_gelbooru(client, inline_query)

    @app.on_callback_query()
    async def callback_query_handler(client, callback_query):
        """Get callback query from inline keyboard"""
        image_file = await callback(client, callback_query)
        await client.send_document(callback_query.from_user.id, image_file)


    await app.start()

## Test


async def start_sync() -> None:
    """Start tgcf live sync."""
    # clear past session files
    clean_session_files()

    USER_SESSION = StringSession(CONFIG.login.SESSION_STRING) # tambahan ku
    # SESSION = get_SESSION()
    client = TelegramClient( 
        USER_SESSION,
        CONFIG.login.API_ID,
        CONFIG.login.API_HASH,
        sequential_updates=CONFIG.live.sequential_updates,
    )
    bot_client = TelegramClient( # tambahan ku
        'tgcf_bot',
        CONFIG.login.API_ID,
        CONFIG.login.API_HASH,
        sequential_updates=CONFIG.live.sequential_updates,
    )
    
    if CONFIG.login.user_type == 0: # bot
        if CONFIG.login.BOT_TOKEN == "":
            logging.warning("Bot token not found, but login type is set to bot.")
            sys.exit()
        await bot_client.start(bot_token=CONFIG.login.BOT_TOKEN) # edit variable
    else:
        await client.start()
        await bot_client.start(bot_token=CONFIG.login.BOT_TOKEN) # tambahan ku

    config.is_bot = await bot_client.is_bot()
    logging.info(f"config.is_bot={config.is_bot}")

    await config.load_admins(bot_client)

    if CONFIG.login.user_type == 1: # user
        command_events = get_events(1)
        ALL_EVENTS.update(command_events)
        for key, val in ALL_EVENTS.items():
            if config.CONFIG.live.delete_sync is False and key == "deleted":
                continue
            client.add_event_handler(*val)

    # tambahan ku
    command_events = get_events(0)
    ALL_EVENTS.update(command_events)
    for key, val in ALL_EVENTS.items():
        if config.CONFIG.live.delete_sync is False and key == "deleted":
            continue
        bot_client.add_event_handler(*val)
        logging.info(f"Added event handler for {key}")

    if const.REGISTER_COMMANDS: # config.is_bot and
        await bot_client( # edit variable
            functions.bots.SetBotCommandsRequest(
                scope=types.BotCommandScopeDefault(),
                lang_code="en",
                commands=[
                    types.BotCommand(command=key, description=value)
                    for key, value in const.COMMANDS.items()
                ],
            )
        )
    config.from_to, config.reply_to = await config.load_from_to(client, config.CONFIG.forwards)

    if CONFIG.login.user_type == 1: # user
        await client.run_until_disconnected()
    await bot_client.run_until_disconnected()


