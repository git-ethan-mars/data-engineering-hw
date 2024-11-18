import pandas

df = pandas.read_csv("fourth_task.txt")
df.drop("description", inplace=True, axis=1)
with open("fourth_task_result_1.txt", "w") as file:
    file.writelines([f"{df["price"].mean()}\n", f"{df["quantity"].max()}\n", f"{df["price"].min()}"])
df[df["status"] == "Out of Stock"].to_csv("fourth_task_result_2.csv")
