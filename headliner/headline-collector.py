import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
import math
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


def get_source_on_date(date, source="fox-news", intervals=4, verbose=False):
    """Get the headlines for all articles for a source on a given day.
    
    Parameters
    ----------
    date : datetime
        The date requested
    source : string, optional
        A string designating the source, by default "fox-news"
    interval: int, optional
        The interval, in number of hours, by which to break up the
        request. By default 6.
    verbose : bool, optional
        Print out waypoints, by default False
    """

    if verbose:
        print(f"Retrieving from newsapi.org")
        ind = "   "

    
    if verbose: print(f"Splitting into {intervals} intervals")

    hour_split = 24/intervals

    for interval in range(intervals):
        begin_date = date + timedelta(hours=hour_split*interval)
        end_date = date + timedelta(hours=hour_split*(interval+1), seconds=-1)    

        from_datehour_str = begin_date.strftime("%Y-%m-%dT%H:%M:%S")
        to_datehour_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")


        if verbose:
            print(f"{ind}requesting from {from_datehour_str} to {to_datehour_str}")

    # get the first set of results for the time period and save
    # use the total_results to calculate the number of pages
    # loop through the rest of the pages

        page = 1

        def get_results(page=page, source=source):

            if verbose: print(f"{3*ind}page: ", page)

            results = api.get_everything(
                from_param=begin_date.strftime("%Y-%m-%dT%H:%M:%S"),
                to=end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                language="en",
                sources=source,  # Max 20 sources
                page=page,
            )

            with open(
                f"headline-store-json/{source}-{from_datehour_str}-p{page:03}.json", "w"
            ) as file:
                json.dump(results, file)

            return results["totalResults"]

        total_results = get_results(page=page, source=source)

        if total_results > 20:

            if total_results > 100:
                print("ERROR: Too many results in this period, reduce time interval.")
                return False

            else:
                n_pages = math.ceil(total_results / 20.)
                
                for this_page in range(page + 1, n_pages + 1):
                    get_results(page=this_page, source=source)

    return True

# top_headlines_now()
get_source_on_date(datetime(2020, 1, 1), intervals=4, source="fox-news", verbose=True)
