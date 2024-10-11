import sys
import os
import asyncio
import logging
from dotenv import load_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from middlewares.scheduler import CounterMiddleware
from handlers.handler_scheduler import router_scheduler
from handlers.start import router_start
from database.models import async_main

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена бота из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")

# Создание экземпляра диспетчера
dp = Dispatcher()

# Создание планировщика задач
scheduler = AsyncIOScheduler()

async def main():
    # Запуск и создание базы данных
    await async_main()
    # Добавление middleware для диспетчера с использованием планировщика
    dp.update.middleware(CounterMiddleware(scheduler=scheduler))
    
    # Подключение роутеров обработчиков
    dp.include_routers(router_start, router_scheduler)
    
    # Создание экземпляра бота с указанным токеном и режимом парсинга сообщений
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    # Запуск планировщика
    scheduler.start()
    
    try:
        # Запуск поллинга обновлений от бота
        await dp.start_polling(bot)
        
        # Настройка логирования на уровень DEBUG и вывод в стандартный поток вывода
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    except:
        # В случае ошибки остановить планировщик
        scheduler.shutdown()

if __name__ == "__main__":
    # Настройка базового логирования на уровень INFO и вывод в стандартный поток вывода
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    # Запуск основной асинхронной функции
    asyncio.run(main())
