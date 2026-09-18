# Restaurant Recommender App — NLP Text Analysis

A restaurant recommendation system that uses Natural Language Processing to analyze customer reviews and match users to restaurants based on the *content* of what people say, not just star ratings.

**Course:** NLP / Generative AI
**Type:** Group Project

## Project Idea

Star ratings hide a lot of nuance — a 4-star review might rave about the food but complain about slow service. This project mines the text of restaurant reviews to build a recommender that understands *why* people liked or disliked a place, and matches that to what a user is actually looking for (e.g. "quiet date-night spot with great pasta" vs. "fast, cheap lunch").

## Core Features

- **Review ingestion** — load a restaurant review dataset (e.g. Yelp Open Dataset, Google local reviews, or scraped data)
- **Text preprocessing** — cleaning, tokenization, stopword removal, lemmatization
- **Aspect extraction** — pull out what reviews actually discuss (food, service, ambiance, price, wait time)
- **Sentiment analysis** — per-aspect sentiment scoring (not just overall polarity)
- **Semantic search / embeddings** — embed reviews and user queries (e.g. OpenAI/Sentence-Transformers embeddings) to match natural-language requests to restaurants
- **Recommendation engine** — rank restaurants by relevance + aspect sentiment fit to the query
- **(Optional) Generative summary** — use an LLM to generate a natural-language summary of why a restaurant was recommended

## Tech Stack (proposed — adjust as your team decides)

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| NLP | spaCy, NLTK, Hugging Face Transformers |
| Embeddings | sentence-transformers |
| Generative layer | OpenAI API / Anthropic API |
| App/UI | Streamlit |
| Data | Pandas, Yelp Open Dataset (or similar) |

## Project Structure

```
restaurant-recommender-nlp/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── src/
│   ├── __init__.py
│   ├── preprocessing.py      # text cleaning, tokenization
│   ├── sentiment.py          # aspect-based sentiment analysis
│   ├── embeddings.py         # embedding generation + similarity search
│   ├── recommender.py        # ranking / recommendation logic
│   └── app.py                # Streamlit app entry point
├── notebooks/
│   └── 01_exploration.ipynb  # EDA on the review dataset
├── data/
│   └── README.md             # data source notes (raw data not committed)
├── tests/
│   └── test_preprocessing.py
└── docs/
    └── proposal.md           # project proposal / write-up
```

## Getting Started

```bash
git clone https://github.com/<your-org-or-username>/restaurant-recommender-nlp.git
cd restaurant-recommender-nlp
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run src/app.py
```

## Team

#**Yannick Kuete**
#**Luc Dinh**
#**Tej Kandimalla**
## License

MIT — see `LICENSE`.
