"""Small, offline genre-based book recommender; no trained model required."""
import argparse
import csv
from pathlib import Path

REQUIRED_COLUMNS = {"Book", "Author(s)", "Genre"}


def load_books(source):
    """Read a CSV path or text stream and validate its required columns."""
    if hasattr(source, "read"):
        reader = csv.DictReader(source)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing CSV columns: " + ", ".join(sorted(missing)))
        return [{key: (value or "").strip() for key, value in row.items()
                 if key is not None} for row in reader]
    with Path(source).open(encoding="utf-8-sig", newline="") as handle:
        return load_books(handle)


def recommend_books(books, genre, num_recommendations=5, *, max_price=None):
    """Return matching rows in source order. Unknown genres return an empty list.

    Optional price filtering requires a numeric Price column in the source currency.
    Missing/invalid prices are excluded, never assumed to mean free.
    """
    if not isinstance(genre, str) or not genre.strip():
        raise ValueError("Enter a non-empty genre.")
    if (isinstance(num_recommendations, bool)
            or not isinstance(num_recommendations, int) or num_recommendations < 1):
        raise ValueError("Number of recommendations must be a positive integer.")
    if max_price is not None:
        import math
        if not math.isfinite(max_price) or max_price < 0:
            raise ValueError("Maximum price must be a finite non-negative number.")
        if not books or not all("Price" in book for book in books):
            raise ValueError("Price filtering requires a Price column in the CSV.")
    matches = []
    for book in books:
        if (book.get("Genre") or "").strip().casefold() != genre.strip().casefold():
            continue
        if not book.get("Book"):
            continue
        if max_price is not None:
            try:
                price = float(book["Price"])
            except (ValueError, TypeError):
                continue
            if not 0 <= price <= max_price:
                continue
        matches.append(book)
        if len(matches) >= num_recommendations:
            break
    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("genre", help="Genre, e.g. Fantasy")
    parser.add_argument("--csv", type=Path,
                        default=Path(__file__).parent / "data" / "sample_books.csv")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--max-price", type=float, default=None,
                        help="Requires a numeric Price column; 0 selects free entries")
    args = parser.parse_args()
    try:
        books = load_books(args.csv)
        matches = recommend_books(books, args.genre, args.limit, max_price=args.max_price)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")
    if not matches:
        print("No matching books. Available genres: " + ", ".join(sorted(
            {book["Genre"] for book in books if book["Genre"]})))
    for book in matches:
        print(f"{book['Book']} — {book['Author(s)']} ({book['Genre']})")


if __name__ == "__main__":
    main()
