import logging

from aiogram import Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.utils.executor import start_polling

# isort: off
from bot import bot, dp
import libs
import rooms
import handlers

logging.basicConfig(level=logging.INFO)


async def on_start(dp: Dispatcher) -> None:
    await rooms.load_rooms()

    await bot.set_my_commands(
        libs.commands.private,
        BotCommandScopeAllPrivateChats(),
    )
    logging.info("Commands updated")


if __name__ == "__main__":
    start_polling(dp, skip_updates=False, on_startup=on_start)
