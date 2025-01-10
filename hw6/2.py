import json
import matplotlib.pyplot as plt

import pandas as pd


def main():
    with open("dtypes_2.json") as file:
        data = json.load(file)
    df = pd.read_csv("data/title_basics.csv")
    plt.hist(df['startYear'], bins=20, edgecolor='white')
    plt.title('Распределение художественных произведений по годам')
    plt.xlabel('Год')
    plt.ylabel('Частота')
    plt.grid(True)
    plt.savefig("data/start_year_distribution.png")
    plt.clf()
    plt.pie(df['titleType'].value_counts().to_list(), labels=df['titleType'].value_counts().index,
            wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "k"})
    plt.title("График распределения типов произведений")
    plt.savefig("data/title_type_distribution.png")
    plt.clf()
    df_2020 = df[df["startYear"] == 2020]
    d = dict()
    for i in df_2020.index:
        s = df.loc[i]["genres"]
        if not type(s) is str:
            continue
        s = s.lower()
        for genre in s.split(","):
            if genre not in d:
                d[genre] = 0
            d[genre] += 1
    plt.pie(d.values(), labels=d.keys(),
            wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "k"})
    plt.title("График распределения типов произведений в 2020 году")
    plt.savefig("data/title_type_distribution_2020.png")
    plt.clf()


if __name__ == '__main__':
    main()
