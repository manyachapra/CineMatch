import os
import ast
import time
import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer

# Ensure offline operation so HF doesn't wait on network retries
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

print("Starting CineMatch Model Training...")
start_time = time.time()

# Load cleaned & enriched dataset
data_path = "data/enriched_movies.csv" if os.path.exists("data/enriched_movies.csv") else "data/model_movies_v2.csv"
df = pd.read_csv(data_path).fillna("")
print(f"Loaded {len(df)} titles from {data_path}")

# Detect best available compute device
if torch.backends.mps.is_available():
    device = "mps"
elif torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"
print(f"Using compute device: {device}")

# 1. Holistic content text: combines Title, Media Type, Genres, Cast, Tagline, Keywords, and Overview
content_texts = []
# 2. Narrative/plot text: focused on Title, Tagline, and Overview
plot_texts = []
# 3. Thematic text: focused on Media Type, Genres, Keywords, and Tagline
theme_texts = []

for _, row in df.iterrows():
    title = str(row["title"]).strip()
    m_type = "Movie" if str(row.get("type", "")).lower() == "movie" else "TV Series"
    genres = str(row.get("genre_names", "")).strip()
    cast = str(row.get("cast", "")).strip()
    tagline = str(row.get("tagline", "")).strip()
    keywords = str(row.get("keywords", "")).strip()
    desc = str(row.get("description", "")).strip()

    # Holistic text for cross-feature dense representation
    holistic = f"Title: {title}. Media: {m_type}. Genres: {genres}."
    if cast:
        holistic += f" Starring: {cast}."
    if tagline:
        holistic += f" Tagline: {tagline}."
    if keywords:
        holistic += f" Keywords: {keywords}."
    holistic += f" Overview: {desc}"
    content_texts.append(holistic)

    # Narrative/plot representation
    p_text = f"Title: {title}."
    if tagline:
        p_text += f" Tagline: {tagline}."
    p_text += f" Overview: {desc}"
    plot_texts.append(p_text)

    # Theme and mood representation
    t_text = f"Media: {m_type}. Genres: {genres}."
    if keywords:
        t_text += f" Keywords: {keywords}."
    if tagline:
        t_text += f" Tagline: {tagline}."
    theme_texts.append(t_text)

# Initialize sentence transformer
model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True, device=device)

print("Encoding holistic content embeddings...")
content_embeddings = model.encode(
    content_texts,
    batch_size=64,
    normalize_embeddings=True,
    show_progress_bar=True
)

print("Encoding plot embeddings...")
plot_embeddings = model.encode(
    plot_texts,
    batch_size=64,
    normalize_embeddings=True,
    show_progress_bar=True
)

print("Encoding theme embeddings...")
theme_embeddings = model.encode(
    theme_texts,
    batch_size=64,
    normalize_embeddings=True,
    show_progress_bar=True
)

os.makedirs("models", exist_ok=True)

np.save("models/content_embeddings.npy", content_embeddings)
np.save("models/plot_embeddings.npy", plot_embeddings)
np.save("models/theme_embeddings.npy", theme_embeddings)

# For backward compatibility with any legacy code that expects single embeddings.npy:
np.save("models/embeddings.npy", content_embeddings)

df.to_csv("data/model_movies_v2.csv", index=False)

elapsed = time.time() - start_time
print(f"Training successfully completed in {elapsed:.1f}s!")
print(f"Generated {len(df)} embeddings across 3 feature representations.")