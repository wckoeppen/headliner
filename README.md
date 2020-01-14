# headliner
Scripts to pull and track headlines from news APIs.

## NewsAPI.org
This library uses the [NewsAPI.org](https://newsapi.org/) service endpoints using the [newsapi-python](https://github.com/mattlisiv/newsapi-python) package.

The API itself is [very well documented](https://newsapi.org/docs). The free "Developer" plan is limited to 500 requests per day, and it requires attribution near to the implementation.

NewsAPI specifically says that the API is throttled by requests, not results. I.e., ["it doesn't mantter how many results you get back"](https://newsapi.org/pricing). That may be technically true. However:
- the results are paginated and the service will only send 20 results back at maximum. This means you need to traverse pages.
- the developer plan apparently only lets you see the first 100 results from a request. So you cannot see beyond the fifth page. When I requested data from a single source (e.g., `fox-news`) for a single day, the service said there were 111 results, but the service errors if you try to return results 100-111. This means that you need to request smaller batches (e.g., half days may work) and use the total_results to determine if you missed something.
- Also undocumented until you get the error: "Developer accounts are limited to 500 requests over a 24 hour period (250 requests available every 12 hours)."

Of course all these mean more requests. With 500 requests per day, in theory you could pull a max of 10,000 results per day, though we will lose a lot in the partially filled pagination.
- Lastly, with the free version, you can only request data from the past month. Ouch.

### Issues
- Some of the content fields, particularly in The Washington Post, contain newlines. And sometimes more than one (e.g., they include the header which has a newline on either side). This messes with the CSVs. Maybe get around this by quoting those fields?
- Meanwhile, the Reuters feed produces multiple lines (up to 3 is typical) for the same article headline, with different URLS (e.g., one is in "topnews" and one is in "worldnews").

## NYT API
On the third day of successfully pulling New York Times headlines from newsAPI.org, that source was dropped from the newsapi results. The last day they produced was January 11, 2020. So now you have to use https://developer.nytimes.com/apis

### real-time feed
This provides a feed of all the current articles of the current day.

### archive
https://api.nytimes.com/svc/search/v2/articlesearch.json?&begin_date=20120101&end_date=20120101&api-key=your-api-key
https://api.nytimes.com/svc/search/v2/articlesearch.json?&begin_date=20200110&end_date=20200111&api-key=your-api-key

- Date search of the archive from recent articles only seems to produce results from AP and Reuters. I can see articles from NYT authors from earlier.
- Sometimes the source is listed as "The New York Times" and other times it says "New York Times"
- Bylines have different formats. "By AUTHOR". Can this be true?

## Comparing bias
https://www.adfontesmedia.com/interactive-media-bias-chart/ - the first google hit is a media company. Weird? But they list AP and Reuters as the most reliable with least bias. They list The New York times as skews left, and InfoWars as Hyper-Partisan Right. The Hill comes up in the center, somewhat surprisingly. Fox News on the right is the equivalent of MSNBC on the left
https://www.allsides.com/media-bias/media-bias-chart - they smartly split the opinion sections from the online news orgs. They have NPR, Reuters, and Ap as the center
https://sharylattkisson.com/2019/04/media-bias-chart-analysis/ - Sharyl Attkisson says the APO is to the left as much as Fox News is to the right. Meanwhile she labels The New York Times as far left along with NPR, with InfoWars as mid-right. She labels Snopes as mid left. Her commenters say things like "I view InfoWars as further left." Amazing. I'd label this as unreliable.
