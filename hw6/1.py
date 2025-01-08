import json
import os
import matplotlib
import pandas as pd


# Download latest version
# path = kagglehub.dataset_download("fabriziocominetti/imdb-data")
# print("Path to dataset files:", path)

def read_file(file_name):
    return pd.read_csv(file_name, low_memory=False)


def get_memory_stat_by_column(df):
    memory_usage_stat = df.memory_usage(deep=True)
    total_memory_usage = memory_usage_stat.sum()
    print(f"file in memory size = {total_memory_usage // 1024:10} КБ")
    column_stat = list()
    for key in df.dtypes.keys():
        column_stat.append({
            "column_name": key,
            "memory_absolute": memory_usage_stat[key] // 1024,
            "memory_percentage": round(memory_usage_stat[key] / total_memory_usage * 100, 4),
            "dtype": str(df.dtypes[key])
        })
    column_stat.sort(key=lambda x: x["memory_absolute"], reverse=True)
    return column_stat


def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:  # предположим, что если это не датафрейм, то серия
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2  # преобразуем байты в мегабайты
    return "{:03.2f} MB".format(usage_mb)


def opt_obj(df):
    converted_obj = pd.DataFrame()
    dataset_obj = df.select_dtypes(include=['object']).copy()

    for col in dataset_obj.columns:
        num_unique_values = len(dataset_obj[col].unique())
        num_total_values = len(dataset_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:, col] = dataset_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = dataset_obj[col]

    print(mem_usage(dataset_obj))
    print(mem_usage(converted_obj))

    compare_obj = pd.concat([dataset_obj.dtypes, converted_obj.dtypes], axis=1)
    compare_obj.columns = ['before', 'after']
    print(compare_obj)

    return converted_obj


def opt_float(df):
    # # =======================================================================
    # # выполняем понижающее преобразование
    # # для столбцов типа float
    dataset_float = df.select_dtypes(include=['float'])
    converted_float = dataset_float.apply(pd.to_numeric, downcast='float')

    print(mem_usage(dataset_float))
    print(mem_usage(converted_float))

    compare_floats = pd.concat([dataset_float.dtypes, converted_float.dtypes], axis=1)
    compare_floats.columns = ['before', 'after']
    compare_floats.apply(pd.Series.value_counts)
    print(compare_floats)

    return converted_float


def main():
    # steps 1-3
    file_name = "data/title_basics.csv"

    print(f"file in disk size = {os.stat(file_name).st_size // 1024:10} КБ")
    dataset = read_file(file_name)
    # steps 4-6
    stats = pd.DataFrame(get_memory_stat_by_column(dataset))
    stats.to_json("data/stats_before_optimization.json", indent=4, orient="records")
    optimized_dataset = dataset.copy()

    converted_obj = opt_obj(dataset)
    converted_float = opt_float(dataset)
    #
    optimized_dataset[converted_obj.columns] = converted_obj
    optimized_dataset[converted_float.columns] = converted_float
    # 7
    print(mem_usage(dataset))
    print(mem_usage(optimized_dataset))
    optimized_dataset.info(memory_usage='deep')
    stats = pd.DataFrame(get_memory_stat_by_column(optimized_dataset))
    stats.to_json("data/stats_after_optimization.json", indent=4, orient="records")
    # 8
    # отобрать свои 10 колонок
    need_column = dict()
    column_names = ['originalTitle', 'primaryTitle', 'genres',
                    'tconst', 'titleType', 'startYear',
                    'endYear', 'runtimeMinutes', 'isAdult']
    opt_dtypes = optimized_dataset.dtypes
    for key in dataset.columns:
        need_column[key] = opt_dtypes[key]
        print(f"{key}:{opt_dtypes[key]}")
    with open("dtypes_2.json", mode="w") as file:
        dtype_json = need_column.copy()
        for key in dtype_json.keys():
            dtype_json[key] = str(dtype_json[key])
        json.dump(dtype_json, file)

    # 9
    read_and_optimized = pd.read_csv(file_name, usecols=lambda x: x in column_names, dtype=need_column)



if __name__ == '__main__':
    main()
