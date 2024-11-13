import os

import pytest_asyncio

from config import TEST_DB_PATH
from src.data.db import Database
from src.fetcher import PriceFetcher


@pytest_asyncio.fixture(scope="function")
async def setup_database():
    """Fixture для настройки тестовой базы данных."""
    database = Database(TEST_DB_PATH)
    await database.connect()
    yield database
    # Закрываем соединение и удаляем базу данных после завершения тестов
    await database.close()
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@pytest_asyncio.fixture(scope="function")
async def price_fetcher(setup_database):
    """Fixture для создания экземпляра PriceFetcher."""
    return PriceFetcher(setup_database)
