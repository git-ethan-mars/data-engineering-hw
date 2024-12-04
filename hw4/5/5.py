import csv
import json
import sqlite3


def read_csv():
    with open("Pokemon.csv", "r") as file:
        rows = csv.reader(file)
        columns = next(rows)
        items = []
        for row in rows:
            item = dict()
            for i in range(len(row)):
                item[columns[i]] = row[i]
            items.append(item)
        return items


def create_pokemon_table(db):
    cursor = db.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS pokemons (
                pokemon_id integer,
                name text,
                type_1 text,
                type_2 text,
                generation integer,
                legendary boolean)
            """)


def create_modifiers_table(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS modifiers 
            (name text references pokemons(name),
            sp_attack integer,
            sp_defense integer)""")


def create_stats_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            name text references pokemons(name),
            hp integer,
            attack integer,
            defense integer,
            speed integer        
        )
        """)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_to_db(filename) -> sqlite3.dbapi2.Connection:
    connection = sqlite3.connect(filename)
    connection.row_factory = dict_factory
    return connection


def insert_data(db, items):
    pokemons = []
    modifiers = []
    stats = []
    for item in items:
        pokemons.append(
            {"pokemon_id": int(item["#"]), "name": item["Name"], "type_1": item["Type 1"], "type_2": item["Type 2"],
             "generation": int(item["Generation"]), "legendary": bool(item["Legendary"])})
        modifiers.append({"name": item["Name"], "sp_attack": int(item["Sp. Atk"]), "sp_defense": int(item["Sp. Def"])})
        stats.append({"name": item["Name"], "hp": int(item["HP"]), "attack": int(item["Attack"]),
                      "defense": int(item["Defense"]),
                      "speed": int(item["Speed"])})
    cursor = db.cursor()
    cursor.executemany("""INSERT INTO pokemons (pokemon_id, name, type_1, type_2, generation, legendary)
                                VALUES (:pokemon_id, :name, :type_1, :type_2, :generation, :legendary)""", pokemons)
    cursor.executemany("""INSERT INTO modifiers (name, sp_attack, sp_defense)
                                    VALUES (:name, :sp_attack, :sp_defense)""", modifiers)
    cursor.executemany("""INSERT INTO stats (name, hp, attack, defense, speed)
                                    VALUES (:name, :hp, :attack, :defense, :speed)""", stats)
    db.commit()


def first_query(db):
    cursor = db.cursor()
    res = cursor.execute(
        """SELECT p.name, MAX(m.sp_attack + m.sp_defense + s.attack + s.defense + s.speed) as max_stats FROM pokemons p 
        JOIN stats s ON p.name == s.name 
        JOIN modifiers m ON p.name == m.name""")
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("first_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4)

def second_query(db):
    cursor = db.cursor()
    res = cursor.execute(
        """SELECT * FROM pokemons p 
        JOIN stats s ON p.name == s.name 
        WHERE p.type_1 == "Electric"
        ORDER BY s.hp DESC
        LIMIT 20""")
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("second_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4)

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute(
        """SELECT p.type_1, COUNT(*) as pokemon_count FROM pokemons p 
        GROUP BY p.type_1""")
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("third_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4)

def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute(
        """SELECT * FROM pokemons p
        JOIN stats s ON p.name = s.name 
        WHERE p.generation > 1 and p.legendary == True and s.attack > 170
        ORDER BY s.attack DESC
        """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("fourth_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4)

def fifth_query(db):
    cursor = db.cursor()
    res = cursor.execute(
        """SELECT p.type_1, AVG(m.sp_attack) as average_special_attack, AVG(m.sp_defense) as average_special_defense
            FROM pokemons p
            JOIN modifiers m ON p.name = m.name
            GROUP BY p.type_1
        """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("fifth_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4)

def sixth_query(db):
    cursor = db.cursor()
    res = cursor.execute(
        """SELECT s.name, p.type_2, MAX(s.speed) as max_speed
            FROM stats s
            JOIN pokemons p ON p.name == s.name
            GROUP BY p.type_2
        """)
    items = []
    for row in res.fetchall():
        items.append(row)
    with open("sixth_query.json", "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4)

# Предметная область = покемоны
def main():
    db = connect_to_db("fourth.db")
    create_pokemon_table(db)
    create_modifiers_table(db)
    create_stats_table(db)
    items = read_csv()
    insert_data(db, items)
    first_query(db)
    second_query(db)
    third_query(db)
    fourth_query(db)
    fifth_query(db)
    sixth_query(db)

if __name__ == '__main__':
    main()
