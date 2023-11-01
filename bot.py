import asyncio
import logging
import sys
from datetime import datetime
from config import BOT_TOKEN, FLOOD_TIME, EXCEPT_USERS
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import CommandStart
from aiogram.types import Message
from g4f import ChatCompletion
from db.models import GetDB, User


dp = Dispatcher()
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)


@dp.message(CommandStart())
async def start(message: Message) -> None:
    user = message.from_user
    with GetDB() as db:
        User.update_or_create(
            db=db,
            userid=user.id,
            name=user.full_name,
            username=user.username
        )
    await message.answer(f"Hello, {message.from_user.full_name}!")


@dp.message()
async def chat(message: types.Message) -> None:
    user = message.from_user
    with GetDB() as db:
        db_user = User.update_or_create(
            db=db,
            userid=user.id,
            name=user.first_name,
            username=user.username
        )
        if user.id not in EXCEPT_USERS:
            if db_user.last_used and (datetime.now() - db_user.last_used).seconds < FLOOD_TIME:
                await message.answer(
                    f'Please wait {FLOOD_TIME - (datetime.now() - db_user.last_used).seconds} seconds')
                return
            else:
                db_user.set_last_used(db)
    for i in range(3):
        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
        response = await ChatCompletion.create_async(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}])
        if response:
            await message.answer(response)
            break
    else:
        await message.answer('Error!')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
