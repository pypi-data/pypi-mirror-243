import json

import streamlit as st

from test_tele.config import CONFIG_FILE_NAME, read_config, write_config
from test_tele.config_bot import read_bot_config, write_bot_config
from test_tele.utils import platform_info
from test_tele.web_ui.password import check_password
from test_tele.web_ui.utils import hide_st, get_list, get_string

CONFIG = read_config()
BOT_CONFIG = read_bot_config()

st.set_page_config(
    page_title="Advanced",
    page_icon="🔬",
)
hide_st(st)

if check_password(st):

    st.warning("This page is for developers and advanced users.")
    if st.checkbox("I agree"):

        with st.expander("Version & Platform"):
            st.code(platform_info())

        with st.expander("Configuration"):
            with open(CONFIG_FILE_NAME, "r") as file:
                data = json.loads(file.read())
                dumped = json.dumps(data, indent=3)
            st.download_button(
                f"Download config json", data=dumped, file_name=CONFIG_FILE_NAME
            )
            st.json(data)

        with st.expander("Special Options for Live Mode"):
            CONFIG.live.sequential_updates = st.checkbox(
                "Enforce sequential updates", value=CONFIG.live.sequential_updates
            )

            CONFIG.live.delete_on_edit = st.text_input(
                "Delete a message when source edited to",
                value=CONFIG.live.delete_on_edit,
            )
            st.write(
                "When you edit the message in source to something particular, the message will be deleted in both source and destinations."
            )

            if st.button("Save"):
                write_config(CONFIG)

        with st.expander("Bot Configuration"):
            st.info(
                    "Note: For userbots, the commands start with `.` instead of `/`, like `.start` and not `/start`"
            )
            BOT_CONFIG.bot_name = st.text_input(
                "The Username of the bot", value=BOT_CONFIG.bot_name
            )
            BOT_CONFIG.bot_messages.start = st.text_area(
                "Bot's Reply to /start command", value=BOT_CONFIG.bot_messages.start
            )
            BOT_CONFIG.bot_messages.bot_help = st.text_area(
                "Bot's Reply to /help command", value=BOT_CONFIG.bot_messages.bot_help
            )
            BOT_CONFIG.supported_url = get_list(
                st.text_area(
                    "Supported URL", value=get_string(BOT_CONFIG.supported_url)
                )
            )

            if st.button("Save Bot Config"):
                write_bot_config(BOT_CONFIG)
            