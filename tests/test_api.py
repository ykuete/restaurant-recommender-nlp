import pytest
from fastapi.testclient import TestClient

from api.limits import limiter
from api.main import create_app


@pytest.fixture
def client(engine, tmp_path, monkeypatch):
    limiter.reset()
    monkeypatch.setattr("recommender.config.LLM_PROVIDER", "none")
    app = create_app(lambda: engine, database_url=f"sqlite:///{tmp_path / 'feedback.db'}")
    with TestClient(app) as c:
        yield c


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok", "restaurants": 5}


def test_recommend_returns_ranked_results_with_summaries(client):
    resp = client.post("/api/recommend", json={"query": "quiet romantic pasta", "k": 3})
    assert resp.status_code == 200
    body = resp.json()
    assert body["query_aspects"] == ["food", "ambience", "noise"]
    names = [r["name"] for r in body["results"]]
    assert names[0] == "Trattoria Lume"
    assert len(names) == 3
    assert all(r["summary"] for r in body["results"])
    assert all(0 <= r["match"] <= 100 for r in body["results"])
    assert body["baseline"], "baseline list is returned for comparison"


def test_recommend_applies_filters(client):
    body = client.post(
        "/api/recommend", json={"query": "lunch", "price": [1], "dietary": ["vegan"]}
    ).json()
    assert [r["business_id"] for r in body["results"]] == ["taco"]


def test_recommend_with_no_match_returns_empty_list(client):
    body = client.post("/api/recommend", json={"query": "pasta", "city": "Nowhere"}).json()
    assert body["results"] == []


def test_restaurant_detail(client):
    body = client.get("/api/restaurants/lume").json()
    assert body["name"] == "Trattoria Lume"
    assert {s["sentiment"] for s in body["snippets"]} == {"positive", "negative"}
    assert len(body["similar"]) == 3


def test_unknown_restaurant_is_404(client):
    assert client.get("/api/restaurants/nope").status_code == 404


def test_feedback_is_saved(client):
    resp = client.post(
        "/api/feedback", json={"business_id": "lume", "query": "pasta", "helpful": True}
    )
    assert resp.status_code == 201


def test_llm_failure_falls_back_to_template(client, monkeypatch):
    monkeypatch.setattr("recommender.config.LLM_PROVIDER", "anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

    async def broken(provider, prompt):
        raise RuntimeError("LLM down")

    monkeypatch.setattr("recommender.summary._call_llm", broken)
    body = client.post("/api/recommend", json={"query": "quiet pasta", "k": 2}).json()
    assert all(r["summary"].startswith("Reviewers rate") for r in body["results"])


@pytest.mark.parametrize(
    "payload",
    [
        {"query": "x" * 301},
        {"query": "pasta", "k": 21},
        {"query": "pasta", "price": [5]},
        {"query": "pasta", "dietary": ["carnivore"]},
    ],
)
def test_rejects_out_of_range_input(client, payload):
    assert client.post("/api/recommend", json=payload).status_code == 422


def test_recommend_is_rate_limited(client):
    codes = [
        client.post("/api/recommend", json={"query": "pasta", "k": 1}).status_code
        for _ in range(31)
    ]
    assert codes[:30] == [200] * 30
    assert codes[30] == 429
