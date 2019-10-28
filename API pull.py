import requests
import json
import csv
import pandas as pd

# go to https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#teams for documentation and list of directories
url = 'https://statsapi.web.nhl.com/api/v1/teams'
team_endpoint = 'https://statsapi.web.nhl.com/api/v1/teams/12'
roster_endpoint = 'https://statsapi.web.nhl.com/api/v1/teams/12/roster'
r = requests.get(url + team_endpoint + '/' + str(id) + roster_endpoint)
teams = pd.io.json.json_normalize(r.json()['teams'])
team_id = teams[teams['teamName'] == 'Hurricanes']['id'].values[0]
roster = pd.io.json.json_normalize(r.json()['roster'])
print(team_id)

df = pd.DataFrame()
for p_link in roster['person.link']:
    r = requests.get(url + p_link + '/stats', params={'stats':'gameLog', 'season':'20182019'})
    stats = pd.io.json.json_normalize(r.json()['stats'][0]['splits'])
    if not stats.empty:
        stats = stats.groupby(['team.name']).aggregate(sum)
        stats['playerName'] = roster[roster['person.link'] == p_link]['person.fullName'].values[0]
        df = pd.concat([df, stats], ignore_index=True, sort=False)
    else:
        print('No stats for ' + roster[roster['person.link'] == p_link]['person.fullName'].values[0])

keep_cols = ['stat.assists', 'stat.games', 'stat.goals', 'stat.hits', 'stat.points', 'playerName']
df = df[keep_cols]
rename_cols = {'stat.assist': 'assists', 'stat.games': 'games', 'stat.goals': 'goals', 'stat.hits': 'hits',
               'stat.points': 'points'}

# code is WIP
