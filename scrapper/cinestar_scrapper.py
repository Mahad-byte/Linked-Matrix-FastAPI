import requests
from datetime import datetime
import json


now_showing_url = "https://cinestar.pk/Browsing/Home/NowShowing"
response_now_showing = requests.get(now_showing_url)
data = response_now_showing.json()

movies = []

for item in data:
    title = item.get("Title")

    image_url = item.get("PosterImageUrl")
    if image_url and image_url.startswith("//"):
        image_url = "https:" + image_url

    raw_date = item.get("ReleaseDate")

    timestamp = int(raw_date.strip("/Date()"))
    release_date = datetime.fromtimestamp(timestamp / 1000)

    movies.append(
        {
            "name": title,
            "image": image_url,
            "release_date": release_date.strftime("%Y-%m-%d") if release_date else None,
        }
    )


upcoming_url = "https://cinestar.pk/Browsing/Home/ComingSoon"
response_upcoming = requests.get(upcoming_url)
data_upcoming = response_upcoming.json()

movies_upcoming = []

for item in data_upcoming:
    title = item.get("Title")

    image_url = item.get("PosterImageUrl")
    if image_url and image_url.startswith("//"):
        image_url = "https:" + image_url

    raw_date = item.get("ReleaseDate")

    timestamp = int(raw_date.strip("/Date()"))
    release_date = datetime.fromtimestamp(timestamp / 1000)

    movies_upcoming.append(
        {
            "name": title,
            "image": image_url,
            "release_date": release_date.strftime("%Y-%m-%d") if release_date else None,
        }
    )


WEBHOOK_URL = "https://discordapp.com/api/webhooks/1453007866368884759/uSDUHCJ-5VyF8UAeVWYiZ3cugRfGU42OAK9sNCchkiroNBD7pa1K2iV38GEZ6quawe4N"


def build_embeds(payload):
    embeds = []

    for section, movies in payload.items():
        for movie in movies:
            embed = {
                "title": f"**{movie['name']}**",
                "description": f"Release: **{movie['release_date']}**",
                "image": {"url": movie["image"]},
                "footer": {"text": f"{section.replace('_', ' ').title()}"}
            }
            embeds.append(embed)

    return embeds


def send_to_discord(webhook_url: str, movies: list, movies_upcoming: list):
    payload = {
        "now_showing": movies[:2],
        "upcoming": movies_upcoming[:2],
    }


    resp = requests.post(
        webhook_url, json={"embeds": build_embeds(payload)}
    )
    print("Discord webhook status:", resp.status_code)
    if resp.status_code >= 400:
        print("Response:", resp.text)
    return resp


if __name__ == "__main__":
    send_to_discord(WEBHOOK_URL, movies, movies_upcoming)
