from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    s3_endpoint_url: str | None = None
    s3_bucket: str = "featback1"
    aws_default_region: str | None = "us-east-1"
    db_kind: str = "redshift"
    redshift_endpoint: str | None = None
    aws_username: str | None = None
    aws_password: str | None = None
    iam_role: str | None = None
    postgres_host: str | None = None
    postgres_db: str | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None
    reddit_client_id: str | None = None
    reddit_client_secret: str | None = None
    reddit_client_agent: str = "featback/1.0"
    openai_api_key: str | None = None
    mlflow_tracking_uri: str | None = None
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()
