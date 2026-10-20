
import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

if not API_KEY:
    raise ValueError("TMDB_API_KEY missing from .env")

session = requests.Session()
session.params = {"api_key": API_KEY}

from serial_filter import classify_title

def make_record(item, media_type):
    genres = item.get("genre_ids", [])

    rec = {
        "tmdb_id": item["id"],
        "title": item.get("title") or item.get("name"),
        "description": item.get("overview", ""),
        "genres": genres,
        "language": item.get("original_language"),
        "release_date": (
            item.get("release_date")
            or item.get("first_air_date")
        ),
        "rating": item.get("vote_average", 0),
        "poster": item.get("poster_path"),
        "type": (
            "series" if media_type == "tv"
            else "movie"
        )
    }

    # Intelligent serial filtering (removes Hindi daily serials & excluded genres)
    status, reason = classify_title(rec)
    if status == "EXCLUDE":
        return None

    return rec


def fetch_titles(media_type, language, pages=50):
    records = []

    for page in range(1, pages + 1):
        params = {
            "with_original_language": language,
            "sort_by": "popularity.desc",
            "include_adult": "false",
            "page": page
        }

        response = session.get(
            f"{BASE_URL}/discover/{media_type}",
            params=params,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()

        for item in data.get("results", []):
            record = make_record(item, media_type)

            if record:
                records.append(record)

        if page >= data.get("total_pages", 0):
            break

        time.sleep(0.25)

    return records


def search_title(title, media_type="tv"):
    response = session.get(
        f"{BASE_URL}/search/{media_type}",
        params={"query": title},
        timeout=30
    )
    response.raise_for_status()

    return [
        record
        for item in response.json().get("results", [])
        if (record := make_record(item, media_type))
    ]


all_titles = []

# Collect movies and series
for media_type in ["movie", "tv"]:
    for language in ["en", "hi"]:
        print(f"Fetching {media_type}: {language}")

        titles = fetch_titles(
            media_type,
            language,
            pages=50
        )

        all_titles.extend(titles)

# Include specific series that may not appear
# in the most popular discovery results
must_have_series = [
    "The Summer I Turned Pretty",
    "Off Campus",
    "Stranger Things",
    "Wednesday",
    "Never Have I Ever",
    "Maxton Hall",
    "Panchayat",
    "Mirzapur"
]

for title in must_have_series:
    results = search_title(title)

    exact = [
        item for item in results
        if item["title"].casefold() == title.casefold()
    ]

    if exact:
        all_titles.append(exact[0])
        print("Added:", title)
    else:
        print("Not found:", title)

df = pd.DataFrame(all_titles)

df.drop_duplicates(
    subset=["tmdb_id", "type"],
    inplace=True
)

os.makedirs("data", exist_ok=True)

df.to_csv(
    "data/cinematch_titles.csv",
    index=False
)

print("\nTotal titles:", len(df))
print(df["type"].value_counts())