import json

import pandas as pd
import pytest

from recommender.ranking import Filters, parse_query, popularity_baseline, price_level, weighted_rating


def _restaurants():
    return pd.DataFrame(
        {
            "business_id": ["a", "b", "c"],
            "stars": [5.0, 4.0, 3.0],
            "review_count": [10, 100, 1000],
        }
    )


def test_weighted_rating_matches_notebook_formula():
    df = _restaurants()
    c = df["stars"].mean()  # 4.0
    m = df["review_count"].quantile(0.9)
    expected = [(v / (v + m)) * r + (m / (v + m)) * c for r, v in zip(df["stars"], df["review_count"])]
    assert weighted_rating(df).tolist() == pytest.approx(expected)


def test_few_reviews_pull_rating_toward_the_mean():
    wr = weighted_rating(_restaurants())
    # 5 stars from 10 reviews ends close to the 4.0 mean, not at 5.
    assert 4.0 < wr.iloc[0] < 4.2


def test_popularity_baseline_keeps_only_well_reviewed_restaurants():
    top = popularity_baseline(_restaurants(), k=10)
    assert list(top["business_id"]) == ["c"]  # only c reaches the 90th-percentile count


@pytest.mark.parametrize(
    ("attributes", "expected"),
    [
        (json.dumps({"RestaurantsPriceRange2": "2"}), 2),
        (json.dumps({"RestaurantsPriceRange2": "u'3'"}), 3),
        (json.dumps({"RestaurantsPriceRange2": "None"}), None),
        (None, None),
    ],
)
def test_price_level(attributes, expected):
    assert price_level(attributes) == expected


def test_parse_query_finds_requested_aspects():
    assert parse_query("cheap, quiet place with vegan options") == ["price", "noise", "dietary"]


def test_hybrid_prefers_better_aspect_fit(engine):
    # Lume and Forno both match "pasta"; the request asks for quiet, and
    # Forno's noise profile is mostly negative.
    names = [r["business_id"] for r in engine.rank("quiet pasta", k=3)]
    assert names.index("lume") < names.index("forno")


def test_equal_semantic_score_ranks_by_aspect_fit(engine):
    engine.weights = (0.0, 1.0, 0.0)  # aspect fit only
    ranked = [r["business_id"] for r in engine.rank("quiet", k=5)]
    assert ranked[0] == "lume"  # 84% positive on noise, the best in the fixture


def test_filters(engine):
    assert {r["business_id"] for r in engine.rank("food", Filters(city="Tampa"))} == {"brunch"}
    assert {r["business_id"] for r in engine.rank("food", Filters(price=[3]))} == {"lume"}
    assert {r["business_id"] for r in engine.rank("food", Filters(cuisine="pizza"))} == {"forno"}
    assert {r["business_id"] for r in engine.rank("food", Filters(dietary=["vegan"]))} == {"taco"}


def test_results_are_well_formed(engine):
    result = engine.rank("romantic pasta", k=1)[0]
    assert 0 <= result["match"] <= 100
    assert set(result["scores"]) == {"semantic", "aspect_fit", "rating"}
    assert result["aspects"][0]["mentions"] >= result["aspects"][-1]["mentions"]
