import json

from hw4.common import connect_to_db
import csv

def read_csv():
    with open("subitem.csv", encoding="utf-8", newline="\n") as file:
        reader = csv.reader(file, delimiter=";")
        columns = next(reader)
        data = []
        for row in reader:
            entry = dict()
            for i in range(len(row)):
                entry[columns[i]] = row[i]
            data.append(entry)
        return data

def create_prise_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE prise (id integer primary key,
            tournament_name text references tournament(name),
            place integer,
            prise integer)
    """)

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""INSERT INTO prise (tournament_name, place, prise)
                        VALUES (:name, :place, :prise)""", items)
    db.commit()

def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT t.id, t.name, p.prise, p.place
        FROM tournament t
        JOIN prise p ON t.name = p.tournament_name
        WHERE p.place = 0
    """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("first_query_2.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)

def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT p.tournament_name, COUNT(*) as tournament_count
        FROM tournament t
        JOIN prise p ON t.name = p.tournament_name
        GROUP BY t.name
    """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("second_query_2.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT p.tournament_name, MAX(p.prise) as maximum_prise, AVG(t.min_rating) as average_minimum_rating
        FROM tournament t
        JOIN prise p ON t.name = p.tournament_name
        GROUP BY t.name
    """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("third_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)


def main():
    items = read_csv()
    db = connect_to_db("first.db")
    #create_prise_table(db)
    #insert_data(db, items)
    first_query(db)
    second_query(db)
    third_query(db)

if __name__ == '__main__':
    main()