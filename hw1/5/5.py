import pandas as pd

df = pd.read_html("fifth_task.html", encoding="utf-8")[0]
df.to_csv("fifth_task_result.csv")
