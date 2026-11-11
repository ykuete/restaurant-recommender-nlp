import type { RecommendRequest } from "@/lib/types";

export const priceLabel = (level: number | null) => (level ? "$".repeat(level) : null);

export const formatCount = (n: number) => n.toLocaleString("en-US");

/** Search state <-> URL, so results can be bookmarked and shared. */
export function toSearchParams(req: RecommendRequest): URLSearchParams {
  const params = new URLSearchParams({ q: req.query });
  if (req.city) params.set("city", req.city);
  if (req.cuisine) params.set("cuisine", req.cuisine);
  req.price?.forEach((p) => params.append("price", String(p)));
  req.dietary?.forEach((d) => params.append("diet", d));
  return params;
}

export function fromSearchParams(params: URLSearchParams): RecommendRequest {
  return {
    query: params.get("q") ?? "",
    city: params.get("city"),
    cuisine: params.get("cuisine"),
    price: params.getAll("price").map(Number).filter((n) => n >= 1 && n <= 4),
    dietary: params.getAll("diet") as RecommendRequest["dietary"],
  };
}
