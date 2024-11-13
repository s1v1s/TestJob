import asyncio
import ssl
import time
from typing import Optional

import aiohttp
import certifi

from config import CURRENCIES, DERIBIT_URL
from src.data.db import Database
from src.enums.error_enums import ErrorMessages
from src.models.prices_model import PriceData


class PriceFetcher:
    """Класс для получения и сохранения цен с биржи Deribit."""

    def __init__(self, db: Database):
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.db = db

    async def fetch_price(
        self, session: aiohttp.ClientSession, currency: str
    ) -> Optional[PriceData]:
        """Получает индексную цену указанной валюты."""
        params = {"index_name": currency}
        try:
            async with session.get(
                DERIBIT_URL, params=params, ssl=self.ssl_context
            ) as response:
                response.raise_for_status()  # Проверка статуса ответа
                data = await response.json()
                prices = PriceData(
                    ticker=currency,
                    price=data["result"]["index_price"],
                    timestamp=int(time.time()),
                )
                return prices
        except (aiohttp.ClientError, KeyError) as e:
            print(f"Ошибка при получении цены для {currency}: {e}")
            return None
        finally:
            print(f"Получены цены: {prices}")

    async def fetch_and_store_prices(self):
        """Функция для получения цен и записи в БД каждые 60 секунд."""
        async with aiohttp.ClientSession() as session:
            try:
                while True:
                    tasks = [
                        self.fetch_price(session, currency) for currency in CURRENCIES
                    ]
                    prices = await asyncio.gather(*tasks)

                    for record in prices:
                        if record is not None:
                            await self.db.save_price(record)

                    print(f"Сохранены цены: {prices}")
                    await asyncio.sleep(60)
            except asyncio.CancelledError:
                print(ErrorMessages.TASK_FETCH_STORE_CANCELLED.value)
                raise
