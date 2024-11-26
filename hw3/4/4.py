import json
import os
import re

import pandas as pd
from bs4 import BeautifulSoup

digit_re = re.compile("[^0-9]+")


def parse_html(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        content = f.read()
        site = BeautifulSoup(content, 'xml')
        data = []
        for item in site.find_all("clothing"):
            info = dict()
            info["id"] = int(item.id.text.strip())
            info["product_name"] = item.find("name").text.strip()
            info["category"] = item.category.text.strip()
            info["size"] = item.size.text.strip()
            info["color"] = item.color.text.strip()
            info["material"] = item.material.text.strip()
            info["price"] = int(item.price.text.strip())
            info["rating"] = float(item.rating.text.strip())
            info["reviews"] = int(item.reviews.text.strip())
            if item.exclusive:
                info["exclusive"] = item.exclusive.text.strip()
            if item.new:
                info["new"] = item.new.text.strip()
            if item.sporty:
                info["sporty"] = item.sporty.text.strip()
            data.append(info)
        return data


def main():
    storage = list()
    folder_name = "data"
    files = os.listdir("data")
    for file_name in files:
        file_path = f"{folder_name}/{file_name}"
        items = parse_html(file_path)
        for item in items:
            storage.append(item)
    json_storage = json.dumps(storage, ensure_ascii=False, indent=4)
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(json_storage)

    # отсортировал по рейтингу
    sorted_by_bonus = sorted(storage, key=lambda x: x['rating'])
    threshold = 150000
    # отфильтровал предметы, имеющие цену до 150 тысяч
    filter_by_threshold_price = list(filter(lambda x: x['price'] < threshold, storage))
    json_storage = json.dumps(filter_by_threshold_price, ensure_ascii=False, indent=4)
    with open('filter_by_threshold_price.json', 'w', encoding='utf-8') as file:
        file.write(json_storage)

    # числовые характеристики по оценкам
    total_sum = sum(item['reviews'] for item in storage)
    min_value = min(item['reviews'] for item in storage)
    max_value = max(item['reviews'] for item in storage)
    mean_value = total_sum / len(storage)

    # частота меток category
    storage_df = pd.read_json('data.json')
    values_freq = storage_df['category'].value_counts()
    print(values_freq)

if __name__ == '__main__':
    main()