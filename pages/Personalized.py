import pandas as pd
import streamlit as st
from personalized import (
    df,
    get_ratings,
    personalized_recommendations
)

USER_ID = "demo_user"

st.set_page_config(
    page_title="CineMatch - Personalized For You",
    page_icon="✨",
    layout="wide"
)

st.title("✨ Recommended for You")
st.write("Discover movies and series uniquely tailored to your taste profile.")

ratings = get_ratings(USER_ID)

st.metric("Titles rated by you", len(ratings))

content_type = st.radio(
    "Show recommendations",
    ["Both", "Movies", "Series"],
    horizontal=True
)

if ratings.empty:
    st.info(
        "Rate some movies or series first on the main page "
        "to unlock personalized recommendations."
    )
else:
    results = personalized_recommendations(
        USER_ID,
        n=12,
        content_type=content_type
    )

    if results.empty:
        st.info(
            "Rate a few titles above or below "
            "3 stars to build your taste profile."
        )
    else:
        for start in range(0, len(results), 3):
            cols = st.columns(3)

            for col, (_, movie) in zip(
                cols,
                results.iloc[start:start + 3].iterrows()
            ):
                with col:
                    if pd.notna(movie.get("poster")) and str(movie["poster"]).strip():
                        st.image(
                            "https://image.tmdb.org/t/p/w500"
                            + str(movie["poster"]).strip(),
                            use_container_width=True
                        )

                    st.subheader(movie["title"])
                    st.caption(
                        f"{movie['type'].title()} | ⭐ {movie.get('rating', 0):.1f}/10"
                    )
                    st.write(f"_{movie['genre_names']}_")
                    st.caption(
                        f"🎯 **{movie.get('match_percent', 0):.1f}% Match**"
                    )
                    with st.expander("Synopsis"):
                        st.write(movie.get("description", "No synopsis available."))