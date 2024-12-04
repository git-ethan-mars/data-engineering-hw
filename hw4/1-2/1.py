import pickle
import json
from hw4.common import connect_to_db


def read_pickle():
    with open("item.pkl", "rb") as f:
        data = pickle.load(f)
        items = []
        for row in data:
            item = {
                "id": row["id"],
                "name": row["name"],
                "city": row["city"],
                "begin": row["begin"],
                "system": row["system"],
                "tours_count": int(row["tours_count"]),
                "min_rating": int(row["min_rating"]),
                "time_on_game": int(row["time_on_game"])}
            items.append(item)
        return items


def create_tournament_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE tournament (id integer primary key,
            name text,
            city text,
            begin text,
            system text,
            tours_count integer,
            min_rating integer,
            time_on_game integer)
    """)


def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""INSERT INTO tournament (id, name, city, begin, system, tours_count, min_rating, time_on_game)
                        VALUES (:id, :name, :city, :begin, :system, :tours_count, :min_rating, :time_on_game)""", items)
    db.commit()


def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
    SELECT * 
        FROM tournament
        ORDER BY min_rating
        LIMIT 25 
    """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("first_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)


def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(tours_count) as sum_tours_count,
            MAX(tours_count) as max_tours_count,
            MIN(tours_count) as min_tours_count,
            ROUND(AVG(tours_count), 3) as avg_tours_count 
        FROM tournament
    """)
    return res.fetchone()


def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT 
                system, COUNT(*) as count 
            FROM tournament
            GROUP BY system
        """)
    items = []
    for row in res.fetchall():
        items.append(row)
    return items


def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT *
            FROM tournament
            WHERE min_rating < 2300
            ORDER BY min_rating DESC
            LIMIT 25
        """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("fourth_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)


def main():
    # STEP 1
    db = connect_to_db("first.db")
    create_tournament_table(db)
    # STEP 2
    items = read_pickle()
    insert_data(db, items)
    first_query(db)
    print(second_query(db))
    print(third_query(db))
    fourth_query(db)


if __name__ == '__main__':
    main()
