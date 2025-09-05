import praw
from featback.config import settings
from featback.io.s3 import put_json, safe_key

def fetch_reddit_posts(subreddit_name: str, product: str, total_limit: int = 300):
    reddit = praw.Reddit(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_client_secret,
        user_agent=settings.reddit_client_agent,
    )
    
    submissions = reddit.subreddit(subreddit_name).search(query=product, time_filter="week", limit=total_limit)
    
    fetched = []
    for s in submissions:
        if product.lower() in (s.title + s.selftext).lower():
            fetched.append({
                "id": s.id,
                "title": s.title,
                "created_utc": float(s.created_utc),
                "selftext": s.selftext,
                "score": int(s.score),
                "url": s.url,
                "num_comments": int(s.num_comments),
                "subreddit": s.subreddit.display_name,
            })
            if len(fetched) >= total_limit: 
                break
    
    for post in fetched:
        key = safe_key("data","reddit_submissions",subreddit_name,product,f"{post['id']}.json")
        put_json(key, post)
