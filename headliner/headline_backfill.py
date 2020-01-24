#!/home/will/anaconda3/envs/headliner/bin/python

from datetime import datetime, timedelta
from headline_collector import get_newsapi_on_date
from headline_processor import process_source_on_date
from nyt_headline_collector import get_nyt_on_date
import glob
import os
import pandas as pd

# sources = ["associated-press"]
# for source in sources:

#     back_dates = pd.date_range(start="2020-01-14", end="2020-01-16")

#     for back_date in back_dates:
#         print(back_date)
#         get_newsapi_on_date(back_date, intervals=12, source=source)
#         process_source_on_date(back_date, source=source)


back_dates = pd.date_range(start="2020-01-12", end="2020-01-22")

for back_date in back_dates:
    print(back_date)
    get_nyt_on_date(back_date)