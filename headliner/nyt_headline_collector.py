import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
import math
from datetime import datetime, timedelta
import pytz
import json
import logging
import pandas as pd
import glob
from yanytapi import SearchAPI

load_dotenv()

logging.basicConfig(
    filename='/home/will/Projects/headliner/headliner.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )
logger = logging.getLogger(__name__)

# turn off requests logging clutter
logging.getLogger("urllib3").setLevel(logging.WARNING)


NYT_KEY = os.getenv("NYT_KEY")
nytapi = SearchAPI(NYT_KEY)

# articles = nytapi.search(
#     "Trump",
#     fq={
#         "headline": "Trump",
#         "source": ["The New York Times"]
#         },
#     begin_date="20200120", # this can also be an int
#     end_date="20200120", 
#     facet_field=["source", "day_of_week"], 
#     facet_filter=True)

# articles = nytapi.search(
#     "",
#     fq={
#         "source": ["The New York Times"]
#         },
#     begin_date="20200120", # this can also be an int
#     end_date="20200120", 
#     facet_field=["source", "day_of_week"], 
#     facet_filter=True)

# seems like the manual approach would be easier

begin_date="20200110"
end_date="20200110"


url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?&api-key={NYT_KEY}&begin_date={begin_date}&end_date={end_date}"
print(url)

print("https://api.nytimes.com/svc/search/v2/articlesearch.json?q=new+york+times&page=2&sort=oldest)")

# first_article=list(articles)[1]
# print(first_article.headline['print_headline'])
# print(first_article.web_url)
# print(first_article.pub_date)
# print(articles.)

#def get_nytapi_on_date(date, intervals=4):
    
