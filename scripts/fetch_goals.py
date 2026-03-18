import requests
import json
import time

schedule_url = "https://api-web.nhle.com/v1/schedule/now"

def safe_json(url):

    try:
        r = requests.get(url, timeout=20)

        if r.status_code != 200:
            print("Bad status:", r.status_code, url)
            return None

        if not r.text.strip():
            print("Empty response:", url)
            return None

        return r.json()

    except Exception as e:
        print("Request failed:", url, e)
        return None


schedule = safe_json(schedule_url)

if not schedule:
    print("Failed to fetch schedule")
    exit(0)

goals = []

for day in schedule.get("gameWeek", []):

    for game in day.get("games", []):

        game_id = game["id"]

        pbp_url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play"

        pbp = safe_json(pbp_url)

        if not pbp:
            continue

        for play in pbp.get("plays", []):

            if play.get("typeDescKey") != "goal":
                continue

            details = play.get("details", {})

            goals.append({
                "x": details.get("xCoord"),
                "y": details.get("yCoord"),
                "player": details.get("scoringPlayerName"),
                "team": details.get("eventOwnerTeamId"),
                "shotType": details.get("shotType"),
                "period": play.get("periodDescriptor", {}).get("number"),
                "time": play.get("timeInPeriod"),
                "gameId": game_id
            })

        time.sleep(0.5)  # avoid rate limits

print("Goals collected:", len(goals))

with open("data/goals.json", "w") as f:
    json.dump(goals, f)
