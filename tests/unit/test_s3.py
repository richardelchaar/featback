import pandas as pd
from moto import mock_aws
import boto3
from featback.io import s3 as s3io

@mock_aws
def test_put_and_list_json(monkeypatch):
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="featback1")
    monkeypatch.setattr(s3io, "s3", s3)
    monkeypatch.setattr(s3io, "BUCKET", "featback1")
    
    key = s3io.safe_key("data","reddit_submissions","iphone","Iphone_16","abc.json")
    s3io.put_json(key, {"x":1})
    assert key in s3io.list_keys("data/reddit_submissions/iphone/Iphone_16")
    
    df = s3io.load_json_df("data/reddit_submissions/iphone/Iphone_16")
    assert isinstance(df, pd.DataFrame) and len(df)==1 and df.iloc[0]["x"]==1
