from datetime import datetime, timedelta
from typing import Callable, Any, Dict, Awaitable

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram.types import TelegramObject, Message
from aiogram import BaseMiddleware, Bot

from handlers.event_notice import EventNotice, get_count


class CounterMiddleware(BaseMiddleware):
    """
    Middleware для интеграции APScheduler в обработчики Aiogram.
    Добавляет планировщик задач в данные, доступные для обработчиков.
    """
    
    def __init__(self, scheduler: AsyncIOScheduler) -> None:
        """
        Инициализация middleware с переданным планировщиком задач.

        :param scheduler: Экземпляр AsyncIOScheduler для планирования задач.
        """
        self.scheduler = scheduler

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Метод, вызываемый при каждом событии (сообщении) бота.
        Добавляет планировщик задач в данные, передаваемые обработчику.

        :param handler: Функция обработчика, которую необходимо вызвать.
        :param event: Объект события Telegram (например, Message).
        :param data: Словарь данных, передаваемых обработчику.
        :return: Результат выполнения обработчика.
        """
        # Добавление планировщика задач в словарь данных
        data["apscheduler"] = self.scheduler
        # Вызов следующего обработчика в цепочке с обновленными данными
        return await handler(event, data)


async def send_message_scheduler(bot: Bot, message: Message, date: Dict[str, Any]):
    """
    Функция, которая отправляет запланированное сообщение пользователю.

    :param bot: Экземпляр бота для отправки сообщений.
    :param message: Исходное сообщение от пользователя, на основе которого отправляется напоминание.
    :param date: Словарь с данными о времени и интервалах напоминания.
    """
    # Создание экземпляра EventNotice с извлеченными из даты параметрами
    event_notice = EventNotice(get_count(date))
    # Выполнение расчета времени и интервала
    event_notice()
    
    # Получение общего времени в секундах и интервала повторений
    time_seconds = event_notice.resultTime
    interval = event_notice.resultInterval
    
    # Текущая дата и время начала напоминания
    start_date = datetime.now()
    
    # Дата и время окончания напоминаний
    end_date = (start_date + timedelta(seconds=time_seconds)).strftime("%d/%m/%Y, %H:%M:%S")

    # Формирование и отправка сообщения пользователю с информацией о напоминании
    await bot.send_message(
        chat_id=message.from_user.id, 
        text=(
            f"@{message.from_user.id}\n"
            f"Привет {message.from_user.full_name},\n"
            f"Сейчас {end_date}:\n"
            f"Завершите задание - {message.text}"
        )
    )
