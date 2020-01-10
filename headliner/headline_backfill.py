#!/home/will/anaconda3/envs/headliner/bin/python

from datetime import datetime, timedelta
import logging
from headline_collector import get_source_on_date
import glob
import os

sources = ["fox-news", "the-new-york-times"]
store_dir = "/home/will/Projects/headliner/datastore/raw/"

# ~30 requests per day fro
# 4 days of 2 sources = ~100 requests

# 250 requests per 12 hour means gather real-time + 7 days of backfill every 12 hours should be "safe"
# would be great to automate the backfill to run every 12 hours
# and maybe find the max number of requests per day

for source in sources:

    filenames = sorted(glob.glob(os.path.join(store_dir, source, "*.json")))

    first_file = filenames[0]
    first_date = datetime.strptime(
        first_file.split(source + "-")[1].split("T")[0], "%Y-%m-%d"
    )

    n_days = 6

    back_dates = [first_date - timedelta(days=x) for x in range(1, n_days+1)]

    for back_date in back_dates:
        get_source_on_date(back_date, intervals=6, source=source)