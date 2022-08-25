import logging

from aiogram.utils.executor import start_polling

import handlers
import libs
from bot import dp

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    start_polling(dp, skip_updates=True)
