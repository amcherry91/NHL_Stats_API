import requests
import json
import csv
import pandas as pd

# go to https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#teams for documentation and list of directories

response = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
print(response.json())

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(response.json())

r = response.json()
data = (r["teams"])
c = csv.writer(open("team_data_api.csv", "w"), lineterminator= "\n")

for item in r["teams"]:
    c.writerow([item["id"], item["name"], item["abbreviation"], item["teamName"], item["link"], item["venue"], item["locationName"],
               item["firstYearOfPlay"], item["division"], item["conference"], item["franchise"], item["shortName"]])










