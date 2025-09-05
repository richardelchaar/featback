import json
import re
from collections.abc import Iterable

import boto3
import botocore
import pandas as pd

from featback.config import settings


def slugify(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", str(s).strip())

session = boto3.session.Session(
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_default_region,
)

s3 = session.client("s3", endpoint_url=settings.s3_endpoint_url or None)
BUCKET = settings.s3_bucket

def safe_key(*parts: Iterable[str]) -> str:
    return "/".join(slugify(p) for p in parts)

def put_json(key: str, obj: dict | list) -> None:
    s3.put_object(Bucket=BUCKET, Key=key, Body=json.dumps(obj).encode("utf-8"))

def put_bytes(key: str, data: bytes) -> None:
    s3.put_object(Bucket=BUCKET, Key=key, Body=data)

def list_keys(prefix: str) -> list[str]:
    keys, token = [], None
    while True:
        kwargs = {"Bucket": BUCKET, "Prefix": prefix}
        if token: 
            kwargs["ContinuationToken"] = token
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp.get("Contents", []): 
            keys.append(obj["Key"])
        token = resp.get("NextContinuationToken")
        if not token: 
            break
    return keys

def get_json(key: str) -> dict:
    obj = s3.get_object(Bucket=BUCKET, Key=key)
    return json.loads(obj["Body"].read().decode("utf-8"))

def load_json_df(prefix: str) -> pd.DataFrame:
    files = [k for k in list_keys(prefix) if k.endswith(".json")]
    rows = []
    for k in files:
        try: 
            rows.append(get_json(k))
        except Exception: 
            continue
    return pd.DataFrame(rows) if rows else pd.DataFrame()

def put_text(key: str, text: str) -> None:
    s3.put_object(Bucket=BUCKET, Key=key, Body=text.encode("utf-8"))

def get_text(key: str) -> str | None:
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=key)
        return obj["Body"].read().decode("utf-8")
    except botocore.exceptions.ClientError:
        return None
