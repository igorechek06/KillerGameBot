from uuid import uuid4

from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message

from bot import bot, dp
from lib import text
from lib.room import Room
from lib.states import GameState, JoinState
from lib.user import User
from rooms import rooms


@dp.message_handler(content_types=ContentType.PHOTO, state=JoinState.image)
async def image(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["image"] = msg.photo[-1].file_id

    await JoinState.next()
    await msg.reply(text.FULL_NAME)


@dp.message_handler(content_types=ContentType.TEXT, state=JoinState.full_name)
async def full_name(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        photo = data["image"]
        full_name = msg.text
        create = data["create"]

        if create:
            room = Room(msg.from_user.id)
            room_id = str(uuid4())
            rooms[room_id] = room
        else:
            room_id = data["room_id"]
            if room_id not in rooms:
                await msg.reply(text.ROOM_NO_LONGER_EXIST)
                return
            room = rooms[room_id]

    await state.finish()

    user = User(msg.from_user.id, photo, full_name)
    room.users.append(user)
    await GameState.first()

    if create:
        await msg.reply(text.CREATE.format(room_id=room_id))
    else:
        await msg.reply(text.JOIN)
        await bot.send_photo(
            room.owner,
            user.photo,
            caption=text.NEW.format(full_name=user.full_name, id=user.id),
        )

    async with state.proxy() as data:
        data["room_id"] = room_id


@dp.message_handler(
    commands=["cancel"],
    state=[JoinState.image, JoinState.full_name],
)
async def cancel(msg: Message, state: FSMContext) -> None:
    await msg.reply(text.CANCEL)
    await state.finish()


@dp.message_handler(content_types=ContentType.ANY, state=JoinState.image)
async def image_err(msg: Message, state: FSMContext) -> None:
    await msg.reply(text.IMAGE_ERR)


@dp.message_handler(content_types=ContentType.ANY, state=JoinState.full_name)
async def full_name_err(msg: Message, state: FSMContext) -> None:
    await msg.reply(text.FULL_NAME_ERR)
