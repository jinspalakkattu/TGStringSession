import os

from heroku3 import from_key
from pyrogram import Client
from pyromod import listen

# from . import API_HASH, API_ID, BOT_TOKEN
API_ID = int(os.environ.get("API_ID", 3607361))

API_HASH = os.environ.get("API_HASH", "c57bcc4b09591db4f90f60b469e8870f")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "1992112183:AAFMs4xbUCY96P8j5yAKdeIYCUPev8PGt0c")

APP_NAME = os.environ.get("APP_NAME", "")

API_KEY = os.environ.get("API_KEY", "")

# HU_APP = from_key(API_KEY).apps()[APP_NAME]

bot = Client(":memory:",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN)


# class Bot(Client):
#
#     def __init__(self):
#         super().__init__(
#             ":memory:",
#             api_hash=API_HASH,
#             api_id=API_ID,
#             plugins={
#                 "root": "tg_session/plugins"
#             },
#             workers=4,
#             bot_token=BOT_TOKEN,
#             sleep_threshold=10
#         )
#         self.LOGGER = LOGGER
#
#     async def start(self):
#         await super().start()
#         bot_details = await self.get_me()
#         self.set_parse_mode("html")
#         self.LOGGER(__name__).info(
#             f"@{bot_details.username}  started! "
#         )
#
#     async def stop(self, *args):
#         await super().stop()
#         self.LOGGER(__name__).info("Bot stopped. Bye.")
