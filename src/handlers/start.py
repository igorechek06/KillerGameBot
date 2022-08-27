from aiogram.dispatcher import FSMContext
from aiogram.types import BotCommandScopeChat, ContentType, Message

from bot import bot, dp
from libs import commands, text
from libs.states import GameState, JoinState
from rooms import rooms


async def join_state(msg: Message) -> None:
    await msg.reply(text.IMAGE)
    await JoinState.first()
    await bot.set_my_commands(
        commands.join,
        BotCommandScopeChat(msg.from_user.id),
    )


@dp.message_handler(commands=["start"])
async def start(msg: Message, state: FSMContext) -> None:
    room_id = msg.get_args()
    await msg.reply(text.START)

    if room_id != "" and room_id in rooms and not rooms[room_id].started:
        async with state.proxy() as data:
            data["create"] = False
            data["room_id"] = room_id

        await join_state(msg)
    else:
        await bot.delete_my_commands(BotCommandScopeChat(msg.from_user.id))


@dp.message_handler(commands=["rules"], state=[None, GameState.game])
async def rules(msg: Message) -> None:
    await msg.reply(text.RULES)


@dp.message_handler(commands=["create"])
async def create(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["create"] = True
    await join_state(msg)


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

    await join_state(msg)


@dp.message_handler(content_types=ContentType.ANY)
async def any(msg: Message) -> None:
    await bot.delete_my_commands(BotCommandScopeChat(msg.from_user.id))
