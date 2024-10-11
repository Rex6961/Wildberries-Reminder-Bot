from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.formatting import Text, Bold, as_list, as_marked_section

import database.requests as rq
import keyboards.keyboards as kb


# Создание экземпляра роутера для обработки команд начала
router_start = Router()

@router_start.message(Command(commands=['start', 'help']))
async def cmdStart(message: Message):
    """
    Обработчик команды /start.
    И краткое описание использования бота.
    """

    # Передаем в базу данных id пользователя
    await rq.set_user(message.from_user.id)

    
    # Формирование текста сообщения с инструкциями для пользователя
    text = Text(as_list(
        as_marked_section(
            # Жирный текст с инструкцией по вводу даты напоминания
            Bold("Введите дату напоминания в виде\n'@bot ctrl 1M1w1d1h1m1s 1i' где:"),
            "1M - 1month",    # 1 месяц
            "1w - 1week",     # 1 неделя
            "1d - 1day",      # 1 день
            "1h - 1hour",     # 1 час
            "1m - 1minute",   # 1 минута
            f"1s - 1second\n", # 1 секунда
            marker="✅ "       # Маркер перед каждым пунктом
        ),
        as_marked_section(
            # Жирный текст с инструкцией по вводу количества повторений
            Bold("количество повторений"),
            "1i - 1interval", # 1 интервал
            marker="✅ "        # Маркер перед пунктом
        )
    ))
    
    # Отправка сформированного сообщения пользователю
    await message.answer(**text.as_kwargs(), reply_markup=kb.main)
