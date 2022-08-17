from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message

from bot import dp
from lib import text
from lib.states import Join


@dp.message_handler(content_types=ContentType.PHOTO, state=Join.image)
async def image(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["image"] = msg.photo[-1].file_id
    await Join.next()
    await msg.reply(text.FULL_NAME)


@dp.message_handler(content_types=ContentType.TEXT, state=Join.full_name)
async def full_name(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["full_name"] = msg.text
    await state.finish()
    # TODO: game.join()


@dp.message_handler(commands=["cancel"], state=[Join.image, Join.full_name])
async def cancel(msg: Message, state: FSMContext) -> None:
    await msg.reply(text.CANCEL)
    await state.finish()


@dp.message_handler(state=Join.image)
async def image_err(msg: Message, state: FSMContext) -> None:
    await msg.reply(text.IMAGE_ERR)


@dp.message_handler(state=Join.full_name)
async def full_name_err(msg: Message, state: FSMContext) -> None:
    await msg.reply(text.FULL_NAME_ERR)
