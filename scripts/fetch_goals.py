import requests
import json

schedule_url = "https://api-web.nhle.com/v1/schedule/now"
schedule = requests.get(schedule_url).json()

goals = []

for day in schedule.get("gameWeek", []):
    for game in day.get("games", []):

        game_id = game["id"]

        pbp = requests.get(
            f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play"
        ).json()

        for play in pbp.get("plays", []):

            if play.get("typeDescKey") != "goal":
                continue

            d = play.get("details", {})

            goals.append({
                "x": d.get("xCoord"),
                "y": d.get("yCoord"),
                "player": d.get("scoringPlayerName"),
                "team": d.get("eventOwnerTeamId"),
                "shotType": d.get("shotType"),
                "period": play["periodDescriptor"]["number"],
                "time": play["timeInPeriod"],
                "gameId": game_id
            })

print("Collected goals:", len(goals))

with open("data/goals.json","w") as f:
    json.dump(goals,f)
