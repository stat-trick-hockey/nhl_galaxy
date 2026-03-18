import requests
import json
import time
from datetime import datetime, timedelta

START_DATE = "2026-03-10"
END_DATE = "2026-03-17"

def safe_json(url):
    try:
        r = requests.get(url, timeout=20)
        if r.status_code != 200 or not r.text.strip():
            print(f"Bad response {r.status_code} or empty from {url}")
            return None
        return r.json()
    except Exception as e:
        print(f"Request failed: {url} {e}")
        return None

start = datetime.fromisoformat(START_DATE)
end = datetime.fromisoformat(END_DATE)

date = start
goals = []

while date <= end:
    date_str = date.strftime("%Y-%m-%d")
    schedule_url = f"https://api-web.nhle.com/v1/schedule/{date_str}"

    schedule = safe_json(schedule_url)
    if schedule:
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
                    d = play.get("details", {})
                    goals.append({
                        "x": d.get("xCoord"),
                        "y": d.get("yCoord"),
                        "player": d.get("scoringPlayerName"),
                        "team": d.get("eventOwnerTeamId"),
                        "shotType": d.get("shotType"),
                        "period": play.get("periodDescriptor", {}).get("number"),
                        "time": play.get("timeInPeriod"),
                        "gameId": game_id
                    })
                print(f"Processed game {game_id} on {date_str}")
                time.sleep(0.4)  # avoid rate limits
    else:
        print(f"No schedule for {date_str}")

    date += timedelta(days=1)

print(f"Total goals collected: {len(goals)}")

with open("data/goals.json", "w") as f:
    json.dump(goals, f)
