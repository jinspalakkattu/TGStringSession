#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @lnc3f3r Jins Mathew

import os
import logging
import time

from heroku3 import from_key

from logging.handlers import RotatingFileHandler

from translation import Translation

# Change Accordingly While Deploying To A VPS
API_ID = int(os.environ.get("API_ID"))

API_HASH = os.environ.get("API_HASH")

BOT_TOKEN = os.environ.get("BOT_TOKEN"")

APP_NAME = os.environ.get("APP_NAME", "")

API_KEY = os.environ.get("API_KEY", "")

# HU_APP = from_key(API_KEY).apps()[APP_NAME]

VERIFY = {}

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            "tg_session/plugins/autofilterbot.txt",
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

start_uptime = time.time()


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
