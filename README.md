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
- note: NewsAPI pagination starts at 1
- Lastly, with the free version, you can only request data from the past month. Ouch.

### Issues
- Some of the content fields, particularly in The Washington Post, contain newlines. And sometimes more than one (e.g., they include the header which has a newline on either side). This messes with the CSVs. Maybe get around this by quoting those fields?
- Meanwhile, the Reuters feed produces multiple lines (up to 3 is typical) for the same article headline, with different URLS (e.g., one is in "topnews" and one is in "worldnews").
- Reuters and Associated Press produce far more headlines than anyone else, and I typically have to split requests for these sources. So far reqesting data from 2-hour periods (12 intervals per day) seems to work out.

## NYT API
On the third day of successfully pulling New York Times headlines from newsAPI.org, that source was dropped from the newsapi results. The last day they produced was January 11, 2020. So now you have to use https://developer.nytimes.com/apis

### Article Search API
This provides a pretty straightforward feed of articles. Each request is paginated by 10 results, and they say they limit results to 100 pages (i.e., 1000 results). Requesting one day at a time produces 100-200 articles per day. Cool.

However, it turns out that they do seem to have a request rate limiter, and I hit it by asking for 168 results (16 pages) in a python loop. I tried putting in a 5 second wait between requests, but also hit the error. I put in a 10 second wait. It worked. I checked the API FAQ:
> ... there are two rate limits per API: 4,000 requests per day and 10 requests per minute. You should sleep 6 seconds between calls to avoid hitting the per minute rate limit. If you need a higher rate limit, please contact us at code@nytimes.com.

OK FINE. That's not bad, they're saying that with 6 seconds between requests I could hit their server continuously for over 6 hours.

Notes:
- NYT API pagination starts at 0
- The NYT API kicks back a lot of information, including links to every photo in every article. This is overkill for my purposes, but means that I'll need to process the json files in a different way to put them into the format of the newsAPI dataframe.

## Comparing bias
https://www.adfontesmedia.com/interactive-media-bias-chart/ - the first google hit is a media company. Weird? But they list AP and Reuters as the most reliable with least bias. They list The New York times as skews left, and InfoWars as Hyper-Partisan Right. The Hill comes up in the center, somewhat surprisingly. Fox News on the right is the equivalent of MSNBC on the left
https://www.allsides.com/media-bias/media-bias-chart - they smartly split the opinion sections from the online news orgs. They have NPR, Reuters, and Ap as the center
https://sharylattkisson.com/2019/04/media-bias-chart-analysis/ - Sharyl Attkisson says the APO is to the left as much as Fox News is to the right. Meanwhile she labels The New York Times as far left along with NPR, with InfoWars as mid-right. She labels Snopes as mid left. Her commenters say things like "I view InfoWars as further left." Amazing. I'd label this as unreliable.

# To Do List
- begin prototyping out some visualizations
   - word clouds?
   - keyword usage over time?
   - location bylines?
   - would be nice to be able to highlight keyword combinations (e.g., coronavirus + hoax) and see the full results
   - author histograms
   - number of articles per time, maybe count binned by day or week.
 - handle any errors in responses? (this happened once over the past 3 months, where the NYT json response errored on page 10)