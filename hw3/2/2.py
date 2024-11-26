import json
import os
import re

import pandas as pd
from bs4 import BeautifulSoup

digit_re = re.compile("[^0-9]+")


def parse_html(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:

        content = f.read()
        site = BeautifulSoup(content, 'html.parser')
        data = []
        for item in site.findAll("div", class_="pad"):
            info = dict()
            info["image_path"] = item.img["src"]
            info["product_name"] = item.span.text.strip()
            info["price"] = int(re.sub(digit_re,"", item.price.text))
            info["bonus"] = int(re.sub(digit_re, "", item.strong.text))
            device_characteristics = dict()
            for li in item.ul.find_all("li"):
                key = li.attrs['type']
                value = li.text.strip()
                device_characteristics[key] = value
            info["device_characteristics"] = device_characteristics
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

    # отсортировал по количеству получаемых бонусов при покупке
    sorted_by_bonus = sorted(storage, key=lambda x: x['bonus'])
    threshold = 20000
    # отфильтровал предметы, имеющие цену до 20 тысяч
    filter_by_threshold_price = list(filter(lambda x: x['price'] < threshold, storage))
    json_storage = json.dumps(filter_by_threshold_price, ensure_ascii=False, indent=4)
    with open('filter_by_threshold_price.json', 'w', encoding='utf-8') as file:
        file.write(json_storage)

    # числовые характеристики по ценам
    total_sum = sum(item['price'] for item in storage)
    min_value = min(item['price'] for item in storage)
    max_value = max(item['price'] for item in storage)
    mean_value = total_sum / len(storage)

    # частота меток product_name
    storage_df = pd.read_json('data.json')
    values_freq = storage_df['product_name'].value_counts()
    print(values_freq)

if __name__ == '__main__':
    main()