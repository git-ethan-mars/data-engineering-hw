import json

import pymongo
from pymongo import MongoClient, DESCENDING


def read_json():
    with open("task_2_item.json", "r", encoding="utf-8") as file:
        return json.load(file)


def connect_db():
    client = MongoClient()
    db = client["db-2025"]
    return db.jobs


def first_query(collection):
    data = collection.aggregate([
        {
            "$group": {
                "_id": "result",
                "max_salary": {"$max": "$salary"},
                "min_salary": {"$min": "$salary"},
                "avg_salary": {"$avg": "$salary"}
            }

        }]).to_list()
    save_json(data, "first_query.json")


def second_query(collection):
    data = collection.aggregate([
        {
            "$group": {
                "_id": "$job",
                "count": {"$sum": 1},
            }

        }]).to_list()
    save_json(data, "second_query.json")


def third_query(collection):
    data = collection.aggregate([
        {
            "$group": {
                "_id": "$city",
                "min_salary": {"$min": "$salary"},
                "max_salary": {"$max": "$salary"},
                "avg_salary": {"$avg": "$salary"}
            }

        }]).to_list()
    save_json(data, "third_query.json")


def fourth_query(collection):
    data = collection.aggregate([
        {
            "$group": {
                "_id": "$city",
                "min_age": {"$min": "$age"},
                "max_age": {"$max": "$age"},
                "avg_age": {"$avg": "$age"}
            }

        }]).to_list()
    save_json(data, "fourth_query.json")


def fifth_query(collection):
    data = collection.aggregate([
        {
            "$group": {
                "_id": "$age",
                "max_salary": {"$max": "$salary"}
            }
        },
        {
            "$group": {
                "_id": "result",
                "min_age": {"$min": "$_id"},
                "max_salary": {"$max": "$max_salary"}
            }
        }
    ]).to_list()
    save_json(data, "fifth_query.json")


def sixth_query(collection):
    data = collection.aggregate([
        {
            "$group": {
                "_id": "$age",
                "min_salary": {"$min": "$salary"}
            }
        },
        {
            "$group": {
                "_id": "result",
                "max_age": {"$max": "$_id"},
                "min_salary": {"$min": "$min_salary"}
            }
        }
    ]).to_list()
    save_json(data, "sixth_query.json")


def seventh_query(collection):
    data = collection.aggregate([
        {
            "$match": {
                "salary": {"$gt": 50000}
            }
        },
        {
            "$group": {
                "_id": "$city",
                "max_age": {"$max": "$age"},
                "min_age": {"$min": "$age"},
                "avg_age": {"$avg": "$age"}
            }
        },
        {
            "$sort": {
                "avg_age": pymongo.ASCENDING
            }
        }
    ]).to_list()
    save_json(data, "seventh_query.json")


def eighth_query(collection):
    data = collection.aggregate([
        {
            "$match": {
                "city": {"$in": ["Сеговия", "Минск", "Осера", "Фигерас", "Скопье"]},
                "job": {"$in": ["Архитектор", "Косметолог", "Инженер"]},
                "$or": [{"age": {"$gt": 18, "$lt": 25}},
                       {"age": {"$gt": 50, "$lt": 65}}]
            }
        },
        {
            "$group": {
                "_id": "result",
                "max_salary": {"$max": "$salary"},
                "min_salary": {"$min": "$salary"},
                "avg_salary": {"$avg": "$salary"}
            }
        }
    ]).to_list()
    save_json(data, "eighth_query.json")

def ninth_query(collection):
    data = collection.aggregate([
        {
            "$match": {
                "job": {"$in": ["Архитектор", "Косметолог", "Инженер"]},
            }
        },
        {
            "$group": {
                "_id": "$age",
                "max_salary": {"$max": "$salary"},
                "min_salary": {"$min": "$salary"},
                "avg_salary": {"$avg": "$salary"}
            }
        },
        {
            "$sort" : {
                "_id" : DESCENDING
            }
        },
    ]).to_list()
    save_json(data, "ninth_query.json")


def drop_id(items):
    for item in items:
        del item["_id"]
    return items


def save_json(data, filename):
    items = []
    for row in data:
        items.append(row)
    with open(filename, "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)


def main():
    collection: pymongo.cursor.Collection = connect_db()
    items = read_json()
    collection.insert_many(items)
    first_query(collection)
    second_query(collection)
    third_query(collection)
    fourth_query(collection)
    fifth_query(collection)
    sixth_query(collection)
    seventh_query(collection)
    eighth_query(collection)
    ninth_query(collection)


if __name__ == '__main__':
    main()
