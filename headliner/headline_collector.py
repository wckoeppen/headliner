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

load_dotenv()

logging.basicConfig(
    filename='/home/will/Projects/headliner/headliner.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )
logger = logging.getLogger(__name__)

# turn off requests logging clutter
# logging.getLogger("urllib3").setLevel(logging.WARNING)


API_KEY = os.getenv("NEWSAPI_KEY")
api = NewsApiClient(api_key=API_KEY)


# def top_headlines_now(country="us"):
#     """Get the top headlines right now.
    
#     Parameters
#     ----------
#     country : str, optional
#         [description], by default 'us'
#     """

#     now = datetime.now(pytz.utc)

#     results = api.get_top_headlines(country="us")

#     date_string = now.strftime("%Y-%m-%dT%H:%M:%S")

#     with open(f"headline-store-json/{date_string}-top-headlines.json", "w") as file:
#         json.dump(results, file)


def get_source_on_date(date, source="", intervals=4):
    """Get the headlines for all articles for a source on a given day.
    
    Parameters
    ----------
    date : datetime
        The date requested
    source : string, optional
        A string designating the source, by default ""
    interval: int, optional
        The interval, in number of hours, by which to break up the
        request. By default 6.
    """

    logger.debug(f"Splitting into {intervals} intervals")

    hour_split = 24 / intervals

    for interval in range(intervals):
        begin_date = date + timedelta(hours=hour_split * interval)
        end_date = date + timedelta(hours=hour_split * (interval + 1), seconds=-1)

        from_datehour_str = begin_date.strftime("%Y-%m-%dT%H:%M:%S")
        to_datehour_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")

        logger.info(f"requesting from {from_datehour_str} to {to_datehour_str}")

        # get the first set of results for the time period and save
        # use the total_results to calculate the number of pages
        # loop through the rest of the pages

        page = 1

        def get_results(page=page, source=source):

            logger.info(f"page: {page}")

            results = api.get_everything(
                from_param=begin_date.strftime("%Y-%m-%dT%H:%M:%S"),
                to=end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                language="en",
                sources=source,  # Max 20 sources
                page=page,
            )

            logger.debug("collected data")

            with open(
                f"/home/will/Projects/headliner/datastore/raw/{source}/{source}-{from_datehour_str}-p{page:03}.json",
                "w"
            ) as file:
                json.dump(results, file)

            return results["totalResults"]

        total_results = get_results(page=page, source=source)

        if total_results > 20:

            if total_results > 100:
                logger.warning(f"{total_results} results in this period!")
                return False

            else:
                n_pages = math.ceil(total_results / 20.0)

                for this_page in range(page + 1, n_pages + 1):
                    get_results(page=this_page, source=source)

    return True


def find_files(base_dir, begin_date, end_date):

    n_days = int((end_date - begin_date).total_seconds()/60/60/24)
    date_list = [begin_date + timedelta(days=x) for x in range(n_days+1)]
    
    search_strs = []
    
    for date in date_list:
        search_strs.append(date.strftime('%Y-%m-%d'))

    filenames=[]

    for search_str in search_strs:
        
        filenames += sorted(glob.glob(os.path.join(base_dir, '*' + search_str + '*.json')))
        
    return filenames


def process_source_on_date(date, source=""):

    source_dir = f"/home/will/Projects/headliner/datastore/raw/{source}/"
    out_dir = f"/home/will/Projects/headliner/datastore/processed/{source}/"

    filenames = find_files(source_dir, date, date)

    def concat_files(file_list):

        results = []

        for filename in filenames:
            with open(filename, "r") as file:
                to_add = json.load(file)
                to_add = pd.io.json.json_normalize(to_add['articles'])
            
            results.append(to_add)

        return pd.concat(results, ignore_index=True)

    concatted = concat_files(filenames)

    concatted.to_csv(os.path.join(out_dir, f"{source}-{date.strftime('%y-%m-%d')}.csv"), index=False)

    return True