import random

from libs.user import User


class Room:
    owner: int
    users: list[User]
    started: bool

    def __init__(self, owner: int) -> None:
        self.owner = owner
        self.users = []
        self.started = False

    def start_game(self) -> None:
        from rooms import save_rooms

        random.shuffle(self.users)
        for i in range(len(self.users)):
            user = self.users[i]
            target = self.users[(i + 1) % len(self.users)]
            user.target = target
            target.killer = user
        self.started = True
        save_rooms()

    def get(self, user_id: int) -> User:
        for user in self.users:
            if user.id == user_id:
                return user
        raise RuntimeError

    def count_alive(self) -> int:
        return len(list(filter(lambda u: u.alive, self.users)))
