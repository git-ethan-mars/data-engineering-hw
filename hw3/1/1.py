import os
import json

import pandas as pd
from bs4 import BeautifulSoup


def parse_html(file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        content = f.read()

        info = dict()

        site = BeautifulSoup(content, 'html.parser')
        info['article'] = site.span.text.split('Наличие:')[0].replace('Артикул: ', '').strip()
        info['contains'] = site.span.text.split('Наличие:')[1].replace('Артикул: ', '').strip()
        info['item_name'] = site.div.h1.text.strip().replace('Название:', '').strip()
        info['town'] = site.div.p.text.split('Цена:')[0].replace('Город:','').strip()
        info['price'] = int(site.div.p.text.split('Цена:')[1].replace('Город:','').replace('руб','').strip())
        info['color'] = site.find('span', class_='color').text.replace("Цвет: ", "").strip()
        info['quantity'] = int(site.find('span', class_='quantity').text.replace("Количество: ", "").replace('шт','').strip())
        info['size'] = site.find_all('span')[3].text.split()[0].replace('Размеры:', '')
        info['image_path'] = site.div.img.attrs['src']
        info['rating'] = float(site.findAll('span')[4].text.replace('Рейтинг: ', '').strip())
        info['view_count'] = int(site.findAll('span')[5].text.replace('Просмотры: ', '').strip())

        return info



def main():
    storage = list()
    folder_name = "data"
    files = os.listdir("data")
    for file_name in files:
        file_path = f"{folder_name}/{file_name}"
        storage.append(parse_html(file_path))
    json_storage = json.dumps(storage, ensure_ascii=False, indent=4)
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(json_storage)

    # отсортировал по количеству просмотров
    sorted_by_view_count = sorted(storage, key=lambda x: x['view_count'])
    filter_by_contains = list()
    for town in storage:
        if town['contains'] == 'Да':
            filter_by_contains.append(town)
    # отфильтровал по наличию
    json_storage = json.dumps(filter_by_contains, ensure_ascii=False, indent=4)
    with open('filter_by_contains.json', 'w', encoding='utf-8') as file:
        file.write(json_storage)

    # посчитал статистику по количеству предметов
    total_sum = sum(item['quantity'] for item in storage)
    min_value = min(item['quantity'] for item in storage)
    max_value = max(item['quantity'] for item in storage)
    mean_value = total_sum / len(storage)

    # частота меток town
    storage_df = pd.read_json('data.json')
    values_freq = storage_df['town'].value_counts()
    print(values_freq)

if __name__ == '__main__':
    main()