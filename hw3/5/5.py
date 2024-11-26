import os

import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import regex

tournament_info_re = regex.compile(r"[\w ]+:[\w, $]+")


def parse_tournament(link):
    request = requests.get(link)
    site = BeautifulSoup(request.text, features="html.parser")
    data_container = site.find("div", class_="fo-nttax-infobox")
    tournament = dict()
    for elem in data_container.find_all("div"):
        text = elem.text
        text = text.replace("\xa0", " ")
        if tournament_info_re.search(text):
            pair = text.split(":")
            key = pair[0].strip()
            value = pair[1].strip()
            if key == "Teams":
                value = int(value)
            if not key.startswith("[e][h]"):
                tournament[key] = value
    return tournament


def convert_currency(currency):
    currency = currency.replace("$", "").replace("USD", "").replace(" ", "").replace(",", "")
    return int(currency)


def main():
    domain = "https://liquipedia.net"
    request = requests.get(f"{domain}/dota2/Main_Page")
    site = BeautifulSoup(request.text, features="html.parser")
    tournaments = []
    for element in site.find("ul", class_="tournaments-list-type-list").find_all("li"):
        tournament = dict()
        temp = element.find("div", class_="tournament-badge__chip chip--tier1")
        if temp:
            tournament["tier"] = temp.text + " " + element.find("div", class_="tournament-badge__text").text
        else:
            tournament["tier"] = element.find("div", class_="tournament-badge__text").text
        tag_a = element.find("a")
        tournament["name"] = tag_a.attrs["title"]
        tournament["link"] = domain + tag_a.attrs["href"]
        tournament["data"] = element.find("small").text
        tournaments.append(tournament)
    if not os.path.exists("data"):
        os.mkdir("data")
    with open("data/tournaments.json", "w") as file:
        json.dump(tournaments, file, indent=4)
    tournaments_ext = []
    for tournament in tournaments:
        data = {"Name": tournament["name"]}
        data.update(parse_tournament(tournament["link"]))
        tournaments_ext.append(data)
    with open("data/tournaments_ext.json", "w") as file:
        json.dump(tournaments_ext, file, indent=4)
    # Отсортировал по количеству команд на турнире
    sort_by_team_count = list(
        sorted(tournaments_ext, key=lambda tournament: tournament["Teams"] if "Teams" in tournament else 0))
    # Отфильтровал по турнирам, проводимым в СНГ
    filter_by_cis_location = list(filter(lambda tournament: tournament["Location"] == "CIS", tournaments_ext))
    # числовые характеристики по призовому фонду
    tournaments_with_prizes = list(filter(lambda tournament: "Prize Pool" in tournament, tournaments_ext))
    total_sum = sum(convert_currency(item["Prize Pool"]) for item in tournaments_with_prizes)
    min_value = min(convert_currency(item["Prize Pool"]) for item in tournaments_with_prizes)
    max_value = max(convert_currency(item["Prize Pool"]) for item in tournaments_with_prizes)
    mean_value = total_sum / len(tournaments_with_prizes)
    with open("data/prize_pool.json", "w") as file:
        json.dump({"total_sum": total_sum, "min_value": min_value, "max_value": max_value, "mean_value": mean_value},
                  file, indent=4)
    with open("data/filter_by_cis_location.json", "w") as file:
        json.dump(filter_by_cis_location, file, indent=4)

    # Посчитал частоту меток для серии турниров
    storage_df = pd.read_json("data/tournaments_ext.json")
    values_freq = storage_df["Series"].value_counts()
    print(values_freq)


if __name__ == '__main__':
    main()
