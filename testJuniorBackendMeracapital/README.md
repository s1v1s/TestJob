# Crypto Price Fetcher

## Описание

Проект для получения индексных цен BTC/USD и ETH/USD с биржи Deribit и сохранения данных в базу SQLite.

## Установка

1. Клонирование репозитория и переход в папку проекта:

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Создание виртуального окружения

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

Установка зависимостей:

```pip install -r requirements.txt```

или

```pip install fastapi uvicorn aiohttp aiosqlite pydantic certifi pytest pytest-asyncio```

## Запуск

```uvicorn main:app --reload --port 8000```

или

```python main.py```

## Описание эндпоинтов

1. /prices - Получение всех сохраненных данных по указанной валюте
   - Метод: GET
   - Параметры:
      - ticker (обязательный): тикер криптовалюты (например, btc_usd, eth_usd).
   - Ответ: список всех сохранённых цен.

2. /prices/latest - Получение последней цены валюты
   - Метод: GET
   - Параметры:
      - ticker (обязательный): тикер криптовалюты.
   - Ответ: последняя цена для указанной криптовалюты.

3. /prices/filter - Получение цены валюты с фильтром по дате
   - Метод: GET
   - Параметры:
      - ticker (обязательный): тикер криптовалюты.
      - start (обязательный): начальная дата в виде UNIX - timestamp.
      end (обязательный): конечная дата в виде UNIX timestamp.
   - Ответ: список цен, отфильтрованных по дате.

## Примеры запросов

- <localhost:8000/prices?ticker=btc_usd>
- <localhost:8000/prices/latest?ticker=btc_usd>
- <localhost:8000/prices/filter?ticker=btc_usd&start=1&end=123123123321>
- <localhost:8000/docs>

## Тесты pytest

Запуск тестов ```pytest -s -v tests```

## pytest-asyncio

<https://stackoverflow.com/a/73019163>

## TODO/ Основные проблемы

- В реализации клиента не хватает обработки тайм-аута, из за чего есть риск падения программы.
- Неоптимально сохраняются данные в цикле, достаточно одного коммита, а не на каждую итерацию.
- Используется print вместо logging.
- SQL запросы выполняются прямо в обработчиках апи, из за чего есть риск ответа низкоуровневой ошибки БД пользователю.
- Неочевидная архитектура приложения, например почему sql запросы лежат в корне проекта, а роуты АПИ в main?
