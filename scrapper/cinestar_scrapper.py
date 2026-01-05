import requests
from datetime import datetime


def get_movies_data(data):
    moviess = []
    for item in data:
        title = item.get("Title")

        image_url = item.get("PosterImageUrl")
        if image_url and image_url.startswith("//"):
            image_url = "https:" + image_url

        raw_date = item.get("ReleaseDate")

        timestamp = int(raw_date.strip("/Date()"))
        release_date = datetime.fromtimestamp(timestamp / 1000)

        moviess.append(
            {
                "name": title,
                "image": image_url,
                "release_date": release_date.strftime("%Y-%m-%d") if release_date else None,
            }
        )

    return moviess


now_showing_url = "https://cinestar.pk/Browsing/Home/NowShowing"
response_now_showing = requests.get(now_showing_url)
data = response_now_showing.json()
movies = get_movies_data(data)


upcoming_url = "https://cinestar.pk/Browsing/Home/ComingSoon"
response_upcoming = requests.get(upcoming_url)
data_upcoming = response_upcoming.json()
movies_upcoming = get_movies_data(data_upcoming)


WEBHOOK_URL = "https://discordapp.com/api/webhooks/1453007866368884759/uSDUHCJ-5VyF8UAeVWYiZ3cugRfGU42OAK9sNCchkiroNBD7pa1K2iV38GEZ6quawe4N"


def build_embeds(payload):
    embeds = []
    
    for section, movies in payload.items():
        for movie in movies:
            embed = {
                "title": f"**{movie['name']}**",
                "description": f"Release: **{movie['release_date']}**",
                "image": {"url": movie["image"]},
                "fields":[
                    {"name": "Category", "value": f"**{section}**", "inline":True},
                ],
                "color":0x0099ff,
            }
            embeds.append(embed)

    return embeds


def chunk_list(list, size):
    for i in range(0, len(list), size): # 0-size, split 10
        yield list[i:size+i]



def send_to_discord(webhook_url: str, movies: list, movies_upcoming: list):
    payload = {
        "Now Showing": movies,
        "Upcoming": movies_upcoming,
    }
    embeds = build_embeds(payload)
    for chunk in chunk_list(embeds, 10):
        resp = requests.post(
            webhook_url,
            json={"embeds": chunk}
        )
        print("Discord webhook status:", resp.status_code)
        if resp.status_code >= 400:
            print("Response:", resp.text)
            break
        
    return resp


if __name__ == "__main__":
    send_to_discord(WEBHOOK_URL, movies, movies_upcoming)
