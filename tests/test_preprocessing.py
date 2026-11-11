import pandas as pd
import pytest

from recommender.preprocessing import clean_reviews, latest_reviews, normalize_text


def _reviews(rows):
    return pd.DataFrame(rows, columns=["review_id", "business_id", "text", "date"])


def _many(business_id, n, text="A perfectly fine review of the food here", date="2020-01-01"):
    return [(f"{business_id}-{i}", business_id, f"{text} #{i}", date) for i in range(n)]


def test_drops_duplicate_texts():
    rows = _many("a", 15) + [("dup", "a", "A perfectly fine review of the food here #0", "2020-01-01")]
    out = clean_reviews(_reviews(rows), min_reviews=1)
    assert len(out) == 15


def test_drops_short_reviews():
    rows = _many("a", 3) + [("short", "a", "Too short", "2020-01-01")]
    out = clean_reviews(_reviews(rows), min_reviews=1)
    assert "short" not in set(out["review_id"])


def test_drops_reviews_before_min_date():
    rows = _many("a", 3) + [("old", "a", "An old review from long ago, before 2015", "2012-06-01")]
    out = clean_reviews(_reviews(rows), min_reviews=1)
    assert "old" not in set(out["review_id"])


def test_drops_restaurants_with_too_few_reviews():
    rows = _many("big", 15) + _many("small", 14)
    out = clean_reviews(_reviews(rows), min_reviews=15)
    assert set(out["business_id"]) == {"big"}


def test_min_reviews_counts_after_other_filters():
    # 15 reviews, but one is a duplicate: only 14 remain, so the restaurant goes.
    rows = _many("a", 14) + [("dup", "a", "A perfectly fine review of the food here #0", "2020-01-01")]
    out = clean_reviews(_reviews(rows), min_reviews=15)
    assert out.empty


def test_latest_reviews_keeps_most_recent():
    rows = [(f"r{i}", "a", f"Review number {i} is long enough", f"2020-01-{i + 1:02d}") for i in range(5)]
    df = _reviews(rows).assign(date=lambda d: pd.to_datetime(d["date"]))
    out = latest_reviews(df, per_restaurant=2)
    assert set(out["review_id"]) == {"r4", "r3"}


def test_normalize_text_collapses_whitespace():
    assert normalize_text("  great\n\n pasta\t ") == "great pasta"


def test_split_sentences():
    pytest.importorskip("spacy")
    from recommender.preprocessing import split_sentences

    assert split_sentences("Great pasta. Slow service! Would come back?") == [
        "Great pasta.",
        "Slow service!",
        "Would come back?",
    ]
