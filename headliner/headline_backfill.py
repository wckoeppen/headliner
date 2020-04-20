#!/home/will/anaconda3/envs/headliner/bin/python

from datetime import datetime, timedelta
from headline_collector import get_newsapi_on_date
from headline_processor import process_source_on_date
from nyt_headline_processor import process_nytsource_on_date
from nyt_headline_collector import get_nyt_on_date
import glob
import os
import pandas as pd


### newsapi
# sources = ["abc-news", "reuters"]

# for source in sources:

#     back_dates = pd.date_range(start="2020-01-22", end="2020-01-24")

#     for back_date in back_dates:
#         print(back_date)
#         get_newsapi_on_date(back_date, intervals=12, source=source)
#         process_source_on_date(back_date, source=source)

### nyt api
back_dates = pd.date_range(start="2020-04-16", end="2020-04-19")

get_nyt_on_date(datetime(2020, 4, 17, 0, 0))
#
for back_date in back_dates:
    print(back_date)
    process_nytsource_on_date(back_date)