from scripts.s3_utils import get_last_processed_timestamp_from_s3, save_last_processed_timestamp_to_s3, load_json_files_from_s3
from scripts.redshift_utils import load_to_s3_and_redshift
from scripts.data_processing import analysis_results
import pandas as pd

def product_feedback_pipeline(subreddit, product):
    """Main pipeline for processing Reddit submissions and saving results."""
    try:
        prefix = f"data/reddit_submissions/{subreddit}/{product}"
        timestamp_file = f"last_timestamp/{subreddit}/{product}/last_processed.txt"

        last_processed_timestamp = get_last_processed_timestamp_from_s3(timestamp_file)
        reddit_submission_table = load_json_files_from_s3(prefix)
        reddit_submission_table = reddit_submission_table[reddit_submission_table['created_utc'] > last_processed_timestamp]
        reddit_submission_table = reddit_submission_table.drop_duplicates()

        if reddit_submission_table.empty:
            return

        reviews_df, questions_df = analysis_results(reddit_submission_table, product)


        reviews_df['created_utc'] = pd.to_datetime(reviews_df['created_utc'], unit='s')
        questions_df['created_utc'] = pd.to_datetime(questions_df['created_utc'], unit='s')

        reviews_df['created_date'] = reviews_df['created_utc'].dt.date
        questions_df['created_date'] = questions_df['created_utc'].dt.date

        reviews_df.drop('created_utc', axis=1, inplace=True)
        questions_df.drop('created_utc', axis=1, inplace=True)

        load_to_s3_and_redshift(reviews_df, "reviews", subreddit, product)
        load_to_s3_and_redshift(questions_df, "questions", subreddit, product)

        max_timestamp = reviews_df['created_utc'].max()
        save_last_processed_timestamp_to_s3(max_timestamp, timestamp_file)
    except Exception as e:
        raise RuntimeError(f"Error in product feedback pipeline: {e}")