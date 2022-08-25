from aiogram.dispatcher.filters.state import State, StatesGroup


class JoinState(StatesGroup):
    image = State()
    full_name = State()


class GameState(StatesGroup):
    wait = State()
    game = State()
