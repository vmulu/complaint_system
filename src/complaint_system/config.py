"""
dedicated space to load in the ENV file
"""

import os
from dotenv import load_dotenv

# pulls env file into app context
load_dotenv()

# save env variable to variables in the app
AWS_PROFILE = os.environ["AWS_PROFILE"]
AWS_REGION = os.environ["AWS_REGION"]
