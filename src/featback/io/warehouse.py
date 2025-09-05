from datetime import datetime
import io
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import redshift_connector
from featback.config import settings
from featback.io.s3 import put_bytes, safe_key, BUCKET

def write_parquet_to_s3(df: pd.DataFrame, key: str) -> None:
    if df.empty: 
        return
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(df), buf)
    buf.seek(0)
    put_bytes(key, buf.getvalue())

def redshift_copy_parquet(table: str, s3_key: str):
    conn = redshift_connector.connect(
        host=settings.redshift_endpoint, 
        database="dev", 
        port=5439,
        user=settings.aws_username, 
        password=settings.aws_password,
    )
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id VARCHAR, text VARCHAR, category VARCHAR, feature VARCHAR,
            emotion VARCHAR, reason VARCHAR, created_utc TIMESTAMP
        );
    """)
    conn.commit()
    cur.execute(f"""
        COPY {table}
        FROM 's3://{BUCKET}/{s3_key}'
        IAM_ROLE '{settings.iam_role}'
        FORMAT AS PARQUET;
    """)
    conn.commit()
    cur.close()
    conn.close()

def load_to_warehouse(df: pd.DataFrame, table: str, subreddit: str, product: str):
    if df.empty: 
        return
    ds = datetime.utcnow().strftime("%Y-%m-%d")
    key = safe_key("data", table, subreddit, product, f"{ds}.parquet")
    write_parquet_to_s3(df, key)
    if settings.db_kind == "redshift":
        redshift_copy_parquet(table, key)
