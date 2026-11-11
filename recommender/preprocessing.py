"""Text preprocessing: the cleaning rules from notebooks/02_EDA.ipynb plus
sentence splitting, tokenizing and lemmatizing with spaCy."""

from __future__ import annotations

import re
from functools import lru_cache

import pandas as pd

from recommender import config

_WHITESPACE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Collapse runs of whitespace and trim. Case and punctuation are kept,
    because the sentiment model reads them."""
    return _WHITESPACE.sub(" ", text or "").strip()


def clean_reviews(
    reviews: pd.DataFrame,
    min_chars: int = config.MIN_CHARS,
    min_date: str = config.MIN_DATE,
    min_reviews: int = config.MIN_REVIEWS,
) -> pd.DataFrame:
    """Apply the EDA cleaning rules, in the notebook's order:

    1. drop duplicate review texts
    2. drop reviews shorter than ``min_chars`` characters
    3. drop reviews older than ``min_date``
    4. drop restaurants left with fewer than ``min_reviews`` reviews
    """
    df = reviews.drop_duplicates(subset=["text"])
    df = df[df["text"].str.strip().str.len() >= min_chars]
    df = df.assign(date=pd.to_datetime(df["date"]))
    df = df[df["date"] >= pd.Timestamp(min_date)]
    counts = df["business_id"].value_counts()
    keep = counts[counts >= min_reviews].index
    df = df[df["business_id"].isin(keep)]
    return df.reset_index(drop=True)


def latest_reviews(reviews: pd.DataFrame, per_restaurant: int) -> pd.DataFrame:
    """Keep the ``per_restaurant`` most recent reviews of each restaurant."""
    ordered = reviews.sort_values("date", ascending=False)
    return ordered.groupby("business_id", group_keys=False).head(per_restaurant)


@lru_cache(maxsize=1)
def _sentencizer():
    import spacy

    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")
    return nlp


@lru_cache(maxsize=1)
def _lemmatizer():
    import spacy

    try:
        return spacy.load("en_core_web_sm", disable=["parser", "ner"])
    except OSError as err:  # model not downloaded
        raise RuntimeError(
            "spaCy model missing: run `python -m spacy download en_core_web_sm`"
        ) from err


def split_sentences(text: str) -> list[str]:
    """Split a review into sentences (rule-based; no model download needed)."""
    doc = _sentencizer()(normalize_text(text))
    return [s.text.strip() for s in doc.sents if s.text.strip()]


def lemmas(text: str, remove_stopwords: bool = True) -> list[str]:
    """Lower-cased lemmas of the alphabetic tokens, without stopwords."""
    doc = _lemmatizer()(normalize_text(text))
    return [t.lemma_.lower() for t in doc if t.is_alpha and not (remove_stopwords and t.is_stop)]
