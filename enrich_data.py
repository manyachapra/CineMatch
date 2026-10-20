
import os
import time
import ast
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE = "https://api.themoviedb.org/3"

df = pd.read_csv("data/cleaned_movies.csv")
session = requests.Session()

def get_details(row):
    media_type = (
        "tv" if row["type"] in ["tv", "series"]
        else "movie"
    )

    url = f"{BASE}/{media_type}/{int(row['tmdb_id'])}"

    try:
        response = session.get(
            url,
            params={
                "api_key": API_KEY,
                "append_to_response": "keywords,credits"
            },
            timeout=20
        )
        response.raise_for_status()
        data = response.json()

        keywords_data = data.get("keywords", {})
        keywords = keywords_data.get(
            "keywords",
            keywords_data.get("results", [])
        )

        cast = data.get("credits", {}).get(
            "cast", []
        )

        return pd.Series({
            "genre_names": " ".join(
                g["name"]
                for g in data.get("genres", [])
            ),
            "keywords": " ".join(
                k["name"] for k in keywords
            ),
            "cast": " ".join(
                actor["name"]
                for actor in cast[:5]
            ),
            "tagline": data.get("tagline", "")
        })

    except requests.RequestException:
        return pd.Series({
            "genre_names": "",
            "keywords": "",
            "cast": "",
            "tagline": ""
        })

metadata = []

for i, (_, row) in enumerate(df.iterrows()):
    metadata.append(get_details(row))

    if (i + 1) % 100 == 0:
        print(f"Processed {i + 1}/{len(df)}")

    time.sleep(0.25)

metadata = pd.DataFrame(metadata)
result = pd.concat(
    [df.reset_index(drop=True), metadata],
    axis=1
)

result.to_csv(
    "data/enriched_movies.csv",
    index=False
)

print("Enrichment complete:", len(result))