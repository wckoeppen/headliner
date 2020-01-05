import os
from dotenv import load_dotenv
from newsapi import NewsApiClient

from datetime import datetime, timedelta
import pytz
import json

load_dotenv()

API_KEY = os.getenv("NEWSAPI_KEY")
api = NewsApiClient(api_key=API_KEY)


def top_headlines_now(country="us"):
    """Get the top headlines right now.
    
    Parameters
    ----------
    country : str, optional
        [description], by default 'us'
    """

    now = datetime.now(pytz.utc)

    results = api.get_top_headlines(country="us")

    date_string = now.strftime("%Y-%m-%dT%H:%M:%S")

    with open(f"headline-store-json/{date_string}-top-headlines.json", "w") as file:
        json.dump(results, file)


def get_sources_on_date(begin_date, verbose=False):

    source = "fox-news"

    end_date = begin_date + timedelta(hours=6)

    if verbose == True: print("Retrieving from newsapi.org")

    def get_results(page = page):
        results = api.get_everything(
            from_param=begin_date.strftime("%Y-%m-%dT%H:%M:%S"),
            to=end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            language="en",
            sources=source,  # Max 20 sources
            page=page,
        )

        with open(f"headline-store-json/{date_string}-{source}-{page:03}.json", "w") as file:
            json.dump(results, file)



    get_results(page=1)

    if results.total_results > 20:
        page += 1




    date_string = begin_date.strftime("%Y-%m-%d-%H")




#top_headlines_now()
get_sources_on_date(datetime(2020, 1, 1, 0, 0, 0), page=1, verbose=True)
