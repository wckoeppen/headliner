import os
from dotenv import load_dotenv
import math
import time
from datetime import datetime, timedelta
import json
import logging
import requests

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# turn off requests logging clutter
logging.getLogger("urllib3").setLevel(logging.WARNING)
NYT_KEY = os.getenv("NYT_KEY")

def get_nyt_on_date(date, source="the-new-york-times", intervals=12):
    """Get the headlines for all articles for the NYT from the
    NYT Developer's API on a given day.
    
    Parameters
    ----------
    date : datetime
        The date requested
    source : string, optional
        A string designating the source, by default ""
    interval: int, optional
        The interval, in number of hours, by which to break up the
        request. By default 12.
    """

    api_result_limit = 10
    api_total_limit = 1000

    logger.info(f"Retrieving {source} from nytapi on {date.strftime('%Y-%m-%d')}")
    logger.debug(f"Splitting into {intervals} intervals")

    hour_split = 24 / intervals

    for interval in range(intervals):
        begin_date = date + timedelta(hours=hour_split * interval)
        end_date = date + timedelta(hours=hour_split * (interval + 1), seconds=-1)

        from_datehour_str = begin_date.strftime("%Y-%m-%dT%H:%M:%S")
        to_datehour_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")

        logger.debug(f"requesting from {from_datehour_str} to {to_datehour_str}")

        page = 0

        def get_results(page=page, source=source):

            logger.debug(f"page: {page}")

            url = (
                "https://api.nytimes.com/svc/search/v2/articlesearch.json?"
                f"api-key={NYT_KEY}"
                f"&begin_date={from_datehour_str}"
                f"&end_date={to_datehour_str}"
                f'&fq=source:("The New York Times")'
                f"&page={page}"
            )

            r = requests.get(url)

            logger.debug("collected data")

            output_file = (
                    f"/home/will/Projects/headliner/datastore/raw/"
                    f"{source}/{source}-{from_datehour_str}-p{page:03}"
                    f".json"
                )

            with open(output_file, "w") as file:
                json.dump(r.json(), file)
                
            # NYT throttles the rate of return, not the actual
            # number of returns
            time.sleep(6)

            return(r.json()["response"]["meta"]["hits"])

    total_results = get_results(page=page, source=source)

    if total_results > api_result_limit:

        if total_results > api_total_limit:
            logger.warning(f"{total_results} results from {source} from {from_datehour_str} to {to_datehour_str}")
            return False

        else:
            n_pages = math.ceil(total_results / api_result_limit)

            for this_page in range(page + 1, n_pages):
                get_results(page=this_page)

    return True