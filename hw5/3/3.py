import json

import pymongo
from pymongo import MongoClient


def read_text():
    with open("task_3_item.text", "r", encoding="utf-8") as file:
        items = []
        item = dict()
        for line in file:
            if line == "=====\n":
                items.append(item)
                item = dict()
            else:
                pair = line.strip().split("::")
                if pair[1].isdigit():
                    pair[1] = int(pair[1])
                item[pair[0]] = pair[1]
        return items


def connect_db():
    client = MongoClient()
    db = client["db-2025"]
    return db.jobs


def save_json(data, filename):
    items = []
    for row in data:
        items.append(row)
    with open(filename, "w", encoding="utf-8") as outfile:
        json.dump(items, outfile, indent=4, ensure_ascii=False)


def first_query(collection):
    data = [collection.delete_many({
        "$or": [
            {"salary": {"$lt": 25000}},
            {"salary": {"$gt": 175000}}
        ]
    }).raw_result]
    save_json(data, "first_query.json")


def second_query(collection):
    data = [collection.update_many({},
                                   {"$inc": {
                                       "age": 1
                                   }}).raw_result]
    save_json(data, "second_query.json")


def third_query(collection):
    data = [collection.update_many({
        "job": {"$in": ["Архитектор", "Косметолог", "Инженер"]}
    },
        {"$mul": {
            "salary": 1.05
        }}).raw_result]
    save_json(data, "third_query.json")


def fourth_query(collection):
    data = [collection.update_many({
        "city": {"$in": ["Хихон", "Бишкек"]}
    },
        {"$mul": {
            "salary": 1.07
        }}).raw_result]
    save_json(data, "fourth_query.json")


def fifth_query(collection):
    data = [collection.update_many({
        "city": {"$in": ["Тбилиси", "Санхенхо"]},
        "job": {"$in": ["Учитель", "Медсестра"]},
        "age": {"$gt": 20, "$lte": 60}
    },
        {"$mul": {
            "salary": 1.1
        }}).raw_result]
    save_json(data, "fifth_query.json")


def sixth_query(collection):
    data = [collection.delete_many({
        "city": {"$in": ["Барселона", "Валенсия"]},
        "job": {"$in": ["Косметолог", "Архитектор", "Психолог"]}
    }).raw_result]
    save_json(data, "sixth_query.json")


def main():
    collection: pymongo.cursor.Collection = connect_db()
    items = read_text()
    collection.insert_many(items)
    first_query(collection)
    second_query(collection)
    third_query(collection)
    fourth_query(collection)
    fifth_query(collection)
    sixth_query(collection)


if __name__ == '__main__':
    main()
