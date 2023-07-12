import logging
import pickle
from os.path import exists

from bot import dp
from libs.room import Room
from libs.states import GameState

rooms: dict[str, Room] = {}


def save_rooms() -> None:
    global rooms

    with open("data/rooms.pkl", "wb") as file:
        pickle.dump(rooms, file)


async def load_rooms() -> None:
    global rooms

    if not exists("data/rooms.pkl"):
        return

    with open("data/rooms.pkl", "rb") as file:
        room_id: str
        room: Room

        for room_id, room in pickle.load(file).items():
            rooms[room_id] = room

            for user in room.users:
                state = dp.current_state(chat=user.id, user=user.id)

                if not room.started:
                    await state.set_state(GameState.wait_start.state)
                elif not user.alive:
                    await state.set_state(GameState.wait_end.state)
                else:
                    await state.set_state(GameState.game.state)

                async with state.proxy() as data:
                    data["room_id"] = room_id

    logging.info("Rooms loaded")
