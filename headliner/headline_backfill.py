#!/home/will/anaconda3/envs/headliner/bin/python

from datetime import datetime, timedelta
import logging
from headline_collector import get_newsapi_on_date
from headline_processor import process_source_on_date
import glob
import os

logging.basicConfig(
    filename='/home/will/Projects/headliner/headliner.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
    )
logger = logging.getLogger(__name__)

sources = ["abc-news"]
store_dir = "/home/will/Projects/headliner/datastore/raw/"

# ~30 requests per day fro
# 4 days of 2 sources = ~100 requests

# 250 requests per 12 hour means gather real-time + 7 days of backfill every 12 hours should be "safe"
# would be great to automate the backfill to run every 12 hours
# and maybe find the max number of requests per day

for source in sources:

    logger.info(f"Retrieving {source} from newsapi.org")

    logger.debug("Checking backdates")

    filenames = sorted(glob.glob(os.path.join(store_dir, source, "*.json")))

    first_file = filenames[0]
    first_date = datetime.strptime(
        first_file.split(source + "-")[1].split("T")[0], "%Y-%m-%d"
    )

    logger.debug(f"first date found: {first_date}")

    n_days = 6

    back_dates = [first_date - timedelta(days=x) for x in range(1, n_days+1)]

    for back_date in back_dates:
        get_newsapi_on_date(back_date, intervals=8, source=source)
        process_source_on_date(back_date, source=source)