#!/home/will/anaconda3/envs/headliner/bin/python
from datetime import datetime, timedelta
import logging
from headline_collector import get_newsapi_on_date
from headline_processor import process_source_on_date
from nyt_headline_collector import get_nyt_on_date
from nyt_headline_processor import process_nytsource_on_date

logging.basicConfig(
    filename='/home/will/Projects/headliner/headliner.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )
logger = logging.getLogger(__name__)

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
yesterday = today - timedelta(days=1)

### Get NYT from source
logger.info(f"Retrieving the-new-york-times from NYT developer API")
get_nyt_on_date(yesterday)
process_nytsource_on_date(yesterday)

### Get news api sources
newsapi_sources = ["fox-news"] #, "msnbc", "nbc-news", "the-washington-post", "associated-press", "abc-news", "cnn"]

for source in newsapi_sources:
    logger.info(f"Retrieving {source} from newsapi.org")
    get_newsapi_on_date(yesterday, intervals=12, source=source)
    process_source_on_date(yesterday, source=source)