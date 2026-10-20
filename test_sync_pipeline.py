import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock

from serial_filter import classify_title


class TestSyncPipeline(unittest.TestCase):

    def test_gatekeeper_filters_daily_soaps_during_sync(self):
        """Verify candidate new serials from TMDB discover are blocked before ingestion."""
        mock_candidates = [
            {"tmdb_id": 999901, "title": "Yeh Rishta Naya Season", "type": "series", "language": "hi", "genres": [10766]},
            {"tmdb_id": 999902, "title": "Anupamaa Special", "type": "series", "language": "hi", "genres": [18]},
            {"tmdb_id": 999903, "title": "Dune: Prophecy", "type": "series", "language": "en", "genres": [18, 10765]},
            {"tmdb_id": 999904, "title": "Panchayat Season 4", "type": "series", "language": "hi", "genres": [35, 18]}
        ]

        results = []
        for cand in mock_candidates:
            status, reason = classify_title(cand)
            results.append((cand["title"], status))

        self.assertEqual(results[0], ("Yeh Rishta Naya Season", "EXCLUDE"))
        self.assertEqual(results[1], ("Anupamaa Special", "EXCLUDE"))
        self.assertEqual(results[2], ("Dune: Prophecy", "RETAIN"))
        self.assertEqual(results[3], ("Panchayat Season 4", "RETAIN"))

    def test_incremental_embedding_stacking(self):
        """Verify np.vstack preserves vector dimensionalities and row counts."""
        # Simulated existing embeddings (N x 384)
        n_existing = 50
        dim = 384
        existing_emb = np.random.randn(n_existing, dim).astype(np.float32)
        existing_emb /= np.linalg.norm(existing_emb, axis=1, keepdims=True)

        # Simulated new embeddings (K x 384)
        n_new = 5
        new_emb = np.random.randn(n_new, dim).astype(np.float32)
        new_emb /= np.linalg.norm(new_emb, axis=1, keepdims=True)

        updated_emb = np.vstack([existing_emb, new_emb])

        self.assertEqual(updated_emb.shape, (n_existing + n_new, dim))
        # Ensure existing vectors remain identical
        np.testing.assert_array_almost_equal(updated_emb[:n_existing], existing_emb)
        # Ensure new vectors are accurately appended
        np.testing.assert_array_almost_equal(updated_emb[n_existing:], new_emb)


if __name__ == "__main__":
    unittest.main()
