from airflow import DAG
from airflow.utils.state import State
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory of your project to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_dir)

from scripts import product_sentiment_analysis_main
from scripts import reddit_ingestion


subreddit = "iphone"
product = "Iphone 16"
data_lake_path = f"s3a://featback1/data/reddit_submissions/{subreddit}/{product}"





default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['richard.elchaar@outlook.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='review_topic_modeling',
    default_args=default_args,
    start_date=datetime(2024, 12, 28),
    schedule_interval='@weekly',
) as dag:


    fetch_reddit_posts_task = PythonOperator(
        task_id='fetch_reddit_posts_task',
        python_callable=reddit_ingestion.fetch_reddit_posts,
        op_args=[subreddit,product],
    )

    llm_analysis_task = PythonOperator(
        task_id='llm_analysis_task',
        python_callable=product_sentiment_analysis_main.product_feedback_pipeline,
        op_args=[subreddit,product],
    )



    # Branch to choose historical or daily tweets based on previous success
    fetch_reddit_posts_task >> llm_analysis_task




