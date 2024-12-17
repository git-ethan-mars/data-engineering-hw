import json

import pymongo
from pymongo import MongoClient
import msgpack


def read_msgpack():
    with open("task_1_item.msgpack", "rb") as file:
        return msgpack.load(file)


def connect_db():
    client = MongoClient()
    db = client["db-2025"]
    return db.jobs


def first_query(collection):
    data = drop_id(list(collection.find(limit=10).sort({"salary": pymongo.ASCENDING})))
    save_json(data, "first_query.json")


def second_query(collection):
    data = drop_id(list(collection.find({"age": {"$lt": 30}}, limit=15).sort({"salary": pymongo.ASCENDING})))
    save_json(data, "second_query.json")


def third_query(collection):
    data = drop_id(list(collection.find(
        {"job": {"$in": ["Бухгалтер", "Оператор call-центра", "Водитель"]}, "city": {"$in": ["Ташкент"]}},
        limit=10).sort({"salary": pymongo.ASCENDING})))
    save_json(data, "third_query.json")


def fourth_query(collection):
    count = collection.count_documents({"year": {"$gte": 2019, "$lte": 2022},
                                         "$or": [{"salary": {"$gt": 50000, "$lte": 75000}},
                                                 {"salary": {"$gt": 125000, "$lt": 150000}}]})
    save_json([{"entry_count" : count}], "fourth_query.json")


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
    collection : pymongo.cursor.Collection = connect_db()
    items = read_msgpack()
    collection.insert_many(items)
    first_query(collection)
    second_query(collection)
    third_query(collection)
    fourth_query(collection)


if __name__ == '__main__':
    main()
