import aiohttp
import pytest

from src.enums.error_enums import ErrorMessages
from src.models.prices_model import PriceData


@pytest.mark.asyncio
@pytest.mark.parametrize("ticker", ["btc_usd", "eth_usd"])
async def test_fetch_price(price_fetcher, ticker):
    """Тестирует получение цены для различных валютных пар."""
    async with aiohttp.ClientSession() as session:
        price_data = await price_fetcher.fetch_price(session, ticker)
        assert price_data is not None
        assert price_data.ticker == ticker
        assert price_data.price > 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_price_data",
    [
        PriceData(ticker="btc_usd", price=10000, timestamp=1234567890),
        PriceData(ticker="eth_usd", price=2000, timestamp=1234567891),
        PriceData(ticker="btc_usd", price=500, timestamp=1234567892),
    ],
)
async def test_save_price(setup_database, test_price_data):
    """Тестирует сохранение цены в базу данных для разных валют."""
    await setup_database.save_price(test_price_data)

    # Проверяем, что цена сохранена в базе данных
    prices = await setup_database.get_prices(test_price_data.ticker)
    assert len(prices) == 1
    assert prices[0].ticker == test_price_data.ticker
    assert prices[0].price == test_price_data.price


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ticker, price",
    [
        ("eth_usd", 2000),
        ("btc_usd", 500),
        ("btc_usd", 0.5),
    ],
)
async def test_get_all_prices(setup_database, ticker, price):
    """Тестирует получение всех сохраненных данных по валюте для разных тикеров."""
    await setup_database.save_price(
        PriceData(ticker=ticker, price=price, timestamp=1234567890)
    )
    prices = await setup_database.get_prices(ticker)
    assert len(prices) > 0
    assert prices[0].ticker == ticker


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ticker1, ticker2, price1, price2",
    [
        ("btc_usd", "eth_usd", 10000, 10100),
        ("btc_usd", "eth_usd", 500, 520),
    ],
)
async def test_get_latest_price(setup_database, ticker1, ticker2, price1, price2):
    """Тестирует получение последней цены валюты для различных пар цен."""
    await setup_database.save_price(
        PriceData(ticker=ticker1, price=price1, timestamp=1234567890)
    )
    await setup_database.save_price(
        PriceData(ticker=ticker1, price=price2, timestamp=1234567891)
    )

    # Проверяем, что последняя цена возвращается корректно
    latest_price = await setup_database.get_latest_price(ticker1)
    assert latest_price.price == price2, f"Последняя цена должна быть {price2}"
    assert (
        latest_price.timestamp == 1234567891
    ), "Временная метка должна соответствовать последней записи"

    # Проверяем, что функция возвращает ошибку, если данные отсутствуют
    with pytest.raises(Exception, match=ErrorMessages.DATA_NOT_FOUND.value):
        await setup_database.get_latest_price(ticker2)  # Тикер, для которого нет данных


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "price_data1, price_data2, price_data3",
    [
        (
            PriceData(ticker="btc_usd", price=10000, timestamp=1234567890),
            PriceData(ticker="btc_usd", price=10100, timestamp=1234567891),
            PriceData(ticker="btc_usd", price=10200, timestamp=1234567892),
        ),
        (
            PriceData(ticker="eth_usd", price=10000, timestamp=1234567890),
            PriceData(ticker="eth_usd", price=10100, timestamp=1234567891),
            PriceData(ticker="eth_usd", price=10200, timestamp=1234567892),
        ),
    ],
)
async def test_get_prices_by_date(
    setup_database, price_data1, price_data2, price_data3
):
    """Тест для получения записей по тикеру и диапазону дат."""
    # Сохраняем несколько цен для одного тикера с разными временными метками
    await setup_database.save_price(price_data1)
    await setup_database.save_price(price_data2)
    await setup_database.save_price(price_data3)

    # Получаем цены в диапазоне дат, включая первую и вторую запись
    prices_in_range = await setup_database.get_prices_by_date(
        price_data1.ticker,
        price_data1.timestamp,
        price_data2.timestamp,
    )
    assert len(prices_in_range) == 2, "Должно быть возвращено 2 записи в диапазоне"
    assert (
        prices_in_range[0].price == price_data1.price
    ), f"Первая цена должна быть {price_data1.price}"
    assert (
        prices_in_range[1].price == price_data2.price
    ), f"Вторая цена должна быть {price_data2.price}"

    # Проверяем, что функция возвращает ошибку, если в диапазоне нет данных
    with pytest.raises(Exception, match=ErrorMessages.DATA_NOT_FOUND.value):
        await setup_database.get_prices_by_date(
            "btc_usd", 1234567800, 1234567801
        )  # Диапазон без записей
