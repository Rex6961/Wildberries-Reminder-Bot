from .models import async_session
from .models import User, Event
from sqlalchemy import select


async def set_user(tg_id):
    """
    Асинхронная функция для добавления пользователя в базу данных, если он еще не существует.

    :param tg_id: ID пользователя в Telegram.
    """
    # Создание асинхронной сессии с базой данных
    async with async_session() as session:
        # Поиск пользователя по его tg_id
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        # Если пользователь не найден, добавляем его в базу данных
        if not user:
            session.add(User(tg_id=tg_id))
            # Фиксация изменений в базе данных
            await session.commit()


async def set_event(event_id, date, interval, message, tg_id):
    """
    Асинхронная функция для добавления события в базу данных, если оно еще не существует.

    :param event_id: Уникальный идентификатор события.
    :param date: Дата и время события.
    :param interval: Интервал повторения события.
    :param message: Текст сообщения напоминания.
    :param tg_id: ID пользователя в Telegram.
    """
    # Создание асинхронной сессии с базой данных
    async with async_session() as session:
        # Поиск события по его event_id
        event = await session.scalar(select(Event).where(Event.id == event_id))

        # Если событие не найдено, добавляем его в базу данных
        if not event:
            session.add(Event(id=event_id, date=date, interval=interval, message=message, tg_id=tg_id))
            # Фиксация изменений в базе данных
            await session.commit()


async def get_events(tg_id):
    """
    Асинхронная функция для получения всех событий пользователя.

    :param tg_id: ID пользователя в Telegram.
    :return: Генератор объектов Event, связанных с пользователем.
    """
    # Создание асинхронной сессии с базой данных
    async with async_session() as session:
        # Получение всех событий пользователя по его tg_id
        return await session.scalars(select(Event).where(Event.tg_id == tg_id))


async def get_remove_events(user_id):
    """
    Асинхронная функция для получения всех событий пользователя, доступных для удаления.

    :param user_id: ID пользователя в Telegram.
    :return: Генератор объектов Event, связанных с пользователем.
    """
    # Создание асинхронной сессии с базой данных
    async with async_session() as session:
        # Получение всех событий пользователя по его user_id
        return await session.scalars(select(Event).where(Event.tg_id == user_id))


async def get_event(event_id):
    """
    Асинхронная функция для получения конкретного события по его ID.

    :param event_id: Уникальный идентификатор события.
    :return: Объект Event или None, если событие не найдено.
    """
    # Создание асинхронной сессии с базой данных
    async with async_session() as session:
        # Поиск события по его event_id
        return await session.scalar(select(Event).where(Event.id == event_id))


async def remove_event(event_id):
    """
    Асинхронная функция для удаления события из базы данных по его ID.

    :param event_id: Уникальный идентификатор события.
    """
    # Создание асинхронной сессии с базой данных
    async with async_session() as session:
        # Поиск события по его event_id
        event = await session.scalar(select(Event).where(Event.id == event_id))
    
        # Если событие найдено, удаляем его из базы данных
        if event:
            await session.delete(event)
            # Фиксация изменений в базе данных
            await session.commit()
