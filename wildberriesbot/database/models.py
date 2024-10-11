from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

# Создание асинхронного двигателя для подключения к базе данных SQLite с использованием aiosqlite
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

# Создание асинхронного sessionmaker для управления сессиями с базой данных
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовый класс для всех моделей ORM, использующий асинхронные атрибуты.
    """
    pass

class User(Base):
    """
    Модель пользователя, представляющая таблицу 'users' в базе данных.
    """
    __tablename__ = "users"  # Название таблицы в базе данных

    id: Mapped[int] = mapped_column(primary_key=True)  # Первичный ключ таблицы
    tg_id = mapped_column(BigInteger, unique=True)     # Уникальный идентификатор пользователя в Telegram

class Event(Base):
    """
    Модель события, представляющая таблицу 'Events' в базе данных.
    """
    __tablename__ = "Events"  # Название таблицы в базе данных

    id: Mapped[int] = mapped_column(primary_key=True)         # Первичный ключ таблицы
    date = mapped_column(DateTime)                            # Дата и время события
    interval: Mapped[int] = mapped_column(default=0)          # Интервал повторения события (по умолчанию 0)
    message: Mapped[str] = mapped_column(String(128))        # Текст сообщения напоминания (максимум 128 символов)
    
    tg_id = mapped_column(BigInteger, ForeignKey("users.tg_id"))  # Внешний ключ, связывающий событие с пользователем

    # Определение отношения между Event и User моделями
    tg = relationship("User", foreign_keys=[tg_id])

async def async_main():
    """
    Асинхронная функция для создания всех таблиц в базе данных на основе определенных моделей.
    """
    async with engine.begin() as conn:
        # Создание всех таблиц, если они еще не существуют
        await conn.run_sync(Base.metadata.create_all)
