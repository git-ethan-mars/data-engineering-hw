import json

import requests
from pandas import DataFrame

r = requests.get('https://datausa.io/api/data?drilldowns=Nation&measures=Population')
json_object = json.loads(r.text)
json_formatted_str = json.dumps(json_object, indent=2)
data_df = DataFrame(json_object["data"])
data_df.to_html("sixth_task_result.html")