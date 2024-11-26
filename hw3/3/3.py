import json
import os
import re

import pandas as pd
from bs4 import BeautifulSoup

digit_re = re.compile("[^.0-9]+")

def parse_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        item = dict()
        content = f.read()
        site = BeautifulSoup(content, features='xml')
        item["name"] = site.find("name").text.strip()
        item["constellation"] = site.constellation.text.strip()
        item["spectral-class"] = site.find("spectral-class").text.strip()
        item["radius"] = int(site.radius.text.strip())
        item["rotation (in days)"] = float(re.sub(digit_re,"", site.rotation.text))
        item["age (in billion years)"] = float(re.sub(digit_re,"", site.age.text))
        item["distance (in million km)"] = float(re.sub(digit_re,"", site.distance.text))
        item["absolute-magnitude (in million km)"] = float(re.sub(digit_re, "", site.find("absolute-magnitude").text))
        return item

def main():
    folder_name = "data"
    files = os.listdir(folder_name)
    storage = []
    for file_name in files:
        file_path = f"{folder_name}/{file_name}"
        storage.append(parse_file(file_path))
    json_storage = json.dumps(storage, ensure_ascii=False, indent=4)
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(json_storage)

    # отсортировал по радиусу созвездия
    sorted_by_radius = sorted(storage, key=lambda x: x['radius'])
    threshold = 50
    # отфильтровал по длительности вращения
    filter_by_threshold_rotation = list(filter(lambda x: x["rotation (in days)"] < threshold, storage))
    json_storage = json.dumps(filter_by_threshold_rotation, ensure_ascii=False, indent=4)
    with open('filter_by_threshold_rotation.json', 'w', encoding='utf-8') as file:
        file.write(json_storage)

    # числовые характеристики по возрасту
    total_sum = sum(item['age (in billion years)'] for item in storage)
    min_value = min(item['age (in billion years)'] for item in storage)
    max_value = max(item['age (in billion years)'] for item in storage)
    mean_value = total_sum / len(storage)

    # частота меток constellation
    storage_df = pd.read_json('data.json')
    values_freq = storage_df['constellation'].value_counts()
    print(values_freq)


if __name__ == '__main__':
     main()