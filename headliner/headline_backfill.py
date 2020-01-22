#!/home/will/anaconda3/envs/headliner/bin/python

from datetime import datetime, timedelta
import logging
from headline_collector import get_newsapi_on_date
from headline_processor import process_source_on_date
import glob
import os
import pandas as pd

logging.basicConfig(
    filename='/home/will/Projects/headliner/headliner.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
    )
logger = logging.getLogger(__name__)

sources = ["associated-press"]
store_dir = "/home/will/Projects/headliner/datastore/raw/"

for source in sources:

    back_dates = pd.date_range(start="2020-01-14", end="2020-01-16")

    for back_date in back_dates:
        print(back_date)
        get_newsapi_on_date(back_date, intervals=12, source=source)
        process_source_on_date(back_date, source=source)