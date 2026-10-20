import os
import sys
import time
import argparse
import datetime
import requests
import numpy as np
import pandas as pd
import torch
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from serial_filter import classify_title

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

if not API_KEY:
    print("=" * 60)
    print("ERROR: TMDB_API_KEY is not set or empty!")
    print("• For local runs: Add TMDB_API_KEY=<your_key> to .env")
    print("• For GitHub Actions: Add TMDB_API_KEY secret under Settings -> Secrets and variables -> Actions")
    print("=" * 60)

# Offline operation can be controlled via environment variables if desired
# Defaults to normal online/cached behavior for seamless GitHub Actions & local runs


def get_device():
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    return "cpu"


def fetch_candidate_releases(session, days_back=30, max_pages=3):
    """Fetch recently released movies and series from TMDB."""
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days_back)
    start_str = start_date.strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")

    candidates = []

    languages = ["en", "hi", "ta", "te", "ml"]

    # 1. Discover Movies
    for lang in languages:
        for page in range(1, max_pages + 1):
            params = {
                "api_key": API_KEY,
                "primary_release_date.gte": start_str,
                "primary_release_date.lte": today_str,
                "with_original_language": lang,
                "sort_by": "popularity.desc",
                "include_adult": "false",
                "page": page
            }
            try:
                res = session.get(f"{BASE_URL}/discover/movie", params=params, timeout=15)
                res.raise_for_status()
                data = res.json()
                for item in data.get("results", []):
                    candidates.append({
                        "tmdb_id": item["id"],
                        "title": item.get("title") or item.get("original_title"),
                        "description": item.get("overview", ""),
                        "genres": item.get("genre_ids", []),
                        "language": item.get("original_language"),
                        "release_date": item.get("release_date"),
                        "rating": item.get("vote_average", 0),
                        "poster": item.get("poster_path"),
                        "type": "movie"
                    })
                if page >= data.get("total_pages", 0):
                    break
            except Exception as e:
                print(f"Warning: Failed to fetch discover movies ({lang}, p{page}): {e}")
                break
            time.sleep(0.2)

    # 2. Discover TV / Web Series
    for lang in languages:
        for page in range(1, max_pages + 1):
            params = {
                "api_key": API_KEY,
                "first_air_date.gte": start_str,
                "first_air_date.lte": today_str,
                "with_original_language": lang,
                "sort_by": "popularity.desc",
                "include_adult": "false",
                "page": page
            }
            try:
                res = session.get(f"{BASE_URL}/discover/tv", params=params, timeout=15)
                res.raise_for_status()
                data = res.json()
                for item in data.get("results", []):
                    candidates.append({
                        "tmdb_id": item["id"],
                        "title": item.get("name") or item.get("original_name"),
                        "description": item.get("overview", ""),
                        "genres": item.get("genre_ids", []),
                        "language": item.get("original_language"),
                        "release_date": item.get("first_air_date"),
                        "rating": item.get("vote_average", 0),
                        "poster": item.get("poster_path"),
                        "type": "series"
                    })
                if page >= data.get("total_pages", 0):
                    break
            except Exception as e:
                print(f"Warning: Failed to fetch discover TV ({lang}, p{page}): {e}")
                break
            time.sleep(0.2)

    # 3. Trending this week (captures viral hits regardless of language)
    for endpoint, m_type in [("movie", "movie"), ("tv", "series")]:
        try:
            res = session.get(f"{BASE_URL}/trending/{endpoint}/week", params={"api_key": API_KEY}, timeout=15)
            if res.status_code == 200:
                for item in res.json().get("results", []):
                    candidates.append({
                        "tmdb_id": item["id"],
                        "title": item.get("title") or item.get("name") or item.get("original_title"),
                        "description": item.get("overview", ""),
                        "genres": item.get("genre_ids", []),
                        "language": item.get("original_language"),
                        "release_date": item.get("release_date") or item.get("first_air_date"),
                        "rating": item.get("vote_average", 0),
                        "poster": item.get("poster_path"),
                        "type": m_type
                    })
        except Exception as e:
            print(f"Warning: Failed to fetch trending {endpoint}: {e}")

    return candidates


def enrich_item(session, item):
    """Fetch cast, keywords, genres, and tagline from TMDB."""
    media_endpoint = "tv" if item["type"] == "series" else "movie"
    url = f"{BASE_URL}/{media_endpoint}/{item['tmdb_id']}"
    try:
        res = session.get(
            url,
            params={
                "api_key": API_KEY,
                "append_to_response": "keywords,credits"
            },
            timeout=15
        )
        res.raise_for_status()
        data = res.json()

        kw_data = data.get("keywords", {})
        kw_list = kw_data.get("keywords", kw_data.get("results", []))
        cast_list = data.get("credits", {}).get("cast", [])

        genre_names = " ".join(g["name"] for g in data.get("genres", []))
        keywords = " ".join(k["name"] for k in kw_list)
        cast = " ".join(actor["name"] for actor in cast_list[:5])
        tagline = data.get("tagline", "")

        enriched = item.copy()
        enriched["genre_names"] = genre_names
        enriched["keywords"] = keywords
        enriched["cast"] = cast
        enriched["tagline"] = tagline
        return enriched
    except Exception as e:
        print(f"Enrichment error for {item['title']} ({item['tmdb_id']}): {e}")
        enriched = item.copy()
        enriched["genre_names"] = ""
        enriched["keywords"] = ""
        enriched["cast"] = ""
        enriched["tagline"] = ""
        return enriched


def fetch_candidates_by_ids(session, tmdb_ids):
    """Fetch specific titles by TMDB ID."""
    candidates = []
    for mid in tmdb_ids:
        found = False
        for media_type in ["movie", "tv"]:
            url = f"{BASE_URL}/{media_type}/{mid}"
            try:
                res = session.get(url, params={"api_key": API_KEY}, timeout=15)
                if res.status_code == 200:
                    data = res.json()
                    candidates.append({
                        "tmdb_id": data["id"],
                        "title": data.get("title") or data.get("name") or data.get("original_title"),
                        "description": data.get("overview", ""),
                        "genres": [g["id"] for g in data.get("genres", [])],
                        "language": data.get("original_language"),
                        "release_date": data.get("release_date") or data.get("first_air_date"),
                        "rating": data.get("vote_average", 0),
                        "poster": data.get("poster_path"),
                        "type": "movie" if media_type == "movie" else "series"
                    })
                    found = True
                    break
            except Exception as e:
                print(f"Error fetching ID {mid} ({media_type}): {e}")
        if not found:
            print(f"Warning: TMDB ID {mid} not found on TMDB.")
    return candidates


def fetch_candidates_by_query(session, query, max_results=5):
    """Search TMDB for specific title queries."""
    candidates = []
    for media_type in ["movie", "tv"]:
        url = f"{BASE_URL}/search/{media_type}"
        try:
            res = session.get(url, params={"api_key": API_KEY, "query": query}, timeout=15)
            if res.status_code == 200:
                data = res.json()
                for item in data.get("results", [])[:max_results]:
                    candidates.append({
                        "tmdb_id": item["id"],
                        "title": item.get("title") or item.get("name") or item.get("original_title"),
                        "description": item.get("overview", ""),
                        "genres": item.get("genre_ids", []),
                        "language": item.get("original_language"),
                        "release_date": item.get("release_date") or item.get("first_air_date"),
                        "rating": item.get("vote_average", 0),
                        "poster": item.get("poster_path"),
                        "type": "movie" if media_type == "movie" else "series"
                    })
        except Exception as e:
            print(f"Error searching for '{query}' ({media_type}): {e}")
    return candidates


def sync_new_releases(days_back=30, max_pages=3, dry_run=False, specific_ids=None, query=None):
    """
    Main function to discover, filter, enrich, and incrementally embed new releases.
    Supports time-based discovery, specific TMDB IDs, or title search queries.
    """
    dataset_file = "data/model_movies_v2.csv"
    if not os.path.exists(dataset_file):
        raise FileNotFoundError(f"{dataset_file} not found. Please initialize dataset first.")

    if not API_KEY:
        raise ValueError("TMDB_API_KEY environment variable is missing or empty! Please configure TMDB_API_KEY in .env or GitHub Secrets.")

    df_existing = pd.read_csv(dataset_file).fillna("")
    existing_ids = set(df_existing["tmdb_id"].astype(int))

    print(f"Catalog currently has {len(df_existing)} titles.")
    session = requests.Session()

    if specific_ids:
        print(f"Fetching {len(specific_ids)} specific TMDB IDs: {specific_ids}...")
        candidates = fetch_candidates_by_ids(session, specific_ids)
    elif query:
        print(f"Searching TMDB for: '{query}'...")
        candidates = fetch_candidates_by_query(session, query)
    else:
        print(f"Checking TMDB for releases from the last {days_back} days...")
        candidates = fetch_candidate_releases(session, days_back=days_back, max_pages=max_pages)

    print(f"Fetched {len(candidates)} raw candidates from TMDB.")

    # 1. Deduplicate against existing catalog and within the batch
    new_candidates = []
    seen_in_batch = set()
    for c in candidates:
        cid = int(c["tmdb_id"])
        if cid not in existing_ids and cid not in seen_in_batch:
            # Skip entries with no title or overview
            if c["title"] and str(c["title"]).strip() and str(c.get("description", "")).strip():
                new_candidates.append(c)
                seen_in_batch.add(cid)

    print(f"Found {len(new_candidates)} new candidate titles not yet in CineMatch.")

    if not new_candidates:
        print("CineMatch is already up-to-date! No new launches to add.")
        return 0

    # 2. Gatekeeper: Filter out daily soaps & linear TV serials
    eligible_items = []
    excluded_count = 0
    for cand in new_candidates:
        status, reason = classify_title(cand)
        if status == "EXCLUDE":
            excluded_count += 1
            print(f"  [Filtered Out] {cand['title']} ({cand['type']}): {reason}")
        else:
            eligible_items.append(cand)

    print(f"Filtered {excluded_count} serials. {len(eligible_items)} eligible movies/series to add.")

    if not eligible_items:
        print("No new eligible titles after filtering.")
        return 0

    if dry_run:
        print("Dry run mode: Exiting without saving changes.")
        for item in eligible_items:
            print(f"  • [Would Add] {item['title']} ({item['type']}, {item['language']})")
        return len(eligible_items)

    # 3. Enrich eligible items with cast, keywords, tagline
    print(f"Enriching {len(eligible_items)} new titles with cast, keywords, and metadata...")
    enriched_new_rows = []
    for item in eligible_items:
        enr = enrich_item(session, item)
        enriched_new_rows.append(enr)
        time.sleep(0.2)

    df_new = pd.DataFrame(enriched_new_rows).fillna("")

    # 4. Incremental Embedding Generation
    device = get_device()
    print(f"Loading SentenceTransformer on {device} for incremental encoding...")
    model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True, device=device)

    new_content_texts = []
    new_plot_texts = []
    new_theme_texts = []

    for _, row in df_new.iterrows():
        title = str(row["title"]).strip()
        m_type = "Movie" if str(row.get("type", "")).lower() == "movie" else "TV Series"
        genres = str(row.get("genre_names", "")).strip()
        cast = str(row.get("cast", "")).strip()
        tagline = str(row.get("tagline", "")).strip()
        keywords = str(row.get("keywords", "")).strip()
        desc = str(row.get("description", "")).strip()

        # Holistic text
        holistic = f"Title: {title}. Media: {m_type}. Genres: {genres}."
        if cast:
            holistic += f" Starring: {cast}."
        if tagline:
            holistic += f" Tagline: {tagline}."
        if keywords:
            holistic += f" Keywords: {keywords}."
        holistic += f" Overview: {desc}"
        new_content_texts.append(holistic)

        # Plot text
        p_text = f"Title: {title}."
        if tagline:
            p_text += f" Tagline: {tagline}."
        p_text += f" Overview: {desc}"
        new_plot_texts.append(p_text)

        # Theme text
        t_text = f"Media: {m_type}. Genres: {genres}."
        if keywords:
            t_text += f" Keywords: {keywords}."
        if tagline:
            t_text += f" Tagline: {tagline}."
        new_theme_texts.append(t_text)

    print("Encoding incremental embeddings...")
    new_c_emb = model.encode(new_content_texts, batch_size=32, normalize_embeddings=True, show_progress_bar=False)
    new_p_emb = model.encode(new_plot_texts, batch_size=32, normalize_embeddings=True, show_progress_bar=False)
    new_t_emb = model.encode(new_theme_texts, batch_size=32, normalize_embeddings=True, show_progress_bar=False)

    # 5. Stack with existing embeddings
    old_c_emb = np.load("models/content_embeddings.npy")
    old_p_emb = np.load("models/plot_embeddings.npy")
    old_t_emb = np.load("models/theme_embeddings.npy")

    updated_c_emb = np.vstack([old_c_emb, new_c_emb])
    updated_p_emb = np.vstack([old_p_emb, new_p_emb])
    updated_t_emb = np.vstack([old_t_emb, new_t_emb])

    np.save("models/content_embeddings.npy", updated_c_emb)
    np.save("models/plot_embeddings.npy", updated_p_emb)
    np.save("models/theme_embeddings.npy", updated_t_emb)
    np.save("models/embeddings.npy", updated_c_emb)

    # 6. Append to CSV files
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_csv("data/model_movies_v2.csv", index=False)
    df_combined.to_csv("data/enriched_movies.csv", index=False)

    # Ensure cleaned_movies.csv has matching subset
    cleaned_cols = [c for c in ["tmdb_id", "title", "description", "genres", "language", "release_date", "rating", "poster", "type"] if c in df_combined.columns]
    df_combined[cleaned_cols].to_csv("data/cleaned_movies.csv", index=False)

    print("=" * 60)
    print(f"SUCCESS: Added {len(df_new)} new titles to CineMatch!")
    print(f"Total catalog size is now: {len(df_combined)} titles.")
    print(f"Embedding shape: {updated_c_emb.shape}")
    print("=" * 60)

    for _, r in df_new.iterrows():
        print(f"  + Added: {r['title']} ({r['type']}) | Genres: {r['genre_names'][:40]} | Rating: {r['rating']}")

    return len(df_new)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatically sync new movie & series launches from TMDB into CineMatch")
    parser.add_argument("--days", type=int, default=30, help="Number of days back to check for releases (default: 30)")
    parser.add_argument("--pages", type=int, default=3, help="Max pages per category to inspect (default: 3)")
    parser.add_argument("--ids", nargs="+", type=int, help="Specific TMDB IDs to fetch and add")
    parser.add_argument("--query", type=str, help="Search query to find and add specific titles from TMDB")
    parser.add_argument("--dry-run", action="store_true", help="Inspect what would be added without modifying files")
    args = parser.parse_args()

    sync_new_releases(days_back=args.days, max_pages=args.pages, dry_run=args.dry_run, specific_ids=args.ids, query=args.query)
