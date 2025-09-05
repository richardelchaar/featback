import pandas as pd
import pytest
from pandera.errors import SchemaErrors

from featback.quality.expectations import validate_raw


def test_validate_raw_ok():
    df = pd.DataFrame([{
        "id":"1","title":"t","selftext":"x","created_utc":1.0,
        "score":1,"url":"u","num_comments":0,"subreddit":"iphone"
    }])
    assert len(validate_raw(df))==1

def test_validate_raw_bad():
    df = pd.DataFrame([{"id":"1","created_utc":"bad"}])
    with pytest.raises(SchemaErrors): 
        validate_raw(df)
