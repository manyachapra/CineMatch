import ast
import re
import pandas as pd
from typing import Dict, Any, Tuple, List

from filter_config import (
    EXCLUDED_TV_GENRES,
    KNOWN_SERIAL_IDS,
    KNOWN_SERIAL_TITLES,
    KNOWN_WEB_SERIES_IDS,
    KNOWN_WEB_SERIES_TITLES,
    TV_NETWORK_PATTERNS,
    DAILY_SOAP_PATTERNS,
    OTT_PLATFORM_PATTERNS
)

GENRE_ID_NAMES = {
    10763: "News",
    10764: "Reality",
    10766: "Soap",
    10767: "Talk"
}


def normalize_title(title: str) -> str:
    """Normalize title by removing punctuation, extra spaces, and lowercasing."""
    if not title:
        return ""
    t = str(title).lower().strip()
    # Replace punctuation characters with space
    t = re.sub(r"[^\w\s]", " ", t)
    # Collapse multiple whitespaces
    t = re.sub(r"\s+", " ", t).strip()
    return t


def parse_genre_ids(genres_val: Any) -> set:
    """Extract set of genre IDs from int list, string representation, or set."""
    if isinstance(genres_val, (set, list)):
        return {int(x) for x in genres_val if str(x).isdigit()}
    if isinstance(genres_val, str):
        try:
            parsed = ast.literal_eval(genres_val)
            if isinstance(parsed, (list, set)):
                return {int(x) for x in parsed if str(x).isdigit()}
        except (ValueError, SyntaxError, TypeError):
            # Extract numbers via regex as fallback
            nums = re.findall(r"\b\d+\b", genres_val)
            return {int(x) for x in nums}
    return set()


def is_title_in_set(norm_title: str, title_set: set) -> Tuple[bool, str]:
    """Check if normalized title matches or contains a target title in the set."""
    if norm_title in title_set:
        return True, norm_title

    # Partial / substring check for longer distinct titles
    for target in title_set:
        if len(target) >= 6:
            # Word-boundary matching
            pattern = r"\b" + re.escape(target) + r"\b"
            if re.search(pattern, norm_title):
                return True, target

    return False, ""


def classify_title(record: Dict[str, Any]) -> Tuple[str, str]:
    """
    Classify a title into 'RETAIN', 'EXCLUDE', or 'UNCERTAIN'.
    
    Returns:
        status (str): 'RETAIN', 'EXCLUDE', or 'UNCERTAIN'
        reason (str): Human-readable explanation of the decision
    """
    media_type = str(record.get("type", "")).strip().lower()
    language = str(record.get("language", "")).strip().lower()

    # Rule 1: Movies and non-Hindi series are always retained
    if media_type == "movie":
        return "RETAIN", "Eligible movie"

    if language != "hi":
        return "RETAIN", f"Non-Hindi series ({language})"

    # From here, title is a Hindi television series (type == 'series' and language == 'hi')
    tmdb_id = record.get("tmdb_id")
    try:
        tmdb_id = int(tmdb_id) if tmdb_id is not None and str(tmdb_id).isdigit() else None
    except (ValueError, TypeError):
        tmdb_id = None

    raw_title = str(record.get("title", ""))
    norm_title = normalize_title(raw_title)

    desc = str(record.get("description", ""))
    keywords = str(record.get("keywords", ""))
    tagline = str(record.get("tagline", ""))
    combined_text = f"{raw_title} {desc} {keywords} {tagline}".lower()

    # Rule 2: TMDB TV Genre Filtering (Soap, Reality, Talk, News)
    genre_ids = parse_genre_ids(record.get("genres", []))
    excluded_genres = genre_ids & EXCLUDED_TV_GENRES
    if excluded_genres:
        genre_names = ", ".join(GENRE_ID_NAMES.get(gid, str(gid)) for gid in excluded_genres)
        return "EXCLUDE", f"TMDB Genre Exclusion: {genre_names}"

    # Rule 3: Protected Web Series Whitelist (TMDB ID or Title)
    if tmdb_id is not None and tmdb_id in KNOWN_WEB_SERIES_IDS:
        return "RETAIN", f"Protected web series inclusion list (TMDB ID: {tmdb_id})"

    matched_wl, wl_title = is_title_in_set(norm_title, KNOWN_WEB_SERIES_TITLES)
    if matched_wl:
        return "RETAIN", f"Protected web series inclusion list (Title: {wl_title})"

    # Rule 4: Explicit Exclusion List (TMDB ID or Title)
    if tmdb_id is not None and tmdb_id in KNOWN_SERIAL_IDS:
        return "EXCLUDE", f"Explicit exclusion list (TMDB ID: {tmdb_id})"

    matched_serial, s_title = is_title_in_set(norm_title, KNOWN_SERIAL_TITLES)
    if matched_serial:
        return "EXCLUDE", f"Explicit exclusion list (Title: {s_title})"

    # Rule 5: Metadata analysis (OTT platforms vs Linear TV networks & Daily Soap tropes)
    ott_matched = [p for p in OTT_PLATFORM_PATTERNS if re.search(p, combined_text)]
    soap_matched = [p for p in DAILY_SOAP_PATTERNS if re.search(p, combined_text)]
    tv_net_matched = [p for p in TV_NETWORK_PATTERNS if re.search(p, combined_text)]

    # If daily soap pattern matches explicitly
    if soap_matched:
        return "EXCLUDE", f"Daily soap indicator in metadata: {soap_matched[0]}"

    # If linear TV network matches and NO streaming platform is mentioned
    if tv_net_matched and not ott_matched:
        return "EXCLUDE", f"Linear TV network broadcast: {tv_net_matched[0]}"

    # If streaming platform matches and NO TV network matches
    if ott_matched and not tv_net_matched:
        return "RETAIN", f"OTT streaming platform indicator: {ott_matched[0]}"

    # Rule 6: Strict elimination of Hindi daily TV serials
    # Any Hindi television entry that is not a verified streaming original / web series is a broadcast TV serial.
    return "EXCLUDE", "Broadcast television serial / soap opera (unverified streaming release)"


def filter_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Filter dataset into:
    1. cleaned_df: Retained titles + Uncertain titles (retained pending manual review)
    2. excluded_df: Excluded Hindi serials with reasons
    3. uncertain_df: Uncertain titles flagged for manual review
    """
    cleaned_rows = []
    excluded_rows = []
    uncertain_rows = []

    for _, row in df.iterrows():
        record = row.to_dict()
        status, reason = classify_title(record)

        if status == "EXCLUDE":
            excluded_item = {
                "tmdb_id": row.get("tmdb_id"),
                "title": row.get("title"),
                "type": row.get("type"),
                "language": row.get("language"),
                "genre_names": row.get("genre_names", ""),
                "rating": row.get("rating", 0),
                "exclusion_reason": reason
            }
            excluded_rows.append(excluded_item)
        elif status == "UNCERTAIN":
            uncertain_item = {
                "tmdb_id": row.get("tmdb_id"),
                "title": row.get("title"),
                "type": row.get("type"),
                "language": row.get("language"),
                "genre_names": row.get("genre_names", ""),
                "rating": row.get("rating", 0),
                "review_reason": reason
            }
            uncertain_rows.append(uncertain_item)
            # Prioritize precision over aggressive removal: retain uncertain titles in the main dataset
            cleaned_rows.append(row)
        else:
            cleaned_rows.append(row)

    excluded_cols = ["tmdb_id", "title", "type", "language", "genre_names", "rating", "exclusion_reason"]
    uncertain_cols = ["tmdb_id", "title", "type", "language", "genre_names", "rating", "review_reason"]

    cleaned_df = pd.DataFrame(cleaned_rows).reset_index(drop=True)
    excluded_df = pd.DataFrame(excluded_rows, columns=excluded_cols).reset_index(drop=True)
    uncertain_df = pd.DataFrame(uncertain_rows, columns=uncertain_cols).reset_index(drop=True)

    return cleaned_df, excluded_df, uncertain_df
