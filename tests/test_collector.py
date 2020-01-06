import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
import math
from datetime import datetime, timedelta
import pytz
import json

def get_source_on_date(date, source="fox-news", intervals=4, verbose=False):

    if verbose:
        print(f"Retrieving from newsapi.org")
        ind = "   "

    
    if verbose: print(f"Splitting into {intervals} intervals")

    # if n_intervals > 1:

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
            if verbose:
                print(f"{3*ind}page: ", page)

            return 111

        total_results = get_results(page=page, source=source)

        if total_results > 20:

            if total_results > 100:
                print("ERROR: Too many results to get all of them, reduce time interval.")
                return False

            else:
                n_pages = math.ceil(total_results / 20.)
                
                for this_page in range(page + 1, n_pages + 1):
                    get_results(page=this_page, source=source)

    return True

# top_headlines_now()
get_source_on_date(datetime(2020, 1, 1), intervals=8, source="fox-news", verbose=True)