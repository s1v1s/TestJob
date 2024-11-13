# sql_queries.py
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT,
    price REAL,
    timestamp INTEGER
)
"""

INSERT_PRICE = """
INSERT INTO prices (ticker, price, timestamp)
VALUES (?, ?, ?)
"""

SELECT_PRICES = """
SELECT ticker, price, timestamp
FROM prices
WHERE ticker = ?
"""

SELECT_LATEST_PRICE = """
SELECT ticker, price, timestamp
FROM prices
WHERE ticker = ?
ORDER BY timestamp DESC
LIMIT 1
"""

SELECT_PRICE_BY_DATE = """
SELECT ticker, price, timestamp
FROM prices
WHERE ticker = ? AND timestamp
BETWEEN ? AND ?
"""
