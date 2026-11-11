import pandas as pd
import pytest

from recommender.sentiment import build_profiles, score_sentences, tag_aspects


class KeywordScorer:
    """Fake scorer: 'great' is positive, 'rude'/'slow' negative, else neutral."""

    def score_many(self, pairs):
        out = []
        for sentence, _aspect in pairs:
            s = sentence.lower()
            out.append(0.9 if "great" in s else -0.9 if ("rude" in s or "slow" in s) else 0.0)
        return out


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        ("quiet date-night spot with great pasta", {"food", "ambience", "noise"}),
        ("Our waiter was rude", {"service"}),
        ("Plenty of vegan options", {"dietary"}),
        ("We parked nearby", set()),
    ],
)
def test_tag_aspects(sentence, expected):
    assert set(tag_aspects(sentence)) == expected


def test_score_sentences_scores_each_aspect():
    rows = score_sentences(["Great pasta.", "The waiter was rude."], KeywordScorer())
    assert {(r["aspect"], r["score"]) for r in rows} == {("food", 0.9), ("service", -0.9)}


def test_build_profiles_aggregates_per_aspect():
    pytest.importorskip("spacy")
    reviews = pd.DataFrame(
        {
            "business_id": ["a", "a", "a"],
            "stars": [5, 4, 2],
            "date": pd.to_datetime(["2021-01-01", "2021-02-01", "2021-03-01"]),
            "text": [
                "The pasta was great and fresh tonight. Our server was friendly.",
                "Great food, truly great dishes all around.",
                "The waiter was rude to the whole table. Slow service all evening.",
            ],
        }
    )
    profiles, snippets = build_profiles(reviews, KeywordScorer(), per_restaurant=10)
    food = profiles.set_index("aspect").loc["food"]
    assert food["mentions"] == 2 and food["positive_share"] == 1.0
    service = profiles.set_index("aspect").loc["service"]
    assert service["negative_share"] > 0.5
    assert {"business_id", "aspect", "sentence", "score"} <= set(snippets.columns)
