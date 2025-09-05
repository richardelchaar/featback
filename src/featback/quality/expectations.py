import pandas as pd
from pandera import Column, DataFrameSchema

raw_post_schema = DataFrameSchema({
  "id": Column(str),
  "title": Column(str, nullable=True),
  "selftext": Column(str, nullable=True),
  "created_utc": Column(float),
  "score": Column(int, nullable=True),
  "url": Column(str, nullable=True),
  "num_comments": Column(int, nullable=True),
  "subreddit": Column(str),
})

def validate_raw(df: pd.DataFrame) -> pd.DataFrame:
  if df.empty: 
    return df
  return raw_post_schema.validate(df, lazy=True)
