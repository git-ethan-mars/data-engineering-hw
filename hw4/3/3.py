import json
import pickle
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

def create_track_table(db):
    cursor = db.cursor()
    # artist, song, year, duration_ms, tempo, genre
    cursor.execute("""
        CREATE TABLE track (id integer primary key,
            artist text,
            song text,
            duration_ms float,
            year integer,
            tempo float,
            genre text)
    """)

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""INSERT INTO track (artist, song, duration_ms, year, tempo, genre)
                        VALUES (:artist, :song, :duration_ms, :year, :tempo, :genre)""", items)
    db.commit()

def read_pickle():
    with open("_part_1.pkl", "rb") as file:
        items = pickle.load(file, encoding="utf-8")
        for item in items:
            del item["acousticness"]
            del item["energy"]
            del item["popularity"]
        return items


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

def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT artist, song, year
        FROM track
        ORDER BY year DESC
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
        SELECT SUM(duration_ms), MAX(duration_ms), MIN(duration_ms), AVG(duration_ms)
        FROM track
    """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("second_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT artist, COUNT(*) as track_count
        FROM track
        GROUP BY artist
        ORDER BY track_count DESC
    """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("third_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)

def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT artist, song, year
        FROM track
        WHERE artist == "Rihanna"
        ORDER BY year
        LIMIT 25
    """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("fourth_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)

def main():
    pickle_items = read_pickle()
    text_items = read_text()
    db = connect_to_db("second.db")
    create_track_table(db)
    insert_data(db, pickle_items)
    insert_data(db, text_items)
    first_query(db)
    second_query(db)
    third_query(db)
    fourth_query(db)


if __name__ == '__main__':
    main()