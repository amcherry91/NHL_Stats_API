import requests
import json
import csv
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# go to https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#teams for documentation and list of directories

url = 'https://statsapi.web.nhl.com/api/v1/teams'
r = requests.get(url)
teams = pd.io.json.json_normalize(r.json()['teams'])
#print(teams[teams['name']== 'Nashville Predators']['id'])

url_1 = 'https://statsapi.web.nhl.com/api/v1/teams/18/roster'
r_1 = requests.get(url_1)
roster = r_1.json()['roster']
roster = pd.io.json.json_normalize(r_1.json()['roster'])

df = pd.DataFrame()
for pid in roster['person.id']:
    url_2 = 'https://statsapi.web.nhl.com/api/v1/people/' + str(pid) + '/stats'
    params = {'stats': 'gameLog', 'season': '20182019'}
    r_2 = requests.get(url_2, params=params)
    stats = pd.io.json.json_normalize(r_2.json()['stats'][0]['splits'])
    if not stats.empty:
        stats = stats.groupby(['team.name']).aggregate(sum)
        stats['Name'] = roster[roster['person.id'] == pid]['person.fullName'].values[0]
        df = pd.concat([df, stats], ignore_index=True, sort=False)
    else:
        print('No stats for ' + roster[roster['person.id'] == pid]['person.fullName']).values[0]
print(df.columns)

keep_cols = ['team.id', 'Name', 'stat.games', 'stat.points', 'stat.goals', 'stat.assists', 'stat.plusMinus', 'stat.hits']
df = df[keep_cols]
rename_cols = {
    'stat.assists': 'Assists',
    'stat.games': 'Games',
    'stat.goals': 'Goals',
    'stat.hits': 'Hits',
    'stat.points': 'Points',
    'team.id': 'id',
    'stat.plusMinus': 'PlusMinus',
    'Name': 'PlayerName'
}

df.rename(columns=rename_cols, inplace=True)
df.head()
print(df)

df.to_csv('player_stats_20182019.csv', index=False)

# code is WIP