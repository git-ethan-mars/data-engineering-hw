import csv
import json
import os
import pickle
import msgpack

with open("chat.json", "r", encoding="utf-8") as source_file:
    data = json.load(source_file)
    messages = data["messages"]
    messages = list(filter(lambda message: message["type"] != "service", messages))
    for message in messages:
        del message["text_entities"]
        del message["type"]
    min_value = int(messages[0]["date_unixtime"])
    max_value = int(messages[0]["date_unixtime"])
    sum_value = 0
    for message in messages:
        time = int(message["date_unixtime"])
        min_value = min(time, min_value)
        max_value = max(time, max_value)
        sum_value += time
    avg_value = sum_value / len(messages)
    temp = 0
    for message in messages:
        time = int(message["date_unixtime"])
        temp += (time - avg_value) ** 2
    average_deviation = temp / len(messages)
    messages_by_source = dict()
    for message in messages:
        source = message["from"]
        if source not in messages_by_source:
            messages_by_source[source] = 0
        messages_by_source[source] += 1
    sources = map(lambda message: message["from"], messages)
    sorted_messages_by_source = dict()
    for source in sorted(sources, key=lambda key: messages_by_source[key], reverse=True):
        sorted_messages_by_source[source] = messages_by_source[source]
    result = {"time_stats":
        {'min_value': min_value, 'max_value': max_value, 'avg_value': avg_value, 'avg_deviation': average_deviation,
         'sum_value': sum_value}, "user_stats": sorted_messages_by_source}
    with open("calculation_result.json", "w", encoding="utf-8") as output_file:
        output_file.write(json.dumps(result, ensure_ascii=False, indent=4))
    with open("messages.csv", "w", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")
        csv_writer.writerow(messages[0].keys())
        for message in messages:
            csv_writer.writerow(message.values())
    print(f"CSV FILE SIZE: {os.stat("messages.csv").st_size}")
    with open("messages.json", "w", encoding="utf-8") as json_file:
        json.dump(messages, json_file, ensure_ascii=False)
    print(f"JSON FILE SIZE: {os.stat("messages.json").st_size}")
    with open("messages.pkl", "wb") as pkl_file:
        pickle.dump(messages, pkl_file)
    print(f"PKL FILE SIZE: {os.stat("messages.pkl").st_size}")
    with open("messages.msgpack", "wb") as msgpack_file:
        msgpack.dump(messages, msgpack_file)
    print(f"MSGPACK FILE SIZE: {os.stat("messages.msgpack").st_size}")



