from aiogram.dispatcher import FSMContext
from aiogram.types import BotCommandScopeChat, CallbackQuery
from aiogram.types import InlineKeyboardButton as IB
from aiogram.types import InlineKeyboardMarkup as IM
from aiogram.types import Message

from bot import bot, dp
from libs import commands, text
from libs.states import GameState
from rooms import rooms


@dp.message_handler(commands=["startgame"], state=GameState.wait)
async def full_name(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        room = rooms[data["room_id"]]

    if room.owner != msg.from_user.id:
        return

    if len(room.users) < 3:
        await msg.reply(text.GAME_START_ERR)
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
                    id=user.target.id,
                ),
            )
        await dp.current_state(chat=user.id, user=user.id).set_state(
            GameState.game.state,
        )
        await bot.set_my_commands(
            commands.game,
            BotCommandScopeChat(user.id),
        )


@dp.message_handler(commands=["stopgame"], state=GameState.wait)
async def stopgame_wait(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        room = rooms[data["room_id"]]
        rooms.pop(data["room_id"])

    if room.owner != msg.from_user.id:
        return

    for user in room.users:
        await bot.send_message(user.id, text.GAME_STOPED)
        await dp.current_state(chat=user.id, user=user.id).finish()
        await bot.delete_my_commands(BotCommandScopeChat(user.id))


@dp.message_handler(commands=["leave"], state=GameState.wait)
async def leave(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        room = rooms[data["room_id"]]
        user = room.get(msg.from_user.id)

    if room.owner == msg.from_user.id:
        return

    room.users.remove(user)

    await msg.reply(text.LEAVE)
    await bot.send_photo(
        room.owner,
        user.photo,
        caption=text.USER_LEAVE.format(
            full_name=user.full_name,
            id=msg.from_user.id,
        ),
    )
    await state.finish()
    await bot.delete_my_commands(BotCommandScopeChat(msg.from_user.id))


@dp.message_handler(commands=["invite"], state=GameState.wait)
async def invite(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        room_id = data["room_id"]

    await msg.reply(text.INVITE.format(room_id=room_id))


@dp.message_handler(commands=["fail"], state=GameState.game)
async def fail(msg: Message, state: FSMContext) -> None:
    await msg.reply(
        text.FAIL_ACCEPT,
        reply_markup=IM().add(
            IB(text.FAIL_ACCEPT_BTN, callback_data="fail:accept"),
            IB(text.FAIL_DECLINE_BTN, callback_data="decline"),
        ),
    )


@dp.callback_query_handler(
    lambda clb: clb.data == "fail:accept",
    state=GameState.game,
)
async def fail_accept(clb: CallbackQuery, state: FSMContext) -> None:
    await clb.message.delete_reply_markup()
    async with state.proxy() as data:
        room_id = data["room_id"]
        room = rooms[room_id]

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
            if user.alive:
                await dp.current_state(chat=user.id, user=user.id).finish()
                await bot.delete_my_commands(BotCommandScopeChat(user.id))

        rooms.pop(room_id)

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
                    id=killer.target.id,
                ),
            )

        await state.finish()
        await bot.delete_my_commands(BotCommandScopeChat(clb.from_user.id))


@dp.callback_query_handler(
    lambda clb: clb.data == "decline",
    state=GameState.game,
)
async def fail_decline(clb: CallbackQuery) -> None:
    await clb.message.delete()


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
                id=user.target.id,
            ),
        )
