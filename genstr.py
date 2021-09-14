import asyncio

from bot import bot as ufs     # , HU_APP
from pyromod import listen
from asyncio.exceptions import TimeoutError

from translation import Translation as tr
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)


@ufs.on_message(filters.private & filters.command("start"))
async def genStr(_, msg: Message):
    chat = msg.chat
    api = await ufs.ask(
        chat.id, tr.API_TEXT.format(msg.from_user.mention)
    )
    if await is_cancel(msg, api.text):
        return
    try:
        check_api = int(api.text)
    except Exception:
        await msg.reply("`API_ID` is Invalid.\nPress /start to Start again.")
        return
    api_id = api.text
    hash = await ufs.ask(chat.id, tr.HASH_TEXT)
    if await is_cancel(msg, hash.text):
        return
    if not len(hash.text) >= 30:
        await msg.reply("`API_HASH` is Invalid.\nPress /start to Start again.")
        return
    api_hash = hash.text
    while True:
        number = await ufs.ask(chat.id, tr.PHONE_NUMBER_TEXT)
        if not number.text:
            continue
        if await is_cancel(msg, number.text):
            return
        phone = number.text
        confirm = await ufs.ask(chat.id, f'`Is "{phone}" correct? (y/n):` \n\nSend: `y` (If Yes)\nSend: `n` (If No)')
        if await is_cancel(msg, confirm.text):
            return
        if "y" in confirm.text:
            break
    try:
        client = Client("my_account", api_id=api_id, api_hash=api_hash)
    except Exception as e:
        await ufs.send_message(chat.id ,f"**ERROR:** `{str(e)}`\nPress /start to Start again.")
        return
    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()
    try:
        code = await client.send_code(phone)
        await asyncio.sleep(1)
    except FloodWait as e:
        await msg.reply(f"You have Floodwait of {e.x} Seconds")
        return
    except ApiIdInvalid:
        await msg.reply("API ID and API Hash are Invalid.\n\nPress /start to Start again.")
        return
    except PhoneNumberInvalid:
        await msg.reply("Your Phone Number is Invalid.\n\nPress /start to Start again.")
        return
    try:
        otp = await ufs.ask(chat.id, tr.OTP_TEXT, timeout=300)

    except TimeoutError:
        await msg.reply("Time limit reached of 5 min.\nPress /start to Start again.")
        return
    if await is_cancel(msg, otp.text):
        return
    otp_code = otp.text
    try:
        await client.sign_in(phone, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
    except PhoneCodeInvalid:
        await msg.reply("Invalid Code.\n\nPress /start to Start again.")
        return
    except PhoneCodeExpired:
        await msg.reply("Code is Expired.\n\nPress /start to Start again.")
        return
    except SessionPasswordNeeded:
        try:
            two_step_code = await ufs.ask(chat.id, tr.TWO_STEP_TEXT, timeout=300)
        except TimeoutError:
            await msg.reply("`Time limit reached of 5 min.\n\nPress /start to Start again.`")
            return
        if await is_cancel(msg, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await client.check_password(new_code)
        except Exception as e:
            await msg.reply(f"**ERROR:** `{str(e)}`")
            return
    except Exception as e:
        await ufs.send_message(chat.id ,f"**ERROR:** `{str(e)}`")
        return
    try:
        session_string = await client.export_session_string()
        await client.send_message("me", tr.SESSION_TEXT.format(session_string))
        await client.disconnect()
        text = "String Session is Successfully Generated.\nClick on Below Button."
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Show String Session", url=f"tg://openmessage?user_id={chat.id}")]]
        )
        await ufs.send_message(chat.id, text, reply_markup=reply_markup)
    except Exception as e:
        await ufs.send_message(chat.id ,f"**ERROR:** `{str(e)}`")
        return


@ufs.on_message(filters.private & filters.command("restart"))
async def restart(_, msg: Message):
    await msg.reply("Restarted Bot!")
    # HU_APP.restart()


@ufs.on_message(filters.private & filters.command("help"))
async def restart(_, msg: Message):
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Support Group', url='https://t.me/joinchat/6YRhp5LyjXNkNGY0'),
                InlineKeyboardButton('Developer', url='https://t.me/lnc3f3r')
            ],
            [
                InlineKeyboardButton('Bots Updates Channel', url='https://t.me/joinchat/7qlEga5lO0o2MTg0'),
            ]
        ]
    )
    await msg.reply(tr.HELP_TEXT.format(msg.from_user.mention), reply_markup=reply_markup)


async def is_cancel(msg: Message, text: str):
    if text.startswith("/cancel"):
        await msg.reply("Process Cancelled.")
        return True
    return False

if __name__ == "__main__":
    ufs.run()
