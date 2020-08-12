import requests

BASE = "http://statsapi.web.nhl.com/api/v1"

schedule = requests.get("{}/schedule".format(BASE)).json()

for game in schedule['dates'][0]['games']:
	print("Game Number: " + str(game['gamePk']))
	#print("Game date: " + game['gameDate'])
	print("Score: " + game['teams']['away']['team']['name'] + " (" \
	+ str(game['teams']['away']['score']) + ") " \
	+ game['teams']['home']['team']['name'] + " (" \
	+ str(game['teams']['home']['score']) + ")")
	print("Game Status: " + game['status']['codedGameState'])
	print("Game State: " + game['status']['detailedState'])
	print()
