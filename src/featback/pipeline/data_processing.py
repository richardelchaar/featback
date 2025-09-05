import pandas as pd

from featback.llm.openai_extractor import extract_features


def analysis_results(posts_df: pd.DataFrame, product: str):
  reviews, questions = [], []
  for _, post in posts_df.iterrows():
    items = extract_features(post.get("title") or "", post.get("selftext") or "", product)
    if not items: 
      continue
    for it in items:
      base = {
        "id": post["id"], 
        "text": post.get("selftext",""),
        "category": it.get("category"), 
        "feature": it.get("feature"),
        "created_utc": post["created_utc"],
      }
      if it["type"] == "review":
        reviews.append({**base, "emotion": it.get("emotion"), "reason": it.get("reason")})
      else:
        questions.append({**base, "reason": it.get("reason")})
  return pd.DataFrame(reviews), pd.DataFrame(questions)
