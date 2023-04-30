import glob
import json
import logging
import os
from datetime import timedelta
import pandas as pd

logging.basicConfig(
    filename='/Users/wckoeppen/work/projects/headliner/headliner.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
    )
logger = logging.getLogger(__name__)


def find_files(base_dir, begin_date, end_date):

    n_days = int((end_date - begin_date).total_seconds()/60/60/24)
    date_list = [begin_date + timedelta(days=x) for x in range(n_days+1)]

    search_strs = []

    for date in date_list:
        search_strs.append(date.strftime('%Y-%m-%d'))

    filenames=[]

    for search_str in search_strs:

        filenames += sorted(glob.glob(os.path.join(base_dir, '*' + search_str + '*.json')))

    return filenames


def process_nytsource_on_date(date, source='the-new-york-times'):
    source_dir = f"/Users/wckoeppen/work/projects/headliner/datastore/raw/{source}/"
    out_dir = f"/Users/wckoeppen/work/projects/headliner/datastore/processed/{source}/"

    filenames = find_files(source_dir, date, date)

    def concat_files(file_list):

        results = []

        for filename in file_list:

            with open(filename, "r") as file:
                to_add = json.load(file)

            authors = []
            titles = []
            descriptions = []
            urls = []
            urlToImages = []
            publishedAts = []
            contents = []

            for item in to_add['response']['docs']:
                authors.append(item['byline']['original'])
                titles.append(item['headline']['main'])
                descriptions.append(item['abstract'])
                urls.append(item['web_url'])
                publishedAts.append(item['pub_date'])
                contents.append(item['lead_paragraph'])

                if len(item['multimedia']) > 0:
                    urlToImages.append('https://static01.nyt.com/' + item['multimedia'][0]['url'])
                else:
                    urlToImages.append(None)

            to_add = pd.DataFrame(
                {
                    'author': authors,
                    'title': titles,
                    'description': descriptions,
                    'url': urls,
                    'urlToImage': urlToImages,
                    'publishedAt': publishedAts,
                    'content': contents
                }
            )
            to_add['source.id'] = source
            to_add['source.name'] = 'The New York Times'

            results.append(to_add)

        return pd.concat(results, ignore_index=True)

    concatted = concat_files(filenames)
    concatted.to_csv(os.path.join(out_dir, f"{source}-{date.strftime('%Y-%m-%d')}.csv"), index=False)

    return True