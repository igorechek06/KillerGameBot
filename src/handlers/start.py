from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot import dp
from lib import text
from lib.states import JoinState
from rooms import rooms


@dp.message_handler(commands=["start"])
async def start(msg: Message, state: FSMContext) -> None:
    room_id = msg.get_args()
    await msg.reply(text.START)

    if room_id != "" and room_id in rooms and not rooms[room_id].started:
        async with state.proxy() as data:
            data["create"] = False
            data["room_id"] = room_id

        await msg.reply(text.IMAGE)
        await JoinState.first()


@dp.message_handler(commands=["rules"], state="*")
async def rules(msg: Message) -> None:
    await msg.reply(text.RULES)


@dp.message_handler(commands=["create"])
async def create(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["create"] = True

    await msg.reply(text.IMAGE)
    await JoinState.first()


@dp.message_handler(commands=["join"])
async def join(msg: Message, state: FSMContext) -> None:
    room_id = msg.get_args()
    if room_id == "":
        await msg.reply(text.ID_ERR)
        return
    if room_id not in rooms:
        await msg.reply(text.ROOM_NOT_FOUND)
        return
    if rooms[room_id].started:
        await msg.reply(text.ROOM_STARTED)
        return

    async with state.proxy() as data:
        data["create"] = False
        data["room_id"] = room_id

    await msg.reply(text.IMAGE)
    await JoinState.first()


@dp.message_handler(commands=["test"])
async def test(msg: Message) -> None:
    for i, g in rooms.items():
        print(i, g.users)
