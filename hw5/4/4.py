import json
import csv

import pymongo


def read_json():
    with open("pokemons_part_1.json", "r", encoding="utf-8") as file:
        return json.load(file)


def read_csv():
    with open("pokemons_part_2.csv", encoding="utf-8", newline="\n") as file:
        reader = csv.reader(file, delimiter=",")
        columns = next(reader)
        data = []
        for row in reader:
            entry = dict()
            for i in range(len(row)):
                if row[i].isdigit():
                    row[i] = int(row[i])
                entry[columns[i]] = row[i]
            data.append(entry)
        return data

def drop_id(items):
    for item in items:
        del item["_id"]
    return items


def connect_db():
    client = pymongo.MongoClient()
    db = client["db-2025"]
    return db.pokemons

def insert_data(collection, items):
    collection.insert_many(items)

def save_json(data, filename):
    items = []
    for row in data:
        items.append(row)
    with open(filename, "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)


def sample_first_query(collection):
    data = drop_id(list(collection.find(limit=10).sort({"Total": pymongo.ASCENDING})))
    save_json(data, "sample_first_query.json")


def sample_second_query(collection):
    data = drop_id(list(collection.find({"Attack": {"$lt": 30}}, limit=15).sort({"Total": pymongo.ASCENDING})))
    save_json(data, "sample_second_query.json")


def sample_third_query(collection):
    data = drop_id(list(collection.find(
        {"Type 1": {"$in": ["Grass", "Fire"]}, "Type 2": {"$in": ["Flying", "Poison"]}},
        limit=10).sort({"Total": pymongo.ASCENDING})))
    save_json(data, "sample_third_query.json")


def sample_fourth_query(collection):
    count = collection.count_documents({"HP": {"$gte": 40, "$lte": 100},
                                         "$or": [{"Defense": {"$gt": 30, "$lte": 50}},
                                                 {"Defense": {"$gt": 70, "$lt": 80}}]})
    save_json([{"entry_count" : count}], "sample_fourth_query.json")

def sample_fifth_query(collection):
    count = collection.count_documents({"HP": {"$gte": 40, "$lte": 100},
                                        "$or": [{"Attack": {"$gt": 30, "$lte": 50}},
                                                {"Attack": {"$gt": 70, "$lt": 80}}]})
    save_json([{"entry_count" : count}], "sample_fifth_query.json")

def aggregation_first_query(collection):
    data = collection.aggregate([
        {
            "$group": {
                "_id": "result",
                "max_total": {"$max": "$Total"},
                "min_total": {"$min": "$Total"},
                "avg_total": {"$avg": "$Total"}
            }

        }]).to_list()
    save_json(data, "aggregation_first_query.json")


def aggregation_second_query(collection):
    data = collection.aggregate([
        {
            "$group": {
                "_id": "$job",
                "count": {"$sum": 1},
            }

        }]).to_list()
    save_json(data, "aggregation_second_query.json")


def aggregation_third_query(collection):
    data = collection.aggregate([
        {
            "$group": {
                "_id": "$HP",
                "min_attack": {"$min": "$Attack"}
            }
        },
        {
            "$group": {
                "_id": "result",
                "max_hp": {"$max": "$_id"},
                "min_attack": {"$min": "$min_attack"}
            }
        }
    ]).to_list()
    save_json(data, "aggregation_third_query.json")


def aggregation_fourth_query(collection):
    data = collection.aggregate([
        {
            "$match": {
                "Generation": {"$gt": 1}
            }
        },
        {
            "$group": {
                "_id": "$Generation",
                "max_speed": {"$max": "$Speed"},
                "min_speed": {"$min": "$Speed"},
                "avg_speed": {"$avg": "$Speed"}
            }
        },
        {
            "$sort": {
                "avg_speed": pymongo.ASCENDING
            }
        }
    ]).to_list()
    save_json(data, "aggregation_fourth_query.json")


def aggregation_fifth_query(collection):
    data = collection.aggregate([
        {
            "$match": {
                "Type 1": {"$in": ["Fire", "Grass"]},
                "$or": [{"Speed": {"$gt": 50, "$lt": 100}},
                        {"Speed": {"$gt": 10, "$lt": 30}}]
            }
        },
        {
            "$group": {
                "_id": "result",
                "max_total": {"$max": "$Total"},
                "min_total": {"$min": "$Total"},
                "avg_total": {"$avg": "$Total"}
            }
        }
    ]).to_list()
    save_json(data, "aggregation_fifth_query.json")

def update_first_query(collection):
    data = [collection.delete_many({
        "$or": [
            {"Total": {"$lt": 200}},
            {"Total": {"$gt": 600}}
        ]
    }).raw_result]
    save_json(data, "update_first_query.json")


def update_second_query(collection):
    data = [collection.update_many({},
                                   {"$inc": {
                                       "Generation": 1
                                   }}).raw_result]
    save_json(data, "update_second_query.json")


def update_third_query(collection):
    data = [collection.update_many({
        "Type 1": {"$in": ["Grass"]}
    },
        {"$mul": {
            "HP": 2
        }}).raw_result]
    save_json(data, "update_third_query.json")


def update_fourth_query(collection):
    data = [collection.update_many({
        "Type 2": {"$in": ["Poison"]}
    },
        {"$mul": {
            "Defense": 3
        }}).raw_result]
    save_json(data, "update_fourth_query.json")


def update_fifth_query(collection):
    data = [collection.update_many({
        "Type 1": {"$in": ["Fire", "Water"]},
        "Type 2": {"$in": ["Poison"]},
        "Speed": {"$gt": 50, "$lte": 150}
    },
        {"$mul": {
            "Speed": 3
        }}).raw_result]
    save_json(data, "update_fifth_query.json")


def main():
    collection: pymongo.cursor.Collection = connect_db()
    items = read_json()
    insert_data(collection, items)
    sample_first_query(collection)
    sample_second_query(collection)
    sample_third_query(collection)
    sample_fourth_query(collection)
    sample_fifth_query(collection)
    items = read_csv()
    insert_data(collection, items)
    aggregation_first_query(collection)
    aggregation_second_query(collection)
    aggregation_third_query(collection)
    aggregation_fourth_query(collection)
    aggregation_fifth_query(collection)
    update_first_query(collection)
    update_second_query(collection)
    update_third_query(collection)
    update_fourth_query(collection)
    update_fifth_query(collection)

if __name__ == '__main__':
    main()
