import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REDSHIFT_ENDPOINT = os.getenv('ENDPOINT')
REDSHIFT_USERNAME = os.getenv('AWS_USERNAME')
REDSHIFT_PASSWORD = os.getenv('AWS_PASSWORD')
IAM_ROLE = os.getenv('IAM_ROLE')
