import csv
import json
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_to_db(filename) -> sqlite3.dbapi2.Connection:
    connection = sqlite3.connect(filename)
    connection.row_factory = dict_factory
    return connection


def create_product_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            id integer primary key,
            name text,
            price float,
            quantity integer,
            category text,
            fromCity text,
            isAvailable boolean,
            views integer,
            version integer default 0)
    """)


def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""INSERT INTO product (name, price, quantity, category, fromCity, isAvailable, views)
                        VALUES (:name, :price, :quantity, :category, :fromCity, :isAvailable, :views)""", items)
    db.commit()


def read_csv():
    with open("_product_data.csv", "r", encoding="utf-8", newline="\n") as file:
        items = []
        data = csv.reader(file, delimiter=";")
        columns = next(data)
        columns.insert(3, "category")
        for row in data:
            item = dict()
            item["name"] = row[0]
            item["price"] = float(row[1])
            item["quantity"] = int(row[2])
            if len(columns) == len(row):
                item["category"] = row[3]
                item["fromCity"] = row[4]
                item["isAvailable"] = bool(row[5])
                item["views"] = int(row[6])
            else:
                item["category"] = None
                item["fromCity"] = row[3]
                item["isAvailable"] = bool(row[4])
                item["views"] = int(row[5])
            items.append(item)
        return items


def read_updates():
    with open("_update_data.text", "r", encoding="utf-8") as file:
        items = []
        item = dict()
        for line in file:
            if line == "=====\n":
                items.append(item)
                item = dict()
            else:
                pair = line.strip().split("::")
                item[pair[0]] = pair[1]
        return items


def handle_update_operation(db, name, operation, optional_parameter):
    if operation.startswith("quantity"):
        handle_quantity(db, name, optional_parameter)
    elif operation == "price_abs":
        handle_price_abs(db, name, optional_parameter)
    elif operation == "available":
        handle_available(db, name, optional_parameter)
    elif operation == "remove":
        handle_remove(db, name)
    elif operation == "price_percent":
        handle_price_percent(db, name, optional_parameter)


def handle_remove(db, name):
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM product WHERE name = ?", [name])
    db.commit()


def handle_price_percent(db, name, parameter):
    cursor = db.cursor()
    cursor.execute(
        f"UPDATE product SET price = price * (1 + ?), version = version + 1 WHERE name = ?", [float(parameter), name])
    db.commit()


def handle_price_abs(db, name, parameter):
    cursor = db.cursor()
    cursor.execute(
        f"UPDATE product SET price = price + ?, version = version + 1 WHERE name = ?", [float(parameter), name])
    db.commit()


def handle_quantity(db, name, parameter):
    cursor = db.cursor()
    cursor.execute(
        f"UPDATE product SET quantity = quantity + ?, version = version + 1 WHERE name = ?", [int(parameter), name])
    db.commit()


def handle_available(db, name, parameter):
    cursor = db.cursor()
    cursor.execute(
        f"UPDATE product SET isAvailable = ?, version = version + 1 WHERE name = ?", [bool(parameter), name])
    db.commit()


def read_text():
    with open("_part_2.text", "r", encoding="utf-8") as file:
        items = []
        item = dict()
        for line in file:
            if line == "=====\n":
                items.append(item)
                item = dict()
            else:
                pair = line.strip().split("::")
                if pair[0] in ['instrumentalness', 'explicit', 'loudness']:
                    continue
                item[pair[0]] = pair[1]
        return items


def apply_updates(db, items):
    for item in items:
        handle_update_operation(db, item["name"], item["method"], item["param"])


def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM product
        ORDER BY version DESC
        LIMIT 10
    """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("first_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)


def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT category, SUM(quantity) as products_amount, SUM(price) as sum_price, MAX(price) as max_price, MIN(price) as min_price,
            AVG(price) as avg_price
        FROM product
        WHERE category != ('null')
        GROUP BY category
    """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("second_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)


def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT category, SUM(quantity) as sum_quantity, MAX(quantity) as max_quantity, 
            MIN(quantity) as min_quantity, AVG(quantity) as avg_quantity
        FROM product
        WHERE category != ('null')
        GROUP BY category
    """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("third_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)


def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT name, fromCity, MIN(views) as max_views
        FROM product
        WHERE category == "fruit"
    """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("fourth_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)


def main():
    db = connect_to_db("third.db")
    create_product_table(db)
    items = read_csv()
    insert_data(db, items)
    updates = read_updates()
    apply_updates(db, updates)
    first_query(db)
    second_query(db)
    third_query(db)
    fourth_query(db)


if __name__ == '__main__':
    main()
