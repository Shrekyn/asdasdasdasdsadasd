from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from config import BOT_TOKEN
from handlers import start, chat

bot = Bot(token=BOT_TOKEN)
storage = RedisStorage2()
dp = Dispatcher(bot, storage=storage)

# Регистрируем хендлеры
start.register(dp)
chat.register(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
