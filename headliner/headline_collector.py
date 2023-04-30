import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
import math
from datetime import datetime, timedelta
import json
import logging

load_dotenv()
logger = logging.getLogger(__name__)

# turn off requests logging clutter
logging.getLogger("urllib3").setLevel(logging.WARNING)

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
api = NewsApiClient(api_key=NEWSAPI_KEY)

def get_newsapi_on_date(date, source="", intervals=4):
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

    logger.info(f"Retrieving {source} from newsapi.org on {date.strftime('%Y-%m-%d')}")
    logger.debug(f"Splitting into {intervals} intervals")

    hour_split = 24 / intervals

    for interval in range(intervals):
        begin_date = date + timedelta(hours=hour_split * interval)
        end_date = date + timedelta(hours=hour_split * (interval + 1), seconds=-1)

        from_datehour_str = begin_date.strftime("%Y-%m-%dT%H:%M:%S")
        to_datehour_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")

        logger.debug(f"requesting from {from_datehour_str} to {to_datehour_str}")

        # get the first set of results for the time period and save
        # use the total_results to calculate the number of pages
        # loop through the rest of the pages

        page = 1

        def get_results(page=page, source=source):

            logger.debug(f"page: {page}")

            results = api.get_everything(
                from_param=begin_date.strftime("%Y-%m-%dT%H:%M:%S"),
                to=end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                language="en",
                sources=source,  # Max 20 sources
                page=page,
            )

            logger.debug("collected data")

            with open(
                f"/Users/wckoeppen/work/projects/headliner/datastore/raw/{source}/{source}-{from_datehour_str}-p{page:03}.json",
                "w"
            ) as file:
                json.dump(results, file)

            return results["totalResults"]

        total_results = get_results(page=page, source=source)

        if total_results > 20:

            if total_results > 100:
                logger.warning(f"{total_results} results from {source} from {from_datehour_str} to {to_datehour_str}")
                return False

            else:
                n_pages = math.ceil(total_results / 20.0)

                for this_page in range(page + 1, n_pages + 1):
                    get_results(page=this_page, source=source)

    return True