
import praw
from dotenv import load_dotenv
import os
from scripts.s3_utils import store_posts_in_data_lake

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
reddit_user_agent = os.getenv('REDDIT_CLIENT_AGENT')

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')





def fetch_reddit_posts(subreddit_name,product, total_limit=300):

    """" Ingest posts from subreddit, mentioning the product"""

    print("ab")
    print(reddit_client_id)

    # Initialize PRAW with credentials
    reddit = praw.Reddit(client_id = reddit_client_id,
                         client_secret=reddit_client_secret,
                         user_agent=reddit_user_agent)



    # Fetch submissions from the specified subreddit
    subreddit = reddit.subreddit(subreddit_name)
    submissions = subreddit.search(query= product, time_filter="week", limit=total_limit)

    # Fetch submissions within the specified date range
    fetched_posts = []
    for submission in submissions:
        # Check if the product is mentioned in the title or selftext
        if product.lower() in (submission.title + submission.selftext).lower():
            post_info = {
                'id': submission.id,
                'title': submission.title,
                'created_utc': submission.created_utc,
                'selftext': submission.selftext,
                'score': submission.score,
                'url': submission.url,
                'num_comments': submission.num_comments,
                'subreddit': submission.subreddit.display_name
            }
            fetched_posts.append(post_info)

            # Break the loop if the total limit is reached or if the submission is outside the date range
            if len(fetched_posts) >= total_limit:
                break

    store_posts_in_data_lake(fetched_posts,product, subreddit)





