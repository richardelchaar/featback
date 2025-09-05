import pandas as pd

from featback.io.s3 import get_text, load_json_df, put_text, safe_key
from featback.io.warehouse import load_to_warehouse
from featback.pipeline.data_processing import analysis_results
from featback.quality.expectations import validate_raw


def _last_ts_key(subreddit: str, product: str) -> str:
    return safe_key("last_timestamp", subreddit, product, "last_processed.txt")

def _get_last_ts(subreddit: str, product: str) -> float:
    v = get_text(_last_ts_key(subreddit, product))
    try: 
        return float(v) if v is not None else 0.0
    except (ValueError, TypeError): 
        return 0.0

def _set_last_ts(subreddit: str, product: str, ts: float) -> None:
    put_text(_last_ts_key(subreddit, product), str(float(ts)))

def run_pipeline(subreddit: str, product: str):
    prefix = safe_key("data","reddit_submissions",subreddit,product)
    raw = load_json_df(prefix)
    if raw.empty: 
        return
    
    raw["created_utc"] = raw["created_utc"].astype(float)
    raw = validate_raw(raw).drop_duplicates(subset=["id"])
    
    last_ts = _get_last_ts(subreddit, product)
    filtered = raw[raw["created_utc"] > last_ts]
    if filtered.empty: 
        return
    
    max_ts = float(filtered["created_utc"].max())
    reviews_df, questions_df = analysis_results(filtered, product)
    
    for df in (reviews_df, questions_df):
        if not df.empty:
            df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s")
    
    load_to_warehouse(reviews_df, "reviews", subreddit, product)
    load_to_warehouse(questions_df, "questions", subreddit, product)
    
    _set_last_ts(subreddit, product, max_ts)
