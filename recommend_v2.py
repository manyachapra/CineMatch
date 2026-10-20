import ast
import numpy as np
import pandas as pd

# Load dataset and precomputed embeddings
df = pd.read_csv("data/model_movies_v2.csv").fillna("")
content_emb = np.load("models/content_embeddings.npy")
plot_emb = np.load("models/plot_embeddings.npy")
theme_emb = np.load("models/theme_embeddings.npy")

def _parse_genres(value):
    try:
        return set(ast.literal_eval(value))
    except (ValueError, SyntaxError, TypeError):
        return set()

genre_sets = df["genres"].apply(_parse_genres).tolist()

# Precompute actor name sets for fast overlap checks
def _parse_cast(val):
    if not val:
        return set()
    # Clean and split into individual words or full tokens
    return set(str(val).lower().split())

cast_sets = df["cast"].apply(_parse_cast).tolist()

# Quality rating prior: slight positive weight for critically acclaimed titles
ratings = df["rating"].to_numpy(dtype=float)
rating_norm = np.clip((ratings - 4.0) / 5.5, -0.5, 1.0)
rating_bonus = 0.05 * rating_norm


def find_matching_index(title: str):
    """Find index of the movie matching the given title using multi-tier search."""
    clean_title = title.strip()
    if not clean_title:
        return None

    # Tier 1: Exact case-insensitive match
    exact = df[df["title"].str.casefold() == clean_title.casefold()]
    if not exact.empty:
        return exact.index[0]

    # Tier 2: Substring match (e.g. 'Inception' in 'Inception')
    contains = df[df["title"].str.contains(clean_title, case=False, na=False, regex=False)]
    if not contains.empty:
        return contains.index[0]

    # Tier 3: Word token overlap
    tokens = set(clean_title.casefold().split())
    best_idx = None
    best_overlap = 0
    for idx, row_title in enumerate(df["title"]):
        row_tokens = set(str(row_title).casefold().split())
        overlap = len(tokens & row_tokens)
        if overlap > best_overlap:
            best_overlap = overlap
            best_idx = idx

    if best_overlap > 0:
        return best_idx

    return None


def recommend(title: str, n: int = 10, content_type: str = "both"):
    """
    Generate optimized movie and series recommendations.
    
    Parameters:
        title (str): Title of the movie or series.
        n (int): Number of recommendations to return.
        content_type (str): 'both', 'movies' (or 'movie'), or 'series'.
    """
    idx = find_matching_index(title)
    if idx is None:
        print(f"Title '{title}' not found.")
        return pd.DataFrame()

    return recommend_by_index(idx, n=n, content_type=content_type)


def recommend_by_index(idx: int, n: int = 10, content_type: str = "both"):
    """
    Generate recommendations given a movie index in the dataset.
    """
    # 1. Holistic content similarity (captures title, cast, genres, overview simultaneously)
    c_scores = content_emb @ content_emb[idx]

    # 2. Thematic & keyword similarity
    t_scores = theme_emb @ theme_emb[idx]

    # 3. Narrative/plot similarity
    p_scores = plot_emb @ plot_emb[idx]

    # 4. Genre Jaccard similarity
    source_genres = genre_sets[idx]
    if source_genres:
        g_scores = np.array([
            len(source_genres & g) / len(source_genres | g) if (source_genres | g) else 0.0
            for g in genre_sets
        ])
    else:
        g_scores = np.zeros(len(df))

    # 5. Cast overlap bonus
    source_cast = cast_sets[idx]
    if source_cast:
        cast_scores = np.array([
            len(source_cast & c) / max(len(source_cast | c), 1)
            for c in cast_sets
        ])
    else:
        cast_scores = np.zeros(len(df))

    # Composite hybrid score:
    # 0.40 holistic semantic + 0.25 theme + 0.15 narrative + 0.10 genre + 0.05 cast + quality bonus
    scores = (
        0.40 * c_scores +
        0.25 * t_scores +
        0.15 * p_scores +
        0.10 * g_scores +
        0.05 * cast_scores +
        rating_bonus
    )

    # Soft penalty for 0 genre overlap when target movie has known genres
    if source_genres:
        zero_genre_mask = (g_scores == 0)
        scores[zero_genre_mask] -= 0.12

    # Prevent recommending the query movie itself
    scores[idx] = -999.0

    # Content type filter
    ct_clean = content_type.strip().lower()
    if ct_clean in ["movie", "movies"]:
        scores[df["type"].str.lower() != "movie"] = -999.0
    elif ct_clean in ["series", "tv", "tv series"]:
        scores[df["type"].str.lower() != "series"] = -999.0

    top = np.argsort(scores)[::-1]
    top = [i for i in top if scores[i] > -100][:n]

    results = df.iloc[top][[
        "title", "type", "genre_names",
        "keywords", "cast", "rating", "poster", "description"
    ]].copy()

    # Convert score to a user-friendly 0-100% match score
    match_pct = np.clip(scores[top] * 100, 0, 100)
    results["match_score"] = scores[top].round(3)
    results["match_percent"] = match_pct.round(1)

    return results


if __name__ == "__main__":
    test_title = input("Enter a movie or series: ")
    res = recommend(test_title, n=10, content_type="both")
    if not res.empty:
        print(res[["title", "type", "genre_names", "rating", "match_score"]].to_string(index=False))