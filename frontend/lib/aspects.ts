// Same keys and labels as ASPECT_LABELS in recommender/sentiment.py.
export const ASPECT_LABELS: Record<string, string> = {
  food: "Food",
  service: "Service",
  ambience: "Ambience",
  price: "Price",
  noise: "Quiet (noise)",
  wait_time: "Wait time",
  dietary: "Dietary options",
};

export const aspectLabel = (key: string) => ASPECT_LABELS[key] ?? key;
