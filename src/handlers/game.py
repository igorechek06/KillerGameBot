from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from aiogram.types import InlineKeyboardButton as IB
from aiogram.types import InlineKeyboardMarkup as IM
from aiogram.types import Message

from bot import bot, dp
from lib import text
from lib.states import GameState
from rooms import rooms


@dp.message_handler(commands=["startgame"], state=GameState.wait)
async def full_name(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        room = rooms[data["room_id"]]

    if room.owner != msg.from_user.id:
        return

    room.start_game()
    for user in room.users:
        await bot.send_message(user.id, text.GAME_STARTED)
        if user.target is not None:
            await bot.send_photo(
                user.id,
                user.target.photo,
                caption=text.TARGET.format(
                    full_name=user.target.full_name,
                    id=user.id,
                ),
            )
        await dp.current_state(chat=user.id, user=user.id).set_state(
            GameState.game.state,
        )


@dp.message_handler(commands=["stopgame"], state=GameState.wait)
async def stopgame_wait(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        room = rooms[data["room_id"]]

    for user in room.users:
        await bot.send_message(user.id, text.GAME_STOPED)


@dp.message_handler(commands=["fail"], state=GameState.game)
async def fail(msg: Message, state: FSMContext) -> None:
    await msg.reply(
        text.FAIL_ACCEPT,
        reply_markup=IM().add(
            IB(text.FAIL_ACCEPT_BTN, callback_data="fail"),
        ),
    )


@dp.callback_query_handler(
    lambda clb: clb.data == "fail",
    state=GameState.game,
)
async def fail_accept(clb: CallbackQuery, state: FSMContext) -> None:
    await clb.message.delete_reply_markup()
    async with state.proxy() as data:
        room = rooms[data["room_id"]]

    user = room.get(clb.from_user.id)
    killer = user.killer
    user.die()

    if room.alives() == 1:
        t = text.GAME_FINISHD.format(
            stats="\n".join(
                [
                    text.KILL_ENTRY.format(
                        full_name=u.full_name,
                        kills=u.kills,
                        id=u.id,
                    )
                    for u in room.users
                ]
            )
        )

        for user in room.users:
            await bot.send_message(user.id, t)
    elif killer is not None:
        await clb.message.answer(text.FAIL.format(kills=user.kills))

        if killer.target is not None:
            await bot.send_message(
                killer.id,
                text.KILL.format(kills=killer.kills),
            )
            await bot.send_photo(
                killer.id,
                killer.target.photo,
                caption=text.TARGET.format(
                    full_name=killer.target.full_name,
                    id=user.id,
                ),
            )

    await state.finish()


@dp.message_handler(commands=["target"], state=GameState.game)
async def target(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        room = rooms[data["room_id"]]

    user = room.get(msg.from_user.id)
    if user.target is not None:
        await bot.send_photo(
            user.id,
            user.target.photo,
            caption=text.TARGET.format(
                full_name=user.target.full_name,
                id=user.id,
            ),
        )
