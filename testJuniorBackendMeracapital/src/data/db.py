import aiosqlite

from config import DB_PATH
from sql_queries import (
    CREATE_TABLE,
    INSERT_PRICE,
    SELECT_LATEST_PRICE,
    SELECT_PRICE_BY_DATE,
    SELECT_PRICES,
)
from src.enums.error_enums import ErrorMessages
from src.models.prices_model import PriceData


class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.connection = None

    async def connect(self):
        """Инициализирует подключение к базе данных и создает таблицу, если она не существует."""
        if not self.connection:
            self.connection = await aiosqlite.connect(self.db_path)
            await self.connection.execute(CREATE_TABLE)
            await self.connection.commit()
            print("Подключение к базе данных открыто")

    async def close(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            await self.connection.close()
            print("Подключение к базе данных закрыто")

    async def save_price(self, price_data: PriceData):
        """Сохраняет данные о цене в базу данных."""
        try:
            await self.connection.execute(
                INSERT_PRICE,
                (price_data.ticker, price_data.price, price_data.timestamp),
            )
            await self.connection.commit()
        except Exception as e:
            raise Exception(f"{ErrorMessages.DATABASE_ERROR.value}: {str(e)}") from e

    async def get_prices(self, ticker: str):
        """Возвращает все записи с указанным тикером."""
        cursor = await self.connection.execute(SELECT_PRICES, (ticker,))
        rows = await cursor.fetchall()
        if not rows:
            raise Exception(ErrorMessages.DATA_NOT_FOUND.value)
        return [
            PriceData(ticker=row[0], price=row[1], timestamp=row[2]) for row in rows
        ]

    async def get_latest_price(self, ticker: str):
        """Возвращает последнюю запись с указанным тикером."""
        cursor = await self.connection.execute(SELECT_LATEST_PRICE, (ticker,))
        row = await cursor.fetchone()
        if row is None:
            raise Exception(ErrorMessages.DATA_NOT_FOUND.value)
        return PriceData(ticker=row[0], price=row[1], timestamp=row[2])

    async def get_prices_by_date(self, ticker: str, start: int, end: int):
        """Возвращает записи с указанным тикером, отфильтрованные по дате."""
        cursor = await self.connection.execute(
            SELECT_PRICE_BY_DATE, (ticker, start, end)
        )
        rows = await cursor.fetchall()
        if not rows:
            raise Exception(ErrorMessages.DATA_NOT_FOUND.value)
        return [
            PriceData(ticker=row[0], price=row[1], timestamp=row[2]) for row in rows
        ]
