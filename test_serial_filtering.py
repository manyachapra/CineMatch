import os
import sqlite3
import unittest
import numpy as np
import pandas as pd

from serial_filter import classify_title, filter_dataset, normalize_title
from personalized import personalized_recommendations, save_rating, get_ratings


class TestSerialFiltering(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cleaned_path = "data/model_movies_v2.csv"
        cls.excluded_path = "data/excluded_serials.csv"
        cls.uncertain_path = "data/uncertain_titles.csv"
        cls.backup_path = "data/model_movies_v2_backup.csv"

        if not os.path.exists(cls.backup_path):
            cls.backup_path = "data/model_movies_v2.csv"

        cls.orig_df = pd.read_csv(cls.backup_path).fillna("")

        # Ensure pipeline output files exist and are valid
        need_regenerate = False
        for path in [cls.cleaned_path, cls.excluded_path, cls.uncertain_path]:
            if not os.path.exists(path) or os.path.getsize(path) < 10:
                need_regenerate = True
                break

        if need_regenerate:
            cleaned, excluded, uncertain = filter_dataset(cls.orig_df)
            cleaned.to_csv(cls.cleaned_path, index=False)
            excluded.to_csv(cls.excluded_path, index=False)
            uncertain.to_csv(cls.uncertain_path, index=False)

        cls.cleaned_df = pd.read_csv(cls.cleaned_path).fillna("")
        cls.excluded_df = pd.read_csv(cls.excluded_path).fillna("")
        cls.uncertain_df = pd.read_csv(cls.uncertain_path).fillna("")
        cls.orig_df = pd.read_csv(cls.backup_path).fillna("")

    def test_known_hindi_daily_serials_excluded(self):
        """Verify known Hindi daily serials are excluded by classification and absent from cleaned dataset."""
        must_exclude_samples = [
            "Anupamaa",
            "Yeh Rishta Kya Kehlata Hai",
            "Kumkum Bhagya",
            "Kundali Bhagya",
            "Ghum Hai Kisikey Pyaar Meiin",
            "Taarak Mehta Ka Ooltah Chashmah",
            "Bhagya Lakshmi",
            "Saath Nibhaana Saathiya 2",
            "Kyunki Saas Bhi Kabhi Bahu Thi",
            "Kasautii Zindagii Kay",
            "Balika Vadhu",
            "Uttaran",
            "Imlie",
            "Dil Se Dil Tak",
            "Chookar Mere Maan Ko",
            "Yeh Un Dinon Ki Baat Hai"
        ]

        for title in must_exclude_samples:
            status, reason = classify_title({"title": title, "type": "series", "language": "hi"})
            self.assertEqual(status, "EXCLUDE", f"Expected '{title}' to be classified as EXCLUDE, got {status} ({reason})")

            # Check that it is NOT in the cleaned dataset
            matches = self.cleaned_df[self.cleaned_df["title"].str.casefold() == title.casefold()]
            self.assertEqual(len(matches), 0, f"Daily serial '{title}' should not be present in cleaned dataset")

    def test_known_hindi_web_series_retained(self):
        """Verify known Hindi web series are retained and protected."""
        must_preserve_samples = [
            "Panchayat",
            "Mirzapur",
            "Mismatched",
            "The Family Man",
            "Sacred Games",
            "Paatal Lok",
            "Asur",
            "Farzi",
            "Guns & Gulaabs",
            "Special Ops",
            "Dahaad",
            "CAT",
            "Aspirants"
        ]

        for title in must_preserve_samples:
            matches = self.cleaned_df[self.cleaned_df["title"].str.casefold() == title.casefold()]
            self.assertGreater(len(matches), 0, f"Web series '{title}' must be retained in cleaned dataset")

            # Verify classification logic explicitly retains it
            row = matches.iloc[0].to_dict()
            status, reason = classify_title(row)
            self.assertEqual(status, "RETAIN", f"Expected '{title}' to be RETAIN, got {status} ({reason})")

    def test_hollywood_and_bollywood_movies_retained(self):
        """Verify 100% of eligible movies (Hollywood and Bollywood) are retained."""
        orig_movies = self.orig_df[self.orig_df["type"] == "movie"]
        cleaned_movies = self.cleaned_df[self.cleaned_df["type"] == "movie"]

        self.assertEqual(len(orig_movies), len(cleaned_movies), "All eligible movies must be preserved without loss")

        # Specific landmark movie checks
        for title in ["Inception", "Interstellar", "The Dark Knight", "Toy Story"]:
            matches = cleaned_movies[cleaned_movies["title"].str.contains(title, case=False, na=False)]
            self.assertGreater(len(matches), 0, f"Expected movie '{title}' to be in cleaned dataset")

    def test_english_language_web_series_retained(self):
        """Verify English-language and foreign web series are retained."""
        orig_en = self.orig_df[(self.orig_df["type"] == "series") & (self.orig_df["language"] != "hi")]
        cleaned_en = self.cleaned_df[(self.cleaned_df["type"] == "series") & (self.cleaned_df["language"] != "hi")]

        self.assertEqual(len(orig_en), len(cleaned_en), "All non-Hindi web series must be preserved")

        for title in ["Stranger Things", "The Summer I Turned Pretty", "Breaking Bad"]:
            matches = cleaned_en[cleaned_en["title"].str.contains(title, case=False, na=False)]
            self.assertGreater(len(matches), 0, f"Expected English series '{title}' to be in cleaned dataset")

    def test_uncertain_titles_flagged_appropriately(self):
        """Verify uncertain titles tracking works and schema is maintained."""
        self.assertTrue(os.path.exists(self.uncertain_path), "uncertain_titles.csv must exist")

        # Check required columns
        for col in ["tmdb_id", "title", "review_reason"]:
            self.assertIn(col, self.uncertain_df.columns)

        # Verify any uncertain titles are retained in cleaned dataset pending manual review
        for _, r in self.uncertain_df.iterrows():
            matches = self.cleaned_df[self.cleaned_df["tmdb_id"] == r["tmdb_id"]]
            self.assertEqual(len(matches), 1, f"Uncertain title '{r['title']}' should be retained pending review")

    def test_off_campus_recommendations_have_no_daily_soaps(self):
        """Verify that searching / recommending for Off Campus does not return daily soaps."""
        import recommend_v2
        recs = recommend_v2.recommend("Off Campus", n=10)
        self.assertFalse(recs.empty, "Expected recommendations for Off Campus")
        rec_titles = recs["title"].tolist()
        for banned in ["Dil Se Dil Tak", "Chookar Mere Maan Ko", "Yeh Un Dinon Ki Baat Hai", "Anupamaa", "Kumkum Bhagya"]:
            self.assertNotIn(banned, rec_titles, f"Banned daily serial '{banned}' appeared in Off Campus recommendations")

    def test_existing_user_ratings_remain_intact(self):
        """Verify SQLite database ratings are intact and unharmed."""
        db_path = "data/ratings.db"
        self.assertTrue(os.path.exists(db_path), "ratings.db must exist")

        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ratings'")
            self.assertIsNotNone(cursor.fetchone(), "ratings table must exist in SQLite database")

            ratings = pd.read_sql_query("SELECT * FROM ratings", conn)
            self.assertFalse(ratings.empty, "Existing user ratings should be preserved")
        finally:
            conn.close()

    def test_dataset_rows_and_embeddings_aligned(self):
        """Verify perfect 1:1 alignment between dataset rows and embedding matrices."""
        c_emb = np.load("models/content_embeddings.npy")
        p_emb = np.load("models/plot_embeddings.npy")
        t_emb = np.load("models/theme_embeddings.npy")
        legacy_emb = np.load("models/embeddings.npy")

        df_len = len(self.cleaned_df)
        self.assertEqual(df_len, len(c_emb), "content_embeddings row count must match dataset length")
        self.assertEqual(df_len, len(p_emb), "plot_embeddings row count must match dataset length")
        self.assertEqual(df_len, len(t_emb), "theme_embeddings row count must match dataset length")
        self.assertEqual(df_len, len(legacy_emb), "embeddings.npy row count must match dataset length")

    def test_personalized_recommendations_exclude_removed_titles(self):
        """Verify personalized recommendations never recommend excluded serials."""
        # Insert a temporary test rating for Kundali Bhagya (tmdb_id 75282 - excluded)
        test_uid = "unit_test_user"
        conn1 = sqlite3.connect("data/ratings.db")
        try:
            conn1.execute("INSERT OR REPLACE INTO ratings (user_id, tmdb_id, media_type, rating) VALUES (?, ?, ?, ?)",
                          (test_uid, 75282, "series", 5))
            conn1.commit()
        finally:
            conn1.close()

        try:
            # Generate recommendations
            recs = personalized_recommendations(test_uid, n=10, content_type="Both")

            # Check that Kundali Bhagya is NOT in recs
            if not recs.empty:
                matches = recs[recs["title"].str.casefold() == "kundali bhagya"]
                self.assertEqual(len(matches), 0, "Personalized recommendations should not include excluded serials")

                # Verify all recommended titles exist in cleaned dataset
                for title in recs["title"]:
                    in_cleaned = self.cleaned_df["title"].str.casefold() == title.casefold()
                    self.assertTrue(in_cleaned.any(), f"Recommended title '{title}' must be in cleaned dataset")
        finally:
            conn2 = sqlite3.connect("data/ratings.db")
            try:
                conn2.execute("DELETE FROM ratings WHERE user_id = ?", (test_uid,))
                conn2.commit()
            finally:
                conn2.close()

    def test_filtering_reproducibility_and_no_duplicates(self):
        """Verify filtering is deterministic, reproducible, and has no duplicates."""
        cleaned1, excluded1, uncertain1 = filter_dataset(self.orig_df)
        cleaned2, excluded2, uncertain2 = filter_dataset(self.orig_df)

        self.assertEqual(len(cleaned1), len(cleaned2), "Filtering should be deterministic")
        self.assertEqual(len(excluded1), len(excluded2), "Exclusions should be deterministic")
        self.assertEqual(len(uncertain1), len(uncertain2), "Uncertain counts should be deterministic")

        # Check for duplicates
        duplicates = cleaned1.duplicated(subset=["tmdb_id", "type"])
        self.assertFalse(duplicates.any(), "Cleaned dataset should not contain duplicate titles")


if __name__ == "__main__":
    unittest.main()
