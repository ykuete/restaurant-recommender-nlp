// Mirrors api/schemas.py. Change both together.

export type DietaryOption = "vegetarian" | "vegan" | "gluten-free" | "halal" | "kosher";

export interface RecommendRequest {
  query: string;
  city?: string | null;
  cuisine?: string | null;
  price?: number[]; // Yelp price levels 1-4 ($-$$$$)
  dietary?: DietaryOption[];
  k?: number;
}

export interface AspectScore {
  key: string;
  label: string;
  positive: number; // % of mentions that are positive
  negative: number; // % of mentions that are negative
  mentions: number;
}

export interface Snippet {
  text: string;
  stars: number;
  aspect: string | null;
}

export interface MatchScores {
  semantic: number;
  aspect_fit: number;
  rating: number;
}

export interface RestaurantCard {
  business_id: string;
  name: string;
  city: string;
  state: string;
  categories: string[];
  price: number | null;
  stars: number;
  review_count: number;
  aspects: AspectScore[];
}

export interface RestaurantResult extends RestaurantCard {
  match: number; // 0-100
  scores: MatchScores;
  query_aspects: string[];
  snippet: Snippet | null;
  summary: string;
}

export interface RecommendResponse {
  query: string;
  query_aspects: string[];
  results: RestaurantResult[];
  baseline: RestaurantCard[];
}

export interface AspectSnippet {
  aspect: string;
  label: string;
  text: string;
  sentiment: "positive" | "negative";
  stars: number;
  year: number;
}

export interface RestaurantDetail extends RestaurantCard {
  snippets: AspectSnippet[];
  similar: RestaurantCard[];
}

export interface FeedbackIn {
  business_id: string;
  query: string;
  helpful: boolean;
}
