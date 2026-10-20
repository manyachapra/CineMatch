import streamlit as st
import pandas as pd
import numpy as np
import ast
from personalized import (
    save_rating,
    get_ratings,
    personalized_recommendations
)
from recommend_v2 import (
    df,
    recommend_by_index,
    find_matching_index
)

USER_ID = "demo_user"

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide"
)

# TMDB poster URL helper
def get_poster(path):
    if pd.isna(path) or not str(path).strip():
        return None
    return f"https://image.tmdb.org/t/p/w500{str(path).strip()}"

def get_description(value):
    if pd.isna(value) or not str(value).strip():
        return "Description unavailable."
    return str(value)

def get_genres(row):
    value = row.get("genre_names", "")
    if pd.notna(value) and str(value).strip():
        return str(value).strip()
    # Fallback to genre_text if available
    alt_val = row.get("genre_text", "")
    if pd.notna(alt_val) and str(alt_val).strip():
        return str(alt_val).strip()
    return "Not available"

def get_cast(row):
    cast = row.get("cast", "")
    if pd.notna(cast) and str(cast).strip():
        return str(cast).strip()
    return ""

# Sidebar
with st.sidebar:
    st.title("🎬 CineMatch")
    st.caption("Discover your next favorite story")

    st.divider()

    content_type = st.radio(
        "What would you like to watch?",
        ["Both", "Movies", "Series"]
    )

    st.divider()

    st.write("✨ **Hybrid AI Recommendation Engine**")
    st.caption("Combines deep semantic analysis, plot arcs, thematic moods, cast affinity, and quality rankings.")
    st.write(f"Titles available: **{len(df):,}**")

# Main page
st.title("🎬 CineMatch")
st.subheader("Discover movies and series you'll love")

search = st.text_input(
    "Search for a movie or series",
    placeholder="e.g. Inception, Breaking Bad, Stranger Things, Toy Story..."
)

# Build searchable title list
if search.strip():
    matches = df[
        df["title"].str.contains(
            search.strip(),
            case=False,
            na=False,
            regex=False
        )
    ]

    if content_type == "Movies":
        matches = matches[matches["type"] == "movie"]
    elif content_type == "Series":
        matches = matches[matches["type"] == "series"]

    if matches.empty:
        st.warning("No matching titles found. Try another search term.")
        st.stop()

    options = matches.index.tolist()

    selected_index = st.selectbox(
        "Select a title",
        options,
        format_func=lambda i: (
            f"{df.loc[i, 'title']} "
            f"({df.loc[i, 'type'].title()})"
        )
    )

    selected = df.loc[selected_index]

    st.divider()

    # Selected title display
    poster_col, info_col = st.columns([1, 3])

    with poster_col:
        poster = get_poster(selected["poster"])
        if poster:
            st.image(poster, use_container_width=True)

    with info_col:
        st.header(selected["title"])
        st.write(f"**Type:** {selected['type'].title()}")
        st.write(f"**Genres:** {get_genres(selected)}")
        cast_info = get_cast(selected)
        if cast_info:
            st.write(f"**Starring:** {cast_info}")
        st.write(f"**TMDB Rating:** ⭐ {selected['rating']:.1f}/10")
        tagline = selected.get("tagline", "")
        if pd.notna(tagline) and str(tagline).strip():
            st.write(f"*\"{str(tagline).strip()}\"*")
        st.write(get_description(selected["description"]))

        st.subheader("⭐ Rate this movie or series")
        rating = st.select_slider(
            "How much did you enjoy it?",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: "⭐" * x,
            key=f"rating_{selected['type']}_{selected['tmdb_id']}"
        )
        if st.button("Save Rating"):
            save_rating(
                USER_ID,
                selected_index,
                rating
            )
            st.success("Rating saved successfully!")

    st.divider()

    st.header("✨ Recommended for You")

    # Generate hybrid optimized recommendations
    results_df = recommend_by_index(
        selected_index,
        n=12,
        content_type=content_type
    )

    if results_df.empty:
        st.info("No recommendations found matching your criteria.")
    else:
        # Display recommendation cards in a 4-column responsive grid
        rows = [results_df.iloc[i:i + 4] for i in range(0, len(results_df), 4)]
        for row_chunk in rows:
            columns = st.columns(len(row_chunk))
            for col, (_, movie) in zip(columns, row_chunk.iterrows()):
                with col:
                    poster = get_poster(movie["poster"])
                    if poster:
                        st.image(poster, use_container_width=True)

                    st.markdown(f"**{movie['title']}**")
                    st.caption(
                        f"{movie['type'].title()} | ⭐ {movie['rating']:.1f}/10"
                    )
                    st.caption(f"🎯 **{movie['match_percent']}% Match**")
                    st.caption(f"_{movie['genre_names']}_")

                    with st.expander("Details"):
                        if pd.notna(movie.get("cast")) and str(movie["cast"]).strip():
                            st.write(f"**Cast:** {movie['cast']}")
                        st.write(get_description(movie["description"]))

else:
    st.info(
        "Search for a movie or series to get smart, personalized recommendations."
    )