# Book Catalog Filter — Python CLI & Notebook

A small, reproducible Python project that filters books by genre. It includes a command-line tool and a self-contained notebook that works offline or in Colab. Recommendations preserve CSV order; this is not a trained recommendation model.

## Run

Python 3.10 or newer; no third-party packages are required for the command-line tool.

```sh
python3 book_recommender.py Fantasy
python3 book_recommender.py Mystery --csv data/sample_books.csv --limit 3
python3 -m unittest discover -s tests -v
```

Open `book_recommendation_system.ipynb` in Jupyter or Colab and run its cells in order. The notebook embeds the same small demo dataset, so it does not depend on a missing `/content` file.

## Bring your own data

CSV files must contain `Book`, `Author(s)` and `Genre`. A small, hand-curated metadata sample is included in `data/sample_books.csv`; it is not a ranking of bestsellers. Blank genres stay blank. Genre matching ignores case and surrounding whitespace. An unknown genre produces no matches instead of an exception.

Optional `--max-price 0` selects zero-price records only when your CSV has a numeric `Price` column. Use one currency throughout. Missing or malformed prices are excluded; the bundled sample makes no claims about price or availability.

The earlier unused classifier and misleading “free books” output were removed. Historical code remains in Git history. The notebook filename now spells “recommendation” correctly.
