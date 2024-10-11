Wildberries Reminder Bot

Полнофункциональный Telegram-бот, созданный с использованием Aiogram, SQLAlchemy и APScheduler, который помогает пользователям настраивать и управлять напоминаниями эффективно. Этот бот позволяет пользователям создавать, просматривать и удалять события с настраиваемыми интервалами и уведомлениями.
Содержание

    Особенности
    Предварительные требования
    Установка
    Конфигурация
    Использование
    Структура проекта
    Зависимости
    Запуск бота
    Тестирование
    Вклад
    Лицензия

Особенности

    Управление пользователями: Автоматическая регистрация пользователей на основе их Telegram ID.
    Планирование событий: Позволяет пользователям создавать события с конкретными датами, интервалами и сообщениями напоминаний.
    Управление событиями: Пользователи могут просматривать все свои события и удалять ненужные.
    Асинхронные операции: Использует асинхронное программирование для эффективной работы.
    Постоянное хранилище: Сохраняет данные пользователей и событий в базе данных SQLite.
    Интеграция с планировщиком: Использует APScheduler для обработки напоминаний и уведомлений о событиях.

Предварительные требования

    Python 3.10+: Убедитесь, что Python установлен. Скачать можно с python.org.
    Аккаунт Telegram: Необходим для взаимодействия с ботом.
    Токен бота: Получите токен бота, создав нового бота через BotFather в Telegram.

Установка

    Клонируйте репозиторий

    bash

git clone https://github.com/yourusername/wildberries-reminder-bot.git
cd wildberries-reminder-bot

Создайте виртуальное окружение

Рекомендуется использовать виртуальное окружение для управления зависимостями.

bash

python -m venv venv
source venv/bin/activate  # В Windows используйте `venv\Scripts\activate`

Установите зависимости

bash

    pip install -r requirements.txt

Конфигурация

    Переменные окружения

    Создайте файл .env в корневом каталоге проекта и добавьте токен вашего Telegram-бота:

    env

    BOT_TOKEN=your_telegram_bot_token_here

    Настройка базы данных

    Бот использует SQLite для простоты. Файл базы данных (db.sqlite3) будет автоматически создан в каталоге проекта при первом запуске бота.

Использование

    Запустите бота

    bash

    python wildberriesbot/bot.py

    Взаимодействие с ботом
        /start или /help: Зарегистрируйтесь в боте и получите инструкции.
        Установить событие: Следуйте инструкциям для настройки нового напоминания.
        Просмотреть события: Используйте кнопку "События" для просмотра всех ваших событий.
        Удалить события: Используйте кнопку "Удалить" для удаления ненужных событий.

Структура проекта

markdown

wildberries-reminder-bot/
├── db.sqlite3
├── poetry.lock
├── pyproject.toml
├── README.md
├── requirements.txt
├── tests
│   └── __init__.py
└── wildberriesbot
    ├── bot.py
    ├── database
    │   ├── models.py
    │   ├── __pycache__
    │   │   ├── models.cpython-312.pyc
    │   │   └── requests.cpython-312.pyc
    │   └── requests.py
    ├── handlers
    │   ├── event_notice.py
    │   ├── handler_scheduler.py
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── event_notice.cpython-312.pyc
    │   │   ├── handler_scheduler.cpython-312.pyc
    │   │   ├── __init__.cpython-312.pyc
    │   │   └── start.cpython-312.pyc
    │   └── start.py
    ├── __init__.py
    ├── keyboards
    │   ├── keyboards.py
    │   └── __pycache__
    │       └── keyboards.cpython-312.pyc
    └── middlewares
        ├── __init__.py
        ├── __pycache__
        │   ├── __init__.cpython-312.pyc
        │   └── scheduler.cpython-312.pyc
        └── scheduler.py

Описание

    db.sqlite3: Файл базы данных SQLite, хранящий данные пользователей и событий.
    poetry.lock & pyproject.toml: Файлы управления зависимостями (если используется Poetry).
    requirements.txt: Список зависимостей Python.
    tests/: Каталог для тестовых случаев.
    wildberriesbot/: Основной пакет, содержащий исходный код бота.
        bot.py: Точка входа приложения.
        database/: Содержит модели SQLAlchemy и скрипты для работы с базой данных.
            models.py: Определяет ORM-модели (User, Event).
            requests.py: Асинхронные функции для взаимодействия с базой данных.
        handlers/: Содержит обработчики различных команд и колбэков бота.
            start.py: Обрабатывает команды /start и /help.
            handler_scheduler.py: Управляет созданием, просмотром и удалением событий.
            event_notice.py: Обрабатывает логику уведомлений о событиях.
        keyboards/: Определяет макеты клавиатур для взаимодействия с пользователем.
            keyboards.py: Создает кнопки Reply и Inline клавиатур.
        middlewares/: Содержит промежуточные слои для интеграции планировщика.
            scheduler.py: Промежуточный слой для внедрения планировщика в обработчики.

Зависимости

Проект использует следующие основные библиотеки:

    Aiogram: Асинхронный фреймворк для Telegram Bot API.
    SQLAlchemy: SQL-инструментарий и ORM для Python.
    aiosqlite: Асинхронный интерфейс для SQLite.
    APScheduler: Расширенный планировщик задач для Python.
    python-dotenv: Читает пары ключ-значение из файла .env и может устанавливать их как переменные окружения.

Полный список зависимостей:

plaintext

aio-pika==9.4.3 ; python_version >= "3.12" and python_version < "4.0"
aiofiles==24.1.0 ; python_version >= "3.12" and python_version < "4.0"
aiogram==3.13.1 ; python_version >= "3.12" and python_version < "4.0"
aiohappyeyeballs==2.4.3 ; python_version >= "3.12" and python_version < "4.0"
aiohttp==3.10.9 ; python_version >= "3.12" and python_version < "4.0"
aiormq==6.8.1 ; python_version >= "3.12" and python_version < "4.0"
aiosignal==1.3.1 ; python_version >= "3.12" and python_version < "4.0"
annotated-types==0.7.0 ; python_version >= "3.12" and python_version < "4.0"
apscheduler==3.10.4 ; python_version >= "3.12" and python_version < "4.0"
attrs==24.2.0 ; python_version >= "3.12" and python_version < "4.0"
certifi==2024.8.30 ; python_version >= "3.12" and python_version < "4.0"
frozenlist==1.4.1 ; python_version >= "3.12" and python_version < "4.0"
idna==3.10 ; python_version >= "3.12" and python_version < "4.0"
magic-filter==1.0.12 ; python_version >= "3.12" and python_version < "4.0"
multidict==6.1.0 ; python_version >= "3.12" and python_version < "4.0"
pamqp==3.3.0 ; python_version >= "3.12" and python_version < "4.0"
pydantic-core==2.23.4 ; python_version >= "3.12" and python_version < "4.0"
pydantic==2.9.2 ; python_version >= "3.12" and python_version < "4.0"
pytz==2024.2 ; python_version >= "3.12" and python_version < "4.0"
six==1.16.0 ; python_version >= "3.12" and python_version < "4.0"
typing-extensions==4.12.2 ; python_version >= "3.12" and python_version < "4.0"
tzdata==2024.2 ; python_version >= "3.12" and python_version < "4.0" and platform_system == "Windows"
tzlocal==5.2 ; python_version >= "3.12" and python_version < "4.0"
yarl==1.13.1 ; python_version >= "3.12" and python_version < "4.0"

Примечание: Данные зависимости содержат условия, которые определяют, при каких версиях Python они устанавливаются. Также некоторые зависимости зависят от операционной системы.
Создание файла requirements.txt


Важно: Убедитесь, что ваш файл .gitignore содержит строку .env, чтобы предотвратить случайное добавление чувствительных данных в систему контроля версий.
Запуск бота

    Активируйте виртуальное окружение

    bash

source venv/bin/activate  # В Windows используйте `venv\Scripts\activate`

Запустите бота

bash

    python wildberriesbot/bot.py

    Бот инициализирует базу данных, настроит планировщик и начнет опрашивать обновления.

    Взаимодействие с ботом
        Старт/Помощь: Отправьте /start или /help для получения инструкций.
        Установить напоминание: Следуйте подсказкам для создания нового события с конкретной датой, интервалом и сообщением.
        Просмотреть события: Используйте кнопку "События" для просмотра всех текущих событий.
        Удалить события: Используйте кнопку "Удалить" для удаления существующих событий.

Тестирование

Для запуска тестов перейдите в корневой каталог проекта и выполните:

bash

pytest

Убедитесь, что pytest установлен:

bash

pip install pytest

Структура рабочего процесса проекта

    Модели базы данных (wildberriesbot/database/models.py)
        User: Представляет пользователя Telegram с уникальным tg_id.
        Event: Представляет событие с датой, интервалом, сообщением и внешним ключом, связывающимся с User.

    Операции с базой данных (wildberriesbot/database/requests.py)

    Асинхронные функции для добавления, получения и удаления пользователей и событий из базы данных.

    Клавиатуры (wildberriesbot/keyboards/keyboards.py)
        Основная клавиатура: Содержит кнопки "События" и "Удалить".
        Inline клавиатуры: Генерируются динамически на основе событий пользователя для просмотра и удаления.

    Обработчики
        Обработчик старта (wildberriesbot/handlers/start.py): Обрабатывает команды /start и /help, регистрирует пользователей и предоставляет инструкции.
        Обработчики планировщика (wildberriesbot/handlers/handler_scheduler.py): Управляют созданием, просмотром и удалением событий, взаимодействуют с планировщиком для напоминаний.
        Уведомления о событиях (wildberriesbot/handlers/event_notice.py): Обрабатывает логику уведомлений пользователей о событиях.

    Промежуточные слои планировщика (wildberriesbot/middlewares/scheduler.py)

    Интегрирует APScheduler для обработки запланированных задач по отправке напоминаний на основе событий пользователей.

    Точка входа бота (wildberriesbot/bot.py)
        Инициализирует базу данных.
        Настраивает промежуточные слои и роутеры.
        Запускает APScheduler.
        Начинает опрашивать обновления Telegram.

Вклад

Вклады приветствуются! Пожалуйста, следуйте этим шагам:

    Форкните репозиторий

    Создайте новую ветку

    bash

git checkout -b feature/YourFeature

Закоммитьте ваши изменения

bash

git commit -m "Add your message here"

Отправьте в ветку

bash

    git push origin feature/YourFeature

    Откройте Pull Request

    Опишите ваши изменения и отправьте Pull Request для рассмотрения.

Лицензия

Этот проект лицензирован под MIT License.