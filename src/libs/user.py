from typing import Optional


class User:
    id: int
    photo: str
    full_name: str
    kills: int
    alive: bool
    target: Optional["User"]
    killer: Optional["User"]

    def __init__(self, id: int, photo: str, full_name: str) -> None:
        self.id = id
        self.photo = photo
        self.full_name = full_name
        self.kills = 0
        self.alive = True
        self.target = None
        self.killer = None

    def die(self) -> None:
        if self.killer is not None:
            self.killer.target = self.target
            self.killer.kills += 1
        if self.target is not None:
            self.target.killer = self.killer
        self.target = None
        self.killer = None
        self.alive = False
