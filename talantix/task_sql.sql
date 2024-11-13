/*
Задание 1:
Выведите все заказы Магазина 1 с расчетом выручки (Цена единицы товара * количество заказанного товара)
Необходимо вывести:
-Название магазина;
-Номенклатура;
-Дата заказа;
-Выручка.
*/

SELECT
    pd.Name_store,
    od.Nomenclature,
    od.Date,
    (od.Price * od.Quantity_product) AS Revenue
FROM
    Orders_directory od
JOIN
    Product_directory pd ON od.Nomenclature = pd.Nomenclature
WHERE
    pd.Name_store = 'Магазин 1';

/*
Задание 2:
Выведите информацию о принтах, которые не используются в Product_dictionary.
Необходимо вывести всю информацию о принтах из Print_directory
*/

SELECT
    pd.Print,
    pd.Name_print_1,
    pd.Name_print_2
FROM
    Print_directory pd
LEFT JOIN
    Product_directory p ON pd.Print = p.Print
WHERE
    p.Print IS NULL;

/*
Задание 3:
Выведите все номенклатуры, у которых есть оба названия принта.
Необходимо вывести:
-Номенклатура;
-Артикул принта;
-Название принта.
*/

SELECT
    pd.Nomenclature,
    p.Print,
    p.Name_print_1,
    p.Name_print_2
FROM
    Product_directory pd
JOIN
    Print_directory p ON pd.Print = p.Print
WHERE
    p.Name_print_1 IS NOT NULL AND p.Name_print_2 IS NOT NULL;

/*
Задание 4:
Выведите информацию по товарам, у которых есть остатки на «Складе 1» на последнюю доступную дату в таблице остатков.
Необходимо вывести:
-Название магазина;
-Номенклатуру;
-Название склада;
-Количество остатков.
*/

SELECT
    pd.Name_store,
    sd.Nomenclature,
    sd.Warehouse,
    sd.Value_stocks
FROM
    Stocks_directory sd
JOIN
    Product_directory pd ON sd.Nomenclature = pd.Nomenclature
WHERE
    sd.Warehouse = 'Склад 1' AND
    sd.Date = (SELECT MAX(Date) FROM Stocks_directory);

/*
Задание 5:
Выведите количество заказов за каждую дату (где они есть), выручку, прибыль с учетом налога для магазинов 5% с выручки для товаров со штрихкодом Code_1.
Необходимо вывести:
-Штрихкод товара;
-Дата;
-Количество заказов;
-Выручка;
-Прибыль с учетом налога.
*/

-- Вариант 1: Компактный запрос, но считаем SUM(od.Price * od.Quantity_product) дважды
SELECT
    pd.Barcode,
    od.Date,
    COUNT(od.Nomenclature) AS Number_of_orders,
    SUM(od.Price * od.Quantity_product) AS Revenue,
    SUM((od.Price * od.Quantity_product) * (1 - 0.05)) AS Profit
FROM
    Orders_directory od
JOIN
    Product_directory pd ON od.Nomenclature = pd.Nomenclature
WHERE
    pd.Barcode = 'Code_1'
GROUP BY
    pd.Barcode, od.Date;

-- Вариант 2: зададим отдельную таблицу RevenueData, чтобы не считать SUM(od.Price * od.Quantity_product) дважды!
WITH RevenueData AS (
    SELECT
        pd.Barcode,
        od.Date,
        COUNT(od.Nomenclature) AS Number_of_orders,
        SUM(od.Price * od.Quantity_product) AS Revenue
    FROM
        Orders_directory od
    JOIN
        Product_directory pd ON od.Nomenclature = pd.Nomenclature
    WHERE
        pd.Barcode = 'Code_1'
    GROUP BY
        pd.Barcode, od.Date
)
SELECT
    Barcode,
    Date,
    Number_of_orders,
    Revenue,
    Revenue * (1 - 0.05) AS Profit
FROM
    RevenueData;

/*
Задание 6:
Выведите самый продаваемый принт с количеством продаж.
Необходимо вывести:
-Артикул принта;
-Название принта №1;
-Количество продаж.
*/

SELECT
    p.Print,
    p.Name_print_1,
    SUM(od.Quantity_product) AS Total_sales
FROM
    Orders_directory od
JOIN
    Product_directory pd ON od.Nomenclature = pd.Nomenclature
JOIN
    Print_directory p ON pd.Print = p.Print
GROUP BY
    p.Print, p.Name_print_1
ORDER BY
    Total_sales DESC
LIMIT 1;