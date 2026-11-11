# Mock API responses

Sample responses that match `api/schemas.py`, so the frontend can be built
before the API runs. They were validated against the Pydantic models
(`RecommendResponse` and `RestaurantDetail`). All names and numbers are
made up for the prototype.

- `recommend.json`: `POST /api/recommend` for "quiet date-night spot with great pasta"
- `restaurant.json`: `GET /api/restaurants/mock-lume`

Used when `NEXT_PUBLIC_USE_MOCKS=true` (see `lib/api.ts`).
