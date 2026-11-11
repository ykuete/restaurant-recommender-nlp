# TasteLens — Restaurant Recommender (NLP Text Analysis)

A restaurant recommender that reads what reviewers actually say. Star ratings hide nuance: a 4-star review can praise the food and complain about slow service. TasteLens scores each restaurant on food, service, ambience, price, noise and wait time from review text, then matches those scores to a plain-language request such as *"quiet date-night spot with great pasta"*.

**Course:** NLP / Generative AI · **Type:** group project

## How it works

1. **Review ingestion**: Yelp Open Dataset restaurants and reviews → parquet.
2. **Preprocessing**: cleaning (duplicates, very short and pre-2015 reviews, restaurants with fewer than 15 reviews), sentence splitting.
3. **Aspect extraction + sentiment**: each sentence is tagged with aspects and scored positive or negative.
4. **Semantic search**: a sentence-transformer fine-tuned on restaurant reviews embeds reviews and queries.
5. **Recommendation**: restaurants ranked by semantic match, aspect fit and weighted star rating.
6. **Generative summary**: an LLM explains each pick in two sentences.

## Project layout

```text
recommender/   NLP package: pipeline, preprocessing, sentiment, embeddings, ranking
scripts/       offline jobs that build the artifacts, run in order 01 → 05
api/           FastAPI backend
frontend/      Next.js website
notebooks/     experiments: EDA, baseline, sentiment, fine-tuning
artifacts/     git-ignored build outputs (parquet, profiles, index, model)
data/          raw Yelp JSON goes here (git-ignored, see data/README.md)
tests/         pytest suite
docs/          proposal, requirements, evaluation
```

## Setup

Requires Python 3.11.

```bash
git clone https://github.com/<your-org-or-username>/restaurant-recommender-nlp.git
cd restaurant-recommender-nlp
python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env               # then fill in the values you need
```

Three requirement files:

| File | For | Contains |
| --- | --- | --- |
| `requirements.txt` | the API (and its Docker image) | FastAPI, onnxruntime, FAISS, pandas, LLM clients |
| `requirements-ml.txt` | the offline pipeline (`scripts/`, notebooks) | everything above + PyTorch, transformers, sentence-transformers, optimum, spaCy |
| `requirements-dev.txt` | tests and linting | pytest, ruff, jupyter, onnx, spaCy |

Check the install: `python -c "import recommender"` should print nothing and exit without an error.

## Data

The Yelp licence forbids redistributing the dataset, so no data is committed. Download the Yelp Open Dataset and follow [data/README.md](data/README.md). The data pipeline lives in `recommender/pipeline.py`.

## Team

- Yannick Kuete
- Luc Dinh
- Tej Kandimalla

## License

MIT — see `LICENSE`.
