import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.redis import RedisStorage
from config import BOT_TOKEN
from handlers import start, chat

# Инициализация бота
bot = Bot(token=BOT_TOKEN)

# Инициализация хранилища Redis
storage = RedisStorage(host='localhost', port=6379, db=0)  # Настройте параметры Redis по вашим нуждам

# Инициализация диспетчера
dp = Dispatcher(bot=bot, storage=storage)

# Регистрируем хендлеры
start.register(dp)
chat.register(dp)

# Функция для установки команд бота
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        # Добавьте другие команды, если нужно
    ]
    await bot.set_my_commands(commands)

# Основная функция для запуска бота
async def main():
    try:
        # Устанавливаем команды
        await set_commands(bot)
        # Запускаем polling
        await dp.start_polling(bot, skip_updates=True)
    finally:
        # Закрываем соединения при остановке
        await bot.session.close()
        await storage.close()

if __name__ == '__main__':
    asyncio.run(main())
