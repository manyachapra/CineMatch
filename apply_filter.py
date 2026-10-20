import os
import shutil
import pandas as pd
from serial_filter import filter_dataset

def main():
    print("=" * 60)
    print("CineMatch Hindi Daily TV Serial Filtering Pipeline")
    print("=" * 60)

    # 1. Back up original datasets
    backups = [
        ("data/cinematch_titles.csv", "data/cinematch_titles_backup.csv"),
        ("data/cleaned_movies.csv", "data/cleaned_movies_backup.csv"),
        ("data/enriched_movies.csv", "data/enriched_movies_backup.csv"),
        ("data/model_movies_v2.csv", "data/model_movies_v2_backup.csv"),
    ]

    for src, dst in backups:
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Created backup: {src} -> {dst}")
        elif os.path.exists(dst):
            print(f"Backup already preserved: {dst}")

    # 2. Load dataset (prefer backup to ensure idempotency across multiple runs)
    source_file = "data/model_movies_v2_backup.csv"
    if not os.path.exists(source_file):
        source_file = "data/enriched_movies_backup.csv"
    if not os.path.exists(source_file):
        source_file = "data/model_movies_v2.csv"

    df = pd.read_csv(source_file).fillna("")
    total_before = len(df)
    print(f"\nLoaded {total_before} titles before filtering.")

    # 3. Apply intelligent filtering
    cleaned_df, excluded_df, uncertain_df = filter_dataset(df)

    # 4. Save outputs
    os.makedirs("data", exist_ok=True)

    # Output 1: Cleaned dataset
    cleaned_df.to_csv("data/model_movies_v2.csv", index=False)
    cleaned_df.to_csv("data/enriched_movies.csv", index=False)
    # Also update cleaned_movies.csv for pipeline consistency
    cleaned_cols = [c for c in ["tmdb_id", "title", "description", "genres", "language", "release_date", "rating", "poster", "type"] if c in cleaned_df.columns]
    cleaned_df[cleaned_cols].to_csv("data/cleaned_movies.csv", index=False)

    # Output 2: Excluded serials
    excluded_df.to_csv("data/excluded_serials.csv", index=False)

    # Output 3: Uncertain titles
    uncertain_df.to_csv("data/uncertain_titles.csv", index=False)

    print("\n" + "-" * 50)
    print(f"Total titles before filtering : {total_before}")
    print(f"Hindi daily serials removed   : {len(excluded_df)}")
    print(f"Titles flagged for review     : {len(uncertain_df)}")
    print(f"Total titles remaining        : {len(cleaned_df)}")
    print("-" * 50)

    print("\nSample Excluded Hindi Daily Serials:")
    for _, r in excluded_df.head(8).iterrows():
        print(f"  • {r['title']} (TMDB {r['tmdb_id']}): {r['exclusion_reason']}")

    print("\nSample Uncertain Titles Retained for Review:")
    for _, r in uncertain_df.head(5).iterrows():
        print(f"  • {r['title']} (TMDB {r['tmdb_id']}): {r['review_reason']}")

    print("\nSaved:")
    print("  1. Cleaned dataset  -> data/model_movies_v2.csv")
    print("  2. Excluded serials -> data/excluded_serials.csv")
    print("  3. Uncertain titles -> data/uncertain_titles.csv")


if __name__ == "__main__":
    main()
