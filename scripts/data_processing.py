import pandas as pd
from scripts.llm_utils import extract_features_with_llm

def analysis_results(fetched_posts, product):

    """ Enrich the reddit posts dataframe by calling the extract_features_with_llm function for each row"""
    results_reviews = []
    results_questions = []

    for _, post in fetched_posts.iterrows():
        post_id = post["id"]
        post_title = post["title"]
        post_text = post["selftext"]

        extracted_features = extract_features_with_llm(post_title, post_text, product)

        for feature in extracted_features:
            if feature["type"] == "review":
                results_reviews.append({
                    "id": post_id,
                    "text": post_text,
                    "category": feature['category'],
                    "feature": feature['feature'],
                    "emotion": feature['emotion'],
                    "reason": feature['reason'],
                    "created_utc": post['created_utc']
                })
            elif feature["type"] == "question":
                results_questions.append({
                    "id": post_id,
                    "text": post_text,
                    "category": feature['category'],
                    "feature": feature['feature'],
                    "reason": feature['reason'],
                    "created_utc": post['created_utc']
                })

    reviews_df = pd.DataFrame(results_reviews)
    questions_df = pd.DataFrame(results_questions)

    return reviews_df, questions_df
