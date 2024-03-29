START = """Я бот который поможет сыграть в «Киллера».
/rules - Правила
/create - Создать игру"""

RULES = """<b>Вам нужно убивать цели и оставаться в живых.</b>
1) Каждый игрок является одновременно и охотником и жертвой.
2) Каждый участник получает полную информацию о цели.
3) Убийство производится путем дотрагивания до человека и произнесения ключевой фразы «Tы убит». 
   Убийство должно быть совершено без каких-либо свидетелей.
   Рядом (в радиусе 50-60м) не должно быть ни участников игры, ни обычных людей.
5) Если вас убили, то вы должны прописать команду /fail."""

IMAGE = """Пожалуйста пришли мне своё фото."""
IMAGE_ERR = f"""Это не похоже на фото. {IMAGE}"""

FULL_NAME = """Пожалуйста скажи мне своё ФИО."""
FULL_NAME_ERR = f"""Это не похоже на ФИО. {FULL_NAME}"""

CANCEL = """Действие отменено."""

JOIN = """Ты присоеденился к игре.
/invite - Получить инвайт ссылку
/leave - Выйти из игры"""

LEAVE = """Ты вышел из игры.
/rules - Правила
/create - Создать игру"""

USER_JOIN = (
    """Новый игрок присоеденился: <a href=\"tg://user?id={id}\">{full_name}</a>"""
)
USER_LEAVE = """Игрок вышел из игры: <a href=\"tg://user?id={id}\">{full_name}</a>"""

CREATE = """Игра была создана.
/startgame - Начать игру.
/stopgame - Отменить игру.
/invite - Получить инвайт ссылку.
<code>{room_id}</code> - ID комнаты."""

INVITE = """<code>https://t.me/ru_killer_game_bot?start={room_id}</code>"""

ID_ERR = """ID комнаты не указан. Укажите его таким образом: /join ID"""

ROOM_NOT_FOUND = """Игра не найдена"""
ROOM_NO_LONGER_EXIST = """Игры больше не существует"""
ROOM_STARTED = """Игра уже запущена"""

GAME_STOPPED = """Игра отменена."""
GAME_FINISHED = """Игра окончена.
Статистика игры:
{stats}"""
GAME_STARTED = """Игра началась, удачи )
/rules - Правила.
/fail - Меня убили.
/target - Напомнить цель."""
GAME_START_ERR = """Нужно хотя бы 3 игрока чтобы начать игру."""

TARGET = """Твоя цель: <a href=\"tg://user?id={id}\">{full_name}</a>"""

FAIL_ACCEPT = """Подтвердите действие."""
FAIL_ACCEPT_BTN = """Да меня убили."""
FAIL_DECLINE_BTN = """Нет меня не убили."""
FAIL = """Тебя убили, не расстраивайся в следующий раз повезёт больше.
Убийств: {kills}"""

KILL = """Поздравляю с убийством вашей цели.
Убийств: {kills}"""
KILL_ENTRY = """<a href=\"tg://user?id={id}\">{full_name}</a> - {kills}"""

ALIVE = """Осталось в живых: {alive}"""
