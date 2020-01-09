import json
import pandas as pd
import math

filename = "headline-store-json/fox-news-2020-01-01-00-p001.json"

source = "fox-news"
page = 1

with open(filename) as file:
    _this_json = json.load(file)

    total_results = 21
#    total_results = _this_json["totalResults"]

    print(total_results)

    if total_results > 20:

        if total_results > 100:
            print("Too many results to get all of them, reduce time interval.")

        else:
            n_pages = math.ceil(total_results / 20.)
                    
            for this_page in range(page + 1, n_pages + 1):
                print(f"Will get page {this_page} from {source}")
                # get_results(page=page, source=source)

