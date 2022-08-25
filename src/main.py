import logging

from aiogram import Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.utils.executor import start_polling

import handlers
import libs
from bot import bot, dp

logging.basicConfig(level=logging.INFO)


async def on_start(dp: Dispatcher) -> None:
    await bot.set_my_commands(
        libs.commands.private,
        BotCommandScopeAllPrivateChats(),
    )


if __name__ == "__main__":
    start_polling(dp, skip_updates=False, on_startup=on_start)
