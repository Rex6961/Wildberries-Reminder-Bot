from datetime import datetime, timedelta
from typing import Callable, Any, Dict, Awaitable

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from middlewares.scheduler import send_message_scheduler
from .event_notice import EventNotice, get_count
import database.requests as rq
import keyboards.keyboards as kb

# Создание экземпляра роутера для обработки сообщений, связанных с планировщиком
router_scheduler = Router()

# Определение состояний конечного автомата (FSM) для управления диалогом с пользователем
class Form(StatesGroup):
    event_time = State()  # Состояние ожидания ввода времени события
    event = State()       # Состояние ожидания ввода текста события

@router_scheduler.message(F.text.regexp(r"@.+\s+ctrl\s+(\d+[Mwdhms]){1,6}\s+\d+i"))
async def catch_event(message: Message, state: FSMContext) -> None:
    """
    Обработчик сообщений, соответствующих заданному регулярному выражению.
    Отлавливает у пользователя дату напоминания и количество повторений.
    """
    # Передаем в базу данных ID пользователя для регистрации или обновления информации
    await rq.set_user(message.from_user.id)
        
    # Установка состояния конечного автомата для ожидания ввода времени события
    await state.set_state(Form.event_time)

    # Обновление данных состояния с введенным временем события
    await state.update_data(event_time=message.text)
    
    # Переход к следующему состоянию - ожидание ввода текста события
    await state.set_state(Form.event)
    
    # Отправка пользователю подтверждения о фиксации времени и запроса на ввод текста напоминания
    await message.answer(
        "Спасибо, что воспользовались услугой напоминаний.\nВаше время зафиксировано."
    )
    await message.answer("Введите текст напоминания:")
    
    # Удаление сообщения пользователя для чистоты чата
    await message.delete()

@router_scheduler.message(Form.event)
async def get_event(
    message: Message, 
    bot: Bot, 
    apscheduler: AsyncIOScheduler, 
    state: FSMContext
) -> None:
    """
    Обработчик сообщения в состоянии Form.event.
    Сохраняет текст события, рассчитывает время и интервал для напоминания,
    и планирует задачу с использованием APScheduler.
    """
    # Обновление данных состояния с введенным текстом события
    await state.update_data(event=message.text)
    
    # Получение всех данных из состояния
    data = await state.get_data()

    try:
        # Создание экземпляра EventNotice с количеством повторений, полученных из времени события
        event_notice = EventNotice(get_count(data['event_time']))
        
        # Запуск метода EventNotice для расчета времени и интервала
        event_notice()
        
        # Получение рассчитанного времени в секундах и интервала повторений
        time_seconds = event_notice.resultTime
        interval = event_notice.resultInterval

        # Текущая дата и время начала напоминания
        start_date = datetime.now()

        # Расчет даты и времени окончания напоминаний
        date_db = start_date + timedelta(seconds=time_seconds)
        
        # Сохранение события в базу данных с деталями напоминания
        await rq.set_event(
            event_id=message.message_id,
            date=date_db,
            interval=interval,
            message=message.text,
            tg_id=message.from_user.id
        )
        
        # Дата и время окончания напоминаний для планировщика
        end_date = datetime.now() + timedelta(seconds=interval * time_seconds)
        
        # Отправка пользователю сообщения с подтверждением настроек напоминания
        await message.answer(
            f"Вы установили время на {end_date.strftime('%d/%m/%Y, %H:%M:%S')},\n"
            f"чтобы напомнить вам о:\n - {data['event']}"
        )
        
        # Удаление предыдущих сообщений для чистоты чата
        await message.bot.delete_messages(
            chat_id=message.chat.id,
            message_ids=[message.message_id - 1, 
                        message.message_id - 2,
                        message.message_id]
        )

        # Добавление задачи в планировщик APScheduler
        apscheduler.add_job(
            send_message_scheduler,  # Функция, которая будет вызвана при срабатывании задачи
            trigger="interval",      # Тип триггера - интервальный
            seconds=time_seconds,    # Интервал в секундах между вызовами функции
            start_date=start_date,   # Дата и время начала выполнения задачи
            end_date=end_date,       # Дата и время окончания выполнения задачи
            kwargs={
                "bot": bot,                     # Экземпляр бота для отправки сообщений
                "message": message,             # Объект сообщения для отправки
                "date": data['event_time']      # Время события для использования в сообщении
            },
        )
        
    except TypeError as e:
        # Логирование ошибки в консоль
        print(e)
        # Обработка исключения TypeError, если произошла ошибка в процессе настройки напоминания
        await message.answer("Nice try!")
    
    # Очистка состояния конечного автомата, возвращая пользователя к начальному состоянию
    await state.clear()

@router_scheduler.message(F.text == "События")
async def events(message: Message):
    """
    Обработчик сообщений с текстом "События".
    Отправляет пользователю список его событий с помощью клавиатуры.
    """
    tg_id = message.from_user.id
    # Отправка сообщения с предложением выбрать событие и прикрепленной клавиатурой
    await message.bot.send_message(
        chat_id=message.from_user.id, 
        text="Выберите событие", 
        reply_markup=await kb.events(tg_id)
    )

@router_scheduler.callback_query(F.data.startswith('event_'))
async def event(callback: CallbackQuery):
    """
    Обработчик callback-запросов, начинающихся с 'event_'.
    Отправляет пользователю детали выбранного события.
    """
    # Извлечение ID события из данных callback
    event_id = callback.data.split("_")[1]
    # Получение данных события из базы данных
    event_data = await rq.get_event(event_id)
    
    # Ответ на callback-запрос для уведомления пользователя
    await callback.answer("Вы выбрали событие")
    
    # Отправка пользователю подробной информации о событии
    await callback.message.answer(
        f"Дата события: {event_data.date.strftime('%d/%m/%Y, %H:%M')}\n"
        f"Повторение напоминания о событии: {event_data.interval}\n"
        f"Описание события: {event_data.message}"
    )

@router_scheduler.message(F.text == "Удалить")
async def remove_events(message: Message):
    """
    Обработчик сообщений с текстом "Удалить".
    Предоставляет пользователю возможность выбрать событие для удаления через клавиатуру.
    """
    user_id = message.from_user.id
    # Отправка сообщения с предложением выбрать событие для удаления и прикрепленной клавиатурой
    await message.bot.send_message(
        chat_id=message.from_user.id, 
        text="Выберите событие, которое вы хотите удалить", 
        reply_markup=await kb.remove_events(user_id)
    )
    # Удаление сообщения пользователя для чистоты чата
    await message.delete()
    
@router_scheduler.callback_query(F.data.startswith('remove_'))
async def remove_event(callback: CallbackQuery):
    """
    Обработчик callback-запросов, начинающихся с 'remove_'.
    Удаляет выбранное событие из базы данных и обновляет интерфейс пользователя.
    """
    # Извлечение ID события из данных callback
    event_id = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    # Удаление события из базы данных
    await rq.remove_event(event_id)
    
    # Ответ на callback-запрос для уведомления пользователя
    await callback.answer("👍")
    
    # Логирование ID пользователя в консоль (можно использовать для отладки)
    print(user_id)
    
    # Обновление сообщения с клавиатурой, удаляя выбранное событие
    await callback.message.edit_text(
        "Выберите событие",
        reply_markup=await kb.remove_events(user_id)
    )
