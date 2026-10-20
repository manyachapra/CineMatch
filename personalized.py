import sqlite3
import numpy as np
import pandas as pd

DB_PATH = "data/ratings.db"

df = pd.read_csv("data/model_movies_v2.csv").fillna("")
content = np.load("models/content_embeddings.npy")
plot = np.load("models/plot_embeddings.npy")
themes = np.load("models/theme_embeddings.npy")

assert len(df) == len(content) == len(plot) == len(themes)

# Multi-facet feature representation: holistic (50%) + theme/vibe (30%) + plot (20%)
features = np.concatenate(
    [
        content * np.sqrt(0.50),
        themes * np.sqrt(0.30),
        plot * np.sqrt(0.20),
    ],
    axis=1
)

features = features / np.maximum(
    np.linalg.norm(features, axis=1, keepdims=True),
    1e-8
)

# Quality prior based on TMDB rating
ratings_arr = df["rating"].to_numpy(dtype=float)
quality_bonus = 0.05 * np.clip((ratings_arr - 4.0) / 5.5, -0.5, 1.0)


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ratings (
                    user_id TEXT NOT NULL,
                    tmdb_id INTEGER NOT NULL,
                    media_type TEXT NOT NULL,
                    rating INTEGER NOT NULL
                        CHECK(rating BETWEEN 1 AND 5),
                    PRIMARY KEY(user_id, tmdb_id, media_type)
                )
            """)
    finally:
        conn.close()


def save_rating(user_id, index, rating):
    movie = df.iloc[index]
    conn = get_connection()
    try:
        with conn:
            conn.execute("""
                INSERT INTO ratings
                    (user_id, tmdb_id, media_type, rating)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id, tmdb_id, media_type)
                DO UPDATE SET rating = excluded.rating
            """, (
                str(user_id),
                int(movie["tmdb_id"]),
                str(movie["type"]),
                int(rating)
            ))
    finally:
        conn.close()


def get_ratings(user_id):
    conn = get_connection()
    try:
        return pd.read_sql_query(
            "SELECT * FROM ratings WHERE user_id = ?",
            conn,
            params=(str(user_id),)
        )
    finally:
        conn.close()


def personalized_recommendations(
    user_id, n=12, content_type="Both"
):
    ratings = get_ratings(user_id)

    if ratings.empty:
        return pd.DataFrame()

    # Match ratings to the current dataset
    rated = df.reset_index().merge(
        ratings,
        on=["tmdb_id"],
        how="inner",
        suffixes=("", "_user")
    )

    rated = rated[
        rated["type"] == rated["media_type"]
    ]

    if rated.empty:
        return pd.DataFrame()

    indices = rated["index"].to_numpy(dtype=int)
    values = rated["rating_user"].to_numpy(dtype=float)

    # Ratings above 3 are positive;
    # ratings below 3 are negative.
    weights = values - 3.0

    if np.all(weights == 0):
        return pd.DataFrame()

    # Build the user's preference vector
    profile = np.average(
        features[indices],
        axis=0,
        weights=np.abs(weights)
        if np.all(weights >= 0)
        else None
    ) if np.all(weights >= 0) else (
        weights @ features[indices]
        / np.sum(np.abs(weights))
    )

    norm = np.linalg.norm(profile)

    if norm < 1e-8:
        return pd.DataFrame()

    profile /= norm

    scores = features @ profile + quality_bonus

    # Exclude everything the user has rated
    scores[indices] = -np.inf

    if content_type != "Both":
        target = (
            "movie" if content_type.lower() in ["movies", "movie"]
            else "series"
        )
        scores[df["type"].str.lower().to_numpy() != target] = -np.inf

    top = np.argsort(scores)[::-1]
    top = [i for i in top if np.isfinite(scores[i])][:n]

    results = df.iloc[top][
        ["title", "type", "genre_names", "poster", "rating", "description"]
    ].copy()

    results["match_score"] = scores[top].round(3)
    results["match_percent"] = np.clip(scores[top] * 100, 0, 100).round(1)

    return results


initialize_database()