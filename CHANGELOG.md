# Changelog

## 1.0.0 — first public release

- Natural-language restaurant search over Yelp Open Dataset reviews.
- Aspect-based sentiment for food, service, ambience, price, noise, wait
  time and dietary options.
- Fine-tuned sentence-transformer (all-MiniLM-L6-v2) with a FAISS index;
  ONNX query encoding in the API.
- Hybrid ranking: semantic match + aspect fit + weighted rating, compared
  against a popularity baseline.
- LLM summaries with an 8-second budget and template fallback.
- FastAPI backend (recommend, restaurant detail, feedback, health) with
  input limits and rate limiting.
- Next.js frontend: search, results and detail pages; feedback buttons.
- CI on every pull request; Docker images; deployment on Vercel + Render.
