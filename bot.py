import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
import g4f

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")


@dp.message()
async def gpt_handler(message: types.Message) -> None:
    for i in range(3):
        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
        response = await g4f.ChatCompletion.create_async(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}])
        if response:
            await message.answer(response)
            break
    else:
        await message.answer('Error!')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
