"""Load all user defined config and env vars."""

import logging
import os
import sys
from typing import Dict, List, Optional, Union

from dotenv import load_dotenv
from pydantic import BaseModel, validator  # pylint: disable=no-name-in-module
from pymongo import MongoClient
from telethon import TelegramClient
from telethon.sessions import StringSession

from test_tele import storage as stg
from test_tele.const import BOT_CONFIG_FILE_NAME
from test_tele.plugin_models import PluginConfig

pwd = os.getcwd()
env_file = os.path.join(pwd, ".env")

load_dotenv(env_file)


class UserBot(BaseModel):
    """Configuration for user that using bot"""

    user_id: int = 0
    count: int = 10
    offset: int = 0
    status: int = 0 # 0: standby, 1: processing
    links: list[str] = []
    output_media: str = 0 # 0: album, 1: telegraph, 2: zip
    
    watermark: bool = False
    watermark_img: str = f"wm/{user_id}.png" # path to watermark

    config_ignore: bool = True
    user_config_path: str = "config/config.json"


class BotMessages(BaseModel):
    start: str = "Hi! I am alive, don't mind the profile picture 😭"
    bot_help: str = "For more details, please contact @rizumiya"


class BotConfig(BaseModel):
    """The blueprint for Media Downloader live's bot"""

    # pylint: disable=too-few-public-
    bot_name: str = "@ttloli_bot"
    bot_messages = BotMessages()
    user_cfg: List[UserBot] = []
    supported_url: List[str] = []


def write_config_to_file(config: BotConfig):
    with open(BOT_CONFIG_FILE_NAME, "w", encoding="utf8") as file:
        file.write(config.json())


def detect_config_type() -> int:
    if os.getenv("MONGO_CON_STR"):
        if MONGO_CON_STR:
            logging.info("Using mongo db for storing config!")
            client = MongoClient(MONGO_CON_STR)
            stg.mycol = setup_mongo(client)
        return 2
    if BOT_CONFIG_FILE_NAME in os.listdir():
        logging.info(f"{BOT_CONFIG_FILE_NAME} detected!")
        return 1

    else:
        logging.info(
            "config file not found. mongo not found. creating local config file."
        )
        cfg = BotConfig()
        write_config_to_file(cfg)
        logging.info(f"{BOT_CONFIG_FILE_NAME} created!")
        return 1
    

def read_bot_config(count=1) -> BotConfig:
    """Load the configuration defined by user."""
    if count > 3:
        logging.warning("Failed to read config, returning default config")
        return BotConfig()
    if count != 1:
        logging.info(f"Trying to read config time:{count}")
    try:
        if stg.BOT_CONFIG_TYPE == 1:
            with open(BOT_CONFIG_FILE_NAME, encoding="utf8") as file:
                return BotConfig.parse_raw(file.read())
        elif stg.BOT_CONFIG_TYPE == 2:
            return read_db()
        else:
            return BotConfig()
    except Exception as err:
        logging.warning(err)
        stg.BOT_CONFIG_TYPE = detect_config_type()
        return read_bot_config(count=count + 1)


def write_bot_config(config: BotConfig, persist=True):
    """Write changes in config back to file."""
    if stg.BOT_CONFIG_TYPE == 1 or stg.BOT_CONFIG_TYPE == 0:
        write_config_to_file(config)
    elif stg.BOT_CONFIG_TYPE == 2:
        if persist:
            update_db(config)


def setup_mongo(client):

    mydb = client[MONGO_DB_NAME]
    mycol = mydb[MONGO_COL_NAME]
    if not mycol.find_one({"_id": 0}):
        mycol.insert_one({"_id": 0, "author": "tgcf", "config": BotConfig().dict()})

    return mycol


def update_db(cfg):
    stg.mycol.update_one({"_id": 0}, {"$set": {"config": cfg.dict()}})


def read_db():
    obj = stg.mycol.find_one({"_id": 0})
    cfg = BotConfig(**obj["config"])
    return cfg


stg.BOT_CONFIG_TYPE = detect_config_type()
BOT_CONFIG = read_bot_config()

MONGO_CON_STR = os.getenv("MONGO_CON_STR")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "tgcf-config")
MONGO_COL_NAME = os.getenv("MONGO_COL_NAME", "tgcf-instance-0")

SUPPORTED_URL = []

logging.info("config_bot.py got executed")
