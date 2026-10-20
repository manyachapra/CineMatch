import pandas as pd
from serial_filter import filter_dataset

df = pd.read_csv("data/cinematch_titles.csv")

print("Dataset shape before preprocessing:", df.shape)
print("\nMissing values:")
print(df.isnull().sum())

print("\nMovies vs TV series:")
print(df["type"].value_counts())

print("\nLanguages:")
print(df["language"].value_counts())

# Remove duplicate titles within each media type
df = df.drop_duplicates(
    subset=["tmdb_id", "type"]
)

# Remove entries without descriptions
df = df.dropna(subset=["title", "description"])
df = df[df["description"].str.strip() != ""]

# Fill missing genres
df["genres"] = df["genres"].fillna("[]")

# Convert dates
df["release_date"] = pd.to_datetime(
    df["release_date"], errors="coerce"
)

# Remove unreleased titles
today = pd.Timestamp.today().normalize()
df = df[df["release_date"] <= today]

# Intelligent filtering: Remove Hindi daily TV serials and flag uncertain titles
cleaned_df, excluded_df, uncertain_df = filter_dataset(df)

cleaned_df.to_csv(
    "data/cleaned_movies.csv",
    index=False
)
excluded_df.to_csv(
    "data/excluded_serials.csv",
    index=False
)
uncertain_df.to_csv(
    "data/uncertain_titles.csv",
    index=False
)

print("\nFiltering Results:")
print("Cleaned dataset:", cleaned_df.shape)
print("Excluded serials:", excluded_df.shape)
print("Uncertain titles flagged for review:", uncertain_df.shape)