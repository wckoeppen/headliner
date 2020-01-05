import os
from dotenv import load_dotenv
from newsapi import NewsApiClient

load_dotenv()

API_KEY = os.getenv('NEWSAPI_KEY')

api = NewsApiClient(api_key=API_KEY)

srces = api.get_sources()

print(srces)