import os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = "../models/semantic_minilm_model"
DATA_PATH = "../data/business_sentiment_score"
EMB_PATH = "../data/restaurant_embedding.npy"

def load_model_data():
    model = SentenceTransformer(MODEL_PATH)
    df = pd.read_csv(DATA_PATH)

    df["semantic_text"] = (
        df["business_name"].fillna("") + "-" +
        df["categories"].fillna("") + "located at" +
        df["address"].fillna("") 
    )

    if os.path.exists(EMB_PATH):
        restaurant_embeddings = np.load(EMB_PATH)
    else:
        restaurant_embeddings = model.encode(
            df["semantic_text"].tolist(),
            normalize_embeddings=True,
            show_progress_bar=True
        )
        np.save(EMB_PATH, restaurant_embeddings)

    #Sentiment Smoothing
    C = df["sentiment_score"].mean()
    m = 100
    df["smoothed_sentiment"] = (
        (df["sentiment_score"] * df["business_review_count"] + m * C)
        / (df["business_review_count"] + m)
    )

    return model, df, restaurant_embeddings

def recommend(query: str, model, df: pd.DataFrame, restaurant_embeddings: np.ndarray, top_k : int = 5, alpha: float = 0.7) -> pd.DataFrame:
    query_emb = model.encode(query, normalize_embeddings= True)
    sim_scores = model.similarity(query_emb, restaurant_embeddings).squeeze().cpu().numpy()

    #normalize cosine similarity
    sim_norm = (sim_scores - sim_scores.min())/ (sim_scores.max() - sim_scores.min() + 1e-8) # 1e-8 so the denominator doesn't goes to 0

    results = df.copy()
    results["semantic_score"] = sim_norm
    results["final_score"] = alpha * results["semantic_score"] + (1 - alpha) * results["smoothed_sentiment"]

    cols = [
        "business_name", "categories", "address",
        "business_rating", "business_review_count",
        "sentiment_score", "final_score"
    ]

    return results.sort_values("final_score", ascending= False)[cols].head(top_k)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restaurant Content-Based Recommender")
    parser.add_argument("query", type=str, help="Search query (e.g., 'spicy ramen downtown')")
    parser.add_argument("--top_k", type=int, default=5, help="Number of results to return")
    parser.add_argument("--alpha", type=float, default=0.7, help="Weight for semantic score (0 to 1)")

    args = parser.parse_args()

    model, df, restaurant_embeddings = load_model_data()
    recommendations = recommend(
        query=args.query,
        model=model,
        df=df,
        restaurant_embeddings=restaurant_embeddings,
        top_k=args.top_k,
        alpha=args.alpha
    )

    # Print formatted table without index numbers
    print(f"\nTop {args.top_k} recommendations for: '{args.query}' (alpha={args.alpha})\n")
    print(recommendations.to_string(index=False))