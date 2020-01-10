from datetime import datetime, timedelta
import logging
from headline_collector import get_source_on_date

sources = ["fox-news","the-new-york-times"]

for i in range(20,27):
    for src in sources:
        get_source_on_date(datetime(2019,12,i), intervals=6, source=src, verbose=True)

# must redo the NYT on Dec 26th (missed page 2 of the last request).