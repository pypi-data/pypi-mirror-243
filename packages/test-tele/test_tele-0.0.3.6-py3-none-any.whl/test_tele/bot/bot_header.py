import logging

from typing import TYPE_CHECKING
from telethon.tl import types

from test_tele.utils import start_sending

if TYPE_CHECKING:
    from test_tele.plugins import TgcfMessage


## Helper function for get_message


async def get_entity(event, entity):
    """Get chat entity from entity parameter"""
    if entity.isdigit() or entity.startswith("-"):
        chat = types.PeerChannel(int(entity))
    else:
        try:
            chat = await event.client.get_entity(entity)
        except Exception as e:
            chat = await event.client.get_entity(types.PeerChat(int(entity)))

    return chat


async def send_grouped_messages(chat, tm: "TgcfMessage", message, ids):
    """Send grouped messages"""
    client = tm.message.client

    group = []
    min_id = ids - 10 if ids > ids - ids else ids
    max_id = ids + 10

    grp_id = message.grouped_id
    messages = await client.get_messages(chat, min_id=min_id, max_id=max_id, reverse=True)
    if messages:
        for message in messages:
            if not message:
                continue
            if message.grouped_id != grp_id:
                continue
            group.append(message.media)

    if group:
        tm.new_file = group
        await start_sending(tm.message.chat_id, tm)
    else:
        logging.error('Cannot append item')
        return


async def forward_group_messages(chat, tm: "TgcfMessage", message, ids):
    """Forward grouped messages"""
    client = tm.message.client

    grp_id = message.grouped_id
    while True:
        message = await client.get_messages(chat, ids=ids)
        if message:
            if message.grouped_id == grp_id:
                tm.new_file = message.media
                await start_sending(tm.message.chat_id, tm)
                ids += 1
            else:
                return
        else:
            ids += 1

