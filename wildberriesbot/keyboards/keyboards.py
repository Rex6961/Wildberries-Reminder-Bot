from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

import database.requests as rq

# Создание основного клавиатурного меню с кнопками "События" и "Удалить"
main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="События")],    # Первая строка клавиатуры с кнопкой "События"
        [KeyboardButton(text="Удалить")]      # Вторая строка клавиатуры с кнопкой "Удалить"
    ],
    resize_keyboard=True,                         # Автоматическое изменение размера клавиатуры под экран пользователя
    input_field_placeholder="Выберите событие..." # Текст-заполнитель в поле ввода
)

async def events(tg_id):
    """
    Асинхронная функция для создания инлайн-клавиатуры со списком событий пользователя.

    :param tg_id: ID пользователя Telegram.
    :return: Объект клавиатуры с кнопками для каждого события.
    """
    # Получение всех событий пользователя из базы данных
    all_events = await rq.get_events(tg_id)
    
    # Создание билдера для инлайн-клавиатуры
    keyboard = InlineKeyboardBuilder()
    
    # Добавление кнопки для каждого события
    for event in all_events:
        keyboard.add(
            InlineKeyboardButton(
                text=event.message,                        # Текст кнопки - описание события
                callback_data=f"event_{event.id}"          # Данные callback для идентификации события
            )
        )
    
    # Настройка количества кнопок в каждой строке и преобразование в разметку
    return keyboard.adjust(2).as_markup()

async def remove_events(user_id):
    """
    Асинхронная функция для создания инлайн-клавиатуры со списком событий пользователя для удаления.

    :param user_id: ID пользователя Telegram.
    :return: Объект клавиатуры с кнопками для удаления каждого события.
    """
    # Получение всех событий пользователя, доступных для удаления, из базы данных
    all_events = await rq.get_remove_events(user_id)
    
    # Создание билдера для инлайн-клавиатуры
    keyboard = InlineKeyboardBuilder()
    
    # Добавление кнопки для каждого события, которое можно удалить
    for event in all_events:
        keyboard.add(
            InlineKeyboardButton(
                text=event.message,                        # Текст кнопки - описание события
                callback_data=f"remove_{event.id}"         # Данные callback для идентификации события для удаления
            )
        )
    
    # Настройка количества кнопок в каждой строке и преобразование в разметку
    return keyboard.adjust(2).as_markup()

async def event():
    """
    Асинхронная функция для создания инлайн-клавиатуры с деталями конкретного события.
    
    **Примечание:** Данная функция, как представляется, содержит ошибку,
    так как не принимает параметров и пытается обратиться к `event.id`,
    который не определен в этой области видимости.
    
    :return: Объект клавиатуры с кнопками для выбранного события.
    """
    # Получение всех событий (вероятно, ошибка, так как `event` не определен)
    all_events = await rq.get_event(event.id)
    
    # Создание билдера для инлайн-клавиатуры
    keyboard = InlineKeyboardBuilder()
    
    # Добавление кнопки для каждого события
    for event in all_events:
        keyboard.add(
            InlineKeyboardButton(
                text=event.message,                        # Текст кнопки - описание события
                callback_data=f"event_{event.id}"          # Данные callback для идентификации события
            )
        )
    
    # Настройка количества кнопок в каждой строке и преобразование в разметку
    return keyboard.adjust(2).as_markup()
