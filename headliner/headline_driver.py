#!/home/will/anaconda3/envs/headliner/bin/python
from datetime import datetime, timedelta
import logging
from headline_collector import get_newsapi_on_date
from headline_processor import process_source_on_date

logging.basicConfig(
    filename='/home/will/Projects/headliner/headliner.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )
logger = logging.getLogger(__name__)

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
yesterday = today - timedelta(days=1)

newsapi_sources = ["fox-news", "msnbc", "abc-news", "the-washington-post", "reuters", "associated-press"]

for source in newsapi_sources:
    logger.info(f"Retrieving {source} from newsapi.org")
    get_newsapi_on_date(yesterday, intervals=8, source=source)
    process_source_on_date(yesterday, source=source)