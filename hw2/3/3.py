import json
import os

import msgpack

import pandas

df = pandas.read_json("third_task.json")
stats_df = df.groupby("category").agg(average_price=('price', 'mean'), maximum_price=('price', 'max'),
                                      minimum_price=('price', 'min'))
stats_json = stats_df.to_json(force_ascii=False, indent=4)
with open("third_task_result.json", "w", encoding="utf-8") as file:
    file.write(stats_json)
with open("third_task_result.msgpack", "wb") as file:
    msgpack.dump(stats_json, file)
print(
    f"COMPRESSED FILE = {os.stat("third_task_result.msgpack").st_size}, COMMON FILE = {os.stat("third_task_result.json").st_size}")
