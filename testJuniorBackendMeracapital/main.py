import asyncio
from contextlib import asynccontextmanager
from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query

from config import DB_PATH
from src.data.db import Database
from src.enums.error_enums import ErrorMessages
from src.fetcher import PriceFetcher
from src.models.prices_model import PriceData


async def get_database():
    database = Database(DB_PATH)
    await database.connect()
    try:
        yield database
    finally:
        await database.close()


# Обработчик жизненного цикла приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация базы данных и запуск задачи получения цен."""
    # База данных SQlite
    database = Database(DB_PATH)
    await database.connect()
    # Сборщик цен
    fetcher = PriceFetcher(database)
    task = asyncio.create_task(fetcher.fetch_and_store_prices())

    yield  # Здесь приложение работает

    task.cancel()  # Завершаем задачу при остановке приложения
    await database.close()  # Закрываем соединение с базой данных
    await task  # Ждем завершения задачи


app = FastAPI(lifespan=lifespan)


@app.get("/prices", response_model=List[PriceData])
async def get_all_prices(
    ticker: str = Query(...), database: Database = Depends(get_database)
) -> List[PriceData]:
    """Получает все сохраненные данные по указанной валюте."""
    prices = await database.get_prices(ticker)
    if not prices:
        raise HTTPException(status_code=404, detail=ErrorMessages.DATA_NOT_FOUND.value)
    return prices


@app.get("/prices/latest", response_model=PriceData)
async def get_latest_price(
    ticker: str = Query(...), database: Database = Depends(get_database)
) -> PriceData:
    """Получает последнюю цену валюты."""
    latest_price = await database.get_latest_price(ticker)
    if not latest_price:
        raise HTTPException(status_code=404, detail=ErrorMessages.DATA_NOT_FOUND.value)
    return latest_price


@app.get("/prices/filter", response_model=List[PriceData])
async def get_price_by_date(
    ticker: str = Query(...),
    start: int = Query(...),
    end: int = Query(...),
    database: Database = Depends(get_database),
) -> List[PriceData]:
    """Получает цены валюты с фильтром по дате."""
    prices_by_date = await database.get_prices_by_date(ticker, start, end)
    if not prices_by_date:
        raise HTTPException(status_code=404, detail=ErrorMessages.DATA_NOT_FOUND.value)
    return prices_by_date


# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
