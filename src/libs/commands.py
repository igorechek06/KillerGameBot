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

wait_owner = [
    cmd("startgame", "Начать игру"),
    cmd("stopgame", "Остановить игру"),
    cmd("invite", "Получить инвайт ссылку"),
]

wait_user = [
    cmd("invite", "Получить инвайт ссылку"),
    cmd("leave", "Выйти из игры"),
]

game = [
    cmd("fail", "Меня убили"),
    cmd("target", "Напомнить цель"),
    cmd("rules", "Правила"),
]
