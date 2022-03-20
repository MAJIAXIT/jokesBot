from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import bot_token
from config import dbname, user, password, host
import psycopg2
import random

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    """React on command /start"""

    await message.bot.send_message(message.from_user.id, "Hello!\nInsert some command.")


@dp.message_handler(commands=["joke"])
async def start_command(message: types.Message):
    """React on command /joke"""

    await message.reply(f"{get_random_joke()}", reply=False)


def get_random_joke():
    """Get the random joke from the DB"""

    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jokes WHERE id = %s",
                   (random.randint(0, 30), ))
    record = cursor.fetchone()

    cursor.close()
    conn.close()
    return record[1]


if __name__ == "__main__":
    executor.start_polling(dp)
