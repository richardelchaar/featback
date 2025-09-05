from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from featback.io.s3 import slugify  # reuse helper
from featback.pipeline.product_feedback import run_pipeline
from featback.reddit.ingestion import fetch_reddit_posts

SUBREDDIT = "iphone"
PRODUCT = slugify("Iphone 16")

default_args = {
  "owner": "airflow",
  "depends_on_past": False,
  "email_on_failure": True,
  "email_on_retry": False,
  "retries": 1,
  "retry_delay": timedelta(minutes=5),
}

with DAG(
  dag_id="featback_weekly",
  default_args=default_args,
  start_date=datetime(2024,12,28),
  schedule_interval="@weekly",
  catchup=False, 
  max_active_runs=1,
) as dag:
  
  ingest = PythonOperator(
    task_id="fetch_reddit_posts",
    python_callable=fetch_reddit_posts,
    op_args=[SUBREDDIT, PRODUCT],
  )
  
  process = PythonOperator(
    task_id="run_product_feedback",
    python_callable=run_pipeline,
    op_args=[SUBREDDIT, PRODUCT],
  )
  
  ingest >> process
