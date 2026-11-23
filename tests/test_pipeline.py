import pandas as pd

from recommender.pipeline import filter_restaurants, normalize_city


def _business(rows):
    base = {
        "name": "x",
        "state": "XX",
        "stars": 4.0,
        "review_count": 20,
        "is_open": 1,
        "attributes": None,
    }
    return pd.DataFrame([{**base, **r} for r in rows])


BUSINESS = _business(
    [
        {"business_id": "a", "city": "Philadelphia", "categories": "Italian, Restaurants"},
        {"business_id": "b", "city": "Tampa", "categories": "Restaurants, Mexican"},
        {"business_id": "c", "city": "Reno", "categories": "Restaurants"},
        {"business_id": "d", "city": "St. Louis", "categories": "Restaurants, BBQ"},
        {"business_id": "e", "city": "Tampa", "categories": "Hair Salons"},
    ]
)


def test_no_city_keeps_every_restaurant():
    out = filter_restaurants(BUSINESS)
    assert set(out["business_id"]) == {"a", "b", "c", "d"}


def test_one_city_still_works():
    out = filter_restaurants(BUSINESS, "philadelphia")
    assert set(out["business_id"]) == {"a"}


def test_several_cities():
    out = filter_restaurants(BUSINESS, ["Philadelphia", "Tampa"])
    assert set(out["business_id"]) == {"a", "b"}


def test_city_aliases_are_merged():
    out = filter_restaurants(BUSINESS, ["Saint Louis"])
    assert list(out["business_id"]) == ["d"]
    assert list(out["city"]) == ["Saint Louis"]


def test_normalize_city_trims_spaces():
    assert normalize_city("  New   Orleans ") == "New Orleans"
