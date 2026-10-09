import io
import unittest
from book_recommender import load_books, recommend_books

class RecommenderTests(unittest.TestCase):
    def setUp(self):
        self.books = load_books(io.StringIO(
            "Book,Author(s),Genre,Price\nA,One,Fantasy,0\nB,Two,Fantasy,12\nC,Three,,\n"))

    def test_case_and_whitespace(self):
        self.assertEqual(len(recommend_books(self.books, " fantasy ")), 2)

    def test_unknown_genre_is_empty(self):
        self.assertEqual(recommend_books(self.books, "unknown"), [])

    def test_limit(self):
        self.assertEqual(len(recommend_books(self.books, "Fantasy", 1)), 1)

    def test_free_means_zero_price(self):
        self.assertEqual([b["Book"] for b in recommend_books(
            self.books, "Fantasy", max_price=0)], ["A"])

    def test_missing_price_column(self):
        with self.assertRaisesRegex(ValueError, "Price column"):
            recommend_books([{"Book": "A", "Genre": "Fantasy"}], "Fantasy", max_price=0)

    def test_bad_prices_excluded(self):
        for value in ("", "unknown", "nan", "inf", "-1"):
            self.books[0]["Price"] = value
            self.assertEqual(recommend_books(self.books, "Fantasy", max_price=0), [])

    def test_bad_inputs(self):
        for count in (0, -1, True, 1.2):
            with self.assertRaises(ValueError):
                recommend_books(self.books, "Fantasy", count)
        with self.assertRaises(ValueError):
            recommend_books(self.books, "  ")
        with self.assertRaises(ValueError):
            recommend_books(self.books, "Fantasy", max_price=float('nan'))

    def test_schema(self):
        with self.assertRaisesRegex(ValueError, "Missing CSV columns"):
            load_books(io.StringIO("title,genre\nA,Fantasy\n"))

if __name__ == '__main__':
    unittest.main()
