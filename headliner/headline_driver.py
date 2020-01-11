#!/home/will/anaconda3/envs/headliner/bin/python
from datetime import datetime, timedelta
import logging
from headline_collector import get_source_on_date, process_source_on_date


logging.basicConfig(
    filename='/home/will/Projects/headliner/headliner.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )
logger = logging.getLogger(__name__)

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
yesterday = today - timedelta(days=1)

def get_yesterdays_news(source):
    logger.info(f"Retrieving {source} from newsapi.org")
    get_source_on_date(yesterday, intervals=6, source=source)
    process_source_on_date(yesterday, source=source)

sources = ["fox-news","the-new-york-times"]
for src in sources:
    get_yesterdays_news(src)