"""
dedicated space to load in the ENV file
"""

import os
from dotenv import load_dotenv

load_dotenv()

AWS_PROFILE = os.environ["AWS_PROFILE"]
AWS_REGION = os.environ["AWS_REGION"]
BUCKET_NAME = os.environ["AWS_BUCKET_NAME"]