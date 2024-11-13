# error_messages.py
from enum import Enum


class ErrorMessages(Enum):
    DATA_NOT_FOUND = "Данные не найдены"
    INVALID_TICKER = "Неверный тикер"
    APPLICATION_SHUTTING_DOWN = "Приложение завершает работу, отмена задач..."
    TASK_CANCELLED = "Задачи были отменены во время завершения."
    TASK_FETCH_STORE_CANCELLED = "Задача получения цен и записи в БД отменена"
    DATABASE_ERROR = "Ошибка базы данных"
    DATABASE_CLOSED = "Соединение с базой данных закрыто."
