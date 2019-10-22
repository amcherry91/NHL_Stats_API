import requests
import json
import urllib.request
from urllib.request import urlopen
import csv
import pandas as pd

# go to https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#teams for documentation and list of directories

"""response = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
print(response.json())

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(response.json())

# get current team information
r = response.json()
data_teams = (r["teams"])
c = csv.writer(open("team_data_api.csv", "w"), lineterminator= "\n")

for item in r["teams"]:
    c.writerow([item["id"], item["name"], item["abbreviation"], item["teamName"], item["link"], item["venue"], item["locationName"],
               item["firstYearOfPlay"], item["division"], item["conference"], item["franchise"], item["shortName"]])"""

# get current team standings
response_standings = requests.get("https://statsapi.web.nhl.com/api/v1/standings")
print(response_standings.json())
c = csv.writer(open("team_standings.csv", "w"), lineterminator= "\n")

with urlopen("https://statsapi.web.nhl.com/api/v1/standings") as response:
    source_standings = response.read()

data_standings = json.loads(source_standings)
# print(json.dumps(data_standings, indent= 2))

for item in data_standings["records"]:
    c.writerow([item["teamRecords"]])

# code is WIP

