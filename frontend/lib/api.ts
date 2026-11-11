// Typed client for the FastAPI backend (api/routes.py).
import mockRecommend from "@/mocks/recommend.json";
import mockRestaurant from "@/mocks/restaurant.json";
import type {
  FeedbackIn,
  RecommendRequest,
  RecommendResponse,
  RestaurantDetail,
} from "@/lib/types";

const API_URL = (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000").replace(/\/$/, "");

// Mock data until the API is running. Set NEXT_PUBLIC_USE_MOCKS=false to call the API.
export const USE_MOCKS = process.env.NEXT_PUBLIC_USE_MOCKS !== "false";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_URL}/api${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", ...init?.headers },
    });
  } catch {
    throw new ApiError("The recommendation service is unreachable.", 0);
  }
  if (!response.ok) {
    const messages: Record<number, string> = {
      404: "We could not find that restaurant.",
      422: "Please check your search: it may be too long or use an unknown filter.",
      429: "Too many searches in a minute. Please wait a moment and try again.",
    };
    throw new ApiError(messages[response.status] ?? "Something went wrong.", response.status);
  }
  return (await response.json()) as T;
}

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export async function recommend(body: RecommendRequest): Promise<RecommendResponse> {
  if (USE_MOCKS) {
    await delay(400);
    return { ...(mockRecommend as RecommendResponse), query: body.query };
  }
  return request<RecommendResponse>("/recommend", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function getRestaurant(businessId: string): Promise<RestaurantDetail> {
  if (USE_MOCKS) {
    await delay(300);
    return mockRestaurant as RestaurantDetail;
  }
  return request<RestaurantDetail>(`/restaurants/${encodeURIComponent(businessId)}`);
}

export async function sendFeedback(feedback: FeedbackIn): Promise<void> {
  if (USE_MOCKS) {
    await delay(200);
    return;
  }
  await request("/feedback", { method: "POST", body: JSON.stringify(feedback) });
}
