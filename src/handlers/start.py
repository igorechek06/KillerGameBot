from aiogram.types import Message

from bot import dp
from lib import text
from lib.states import Join


@dp.message_handler(commands=["start"])
async def start(msg: Message) -> None:
    await msg.reply(text.START)


@dp.message_handler(commands=["rules"])
async def rules(msg: Message) -> None:
    await msg.reply(text.RULES)


@dp.message_handler(commands=["create"])
async def create(msg: Message) -> None:
    pass


@dp.message_handler(commands=["join"])
async def join(msg: Message) -> None:
    await msg.reply(text.IMAGE)
    await Join.first()
