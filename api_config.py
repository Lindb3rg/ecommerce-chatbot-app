import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('ANTHROPIC_API_KEY').strip()
API_MODEL = os.getenv('ANTHROPIC_HAIKU').strip()

if not API_KEY.startswith('sk-ant-'):
    raise ValueError("API key appears to be in incorrect format. Should start with 'sk-ant-'")
