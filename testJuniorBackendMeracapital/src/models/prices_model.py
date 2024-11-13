from pydantic import BaseModel


class PriceData(BaseModel):
    """Модель для представления данных о цене."""

    ticker: str
    price: float
    timestamp: int
