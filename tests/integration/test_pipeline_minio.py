import boto3
import pandas as pd
from moto import mock_aws

from featback.io import s3 as s3io
from featback.pipeline.product_feedback import run_pipeline


@mock_aws
def test_pipeline_saves_last_ts(monkeypatch):
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="featback1")
    monkeypatch.setattr(s3io, "s3", s3)
    monkeypatch.setattr(s3io, "BUCKET", "featback1")
    
    key = s3io.safe_key("data","reddit_submissions","iphone","Iphone_16","p1.json")
    s3io.put_json(key, {
        "id":"p1","title":"battery","selftext":"great battery",
        "created_utc":1000.0,"score":1,"url":"u","num_comments":0,"subreddit":"iphone"
    })
    
    from featback.pipeline import data_processing as dp
    def fake_extract(posts_df, product):
        return pd.DataFrame([{
            "id":"p1","text":"t","category":"Battery","feature":"Battery duration",
            "emotion":"Satisfaction","reason":"Functionality","created_utc":1000.0
        }]), pd.DataFrame()
    monkeypatch.setattr(dp, "analysis_results", fake_extract)
    
    run_pipeline("iphone","Iphone_16")
    
    last_key = s3io.safe_key("last_timestamp","iphone","Iphone_16","last_processed.txt")
    v = s3.get_object(Bucket="featback1", Key=last_key)["Body"].read().decode("utf-8")
    assert float(v) == 1000.0
