from aiogram.types import BotCommand as cmd

private = [
    cmd("start", "Cтартовое сообщение"),
    cmd("create", "Создать игру"),
    cmd("join", "Присоедениться к игре"),
    cmd("rules", "Правила"),
]

join = [
    cmd("cancel", "Отменить действие"),
]

wait_start_owner = [
    cmd("startgame", "Начать игру"),
    cmd("stopgame", "Остановить игру"),
    cmd("invite", "Получить инвайт ссылку"),
    cmd("rules", "Правила"),
]

wait_start_user = [
    cmd("invite", "Получить инвайт ссылку"),
    cmd("leave", "Выйти из игры"),
    cmd("rules", "Правила"),
]

game = [
    cmd("fail", "Меня убили"),
    cmd("target", "Напомнить цель"),
    cmd("rules", "Правила"),
]

wait_end = [
    cmd("alive", "Сколько игроков осталось в живых"),
    cmd("rules", "Правила"),
]
