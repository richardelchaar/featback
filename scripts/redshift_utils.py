
import redshift_connector          # For connecting to Redshift
import pyarrow as pa               # For working with Parquet files
import pyarrow.parquet as pq       # For writing DataFrame to Parquet
from datetime import datetime      # For handling timestamps
import io                          # For in-memory file handling
from scripts.s3_utils import s3_client
from scripts.configuration import REDSHIFT_ENDPOINT, REDSHIFT_USERNAME, REDSHIFT_PASSWORD, IAM_ROLE



def load_to_s3_and_redshift(df, table_name, subreddit, product):
    """Write a DataFrame to S3 in Parquet format and load it into Redshift."""
    if df.empty:
        return

    try:
        parquet_buffer = io.BytesIO()
        table = pa.Table.from_pandas(df)
        pq.write_table(table, parquet_buffer)
        parquet_buffer.seek(0)

        today_date = datetime.now().strftime("%Y-%m-%d")
        s3_client.put_object(
            Body=parquet_buffer.getvalue(),
            Bucket="featback1",
            Key=f"data/{table_name}/{subreddit}/{product}/{today_date}.parquet"
        )
    except Exception as e:
        raise RuntimeError(f"Error writing data to S3: {e}")

    try:
        conn = redshift_connector.connect(
            host=REDSHIFT_ENDPOINT,
            database='dev',
            port=5439,
            user=REDSHIFT_USERNAME,
            password=REDSHIFT_PASSWORD
        )
        cursor = conn.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id VARCHAR,
                text VARCHAR,
                category VARCHAR,
                feature VARCHAR,
                emotion VARCHAR,
                reason VARCHAR,
                created_utc TIMESTAMP
            )
        """)
        conn.commit()

        copy_command = f"""
        COPY {table_name}
        FROM 's3://featback1/data/{table_name}/{subreddit}/{product}/{today_date}.parquet'
        IAM_ROLE '{IAM_ROLE}'
        FORMAT AS PARQUET;
        """
        cursor.execute(copy_command)
        conn.commit()
    except Exception as e:
        raise RuntimeError(f"Error loading data into Redshift: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
