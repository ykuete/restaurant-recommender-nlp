# TasteLens frontend

Next.js (App Router, TypeScript, Tailwind CSS 4). Three pages, built from the
clickable prototype:

| Route | Page |
| --- | --- |
| `/` | Search: request, city, cuisine, budget, dietary filters |
| `/results?q=...` | Ranked results with AI summaries, aspect bars, baseline comparison |
| `/restaurants/[id]?q=...` | Aspect profile, review sentences, similar restaurants |

## Run locally

```bash
cd frontend
cp .env.example .env.local      # points at the API on http://localhost:8000
npm install
npm run dev                     # http://localhost:3000
```

Start the API first (`uvicorn api.main:app --reload` from the repository root),
or set `NEXT_PUBLIC_USE_MOCKS=true` to use the sample data in `mocks/`.

## Checks

```bash
npm run lint
npm run build
```

## Code map

- `lib/api.ts`: typed client for the FastAPI endpoints
- `lib/types.ts`: mirrors `api/schemas.py`; change both together
- `components/`: `SearchForm`, `ResultsView`, `RestaurantCard`, `AspectBar`,
  `DetailView`, `FeedbackButtons`, loading/empty/error `States`
