Included APIs
=============

NewsAPI.org
-----------

This library uses the `NewsAPI.org <https://newsapi.org/>`_ service endpoints using the [newsapi-python](https://github.com/mattlisiv/newsapi-python) package.

The API itself is `very well documented <https://newsapi.org/docs>`_. The free "Developer" plan is limited to 500 requests per day, and it requires attribution near to the implementation. NewsAPI specifically says that the API is throttled by requests, not results. I.e., `"it doesn't matter how many results you get back" <https://newsapi.org/pricing>`_. That may be technically true. However:

- the results are paginated and the service will only send 20 results back at maximum. This means you need to traverse pages.
- the developer plan apparently only lets you see the first 100 results from a request. So you cannot see beyond the fifth page. When I requested data from a single source (e.g., ``fox-news``) for a single day, the service said there were 111 results, but the service errors if you try to return results 100-111. This means that you need to request smaller batches (e.g., half days may work) and use the total_results to determine if you missed something.
- Also undocumented until you get the error: "Developer accounts are limited to 500 requests over a 24 hour period (250 requests available every 12 hours)."

Of course all these mean more requests. With 500 requests per day, in theory you could pull a max of 10,000 results per day, though we will lose a lot in the partially filled pagination.

Issues
^^^^^^^^^^^^^^
- Some of the content fields, particularly in The Washington Post, contain newlines. And sometimes more than one (e.g., they include the header which has a newline on either side). This messes with the CSVs. Maybe get around this by quoting those fields?
- Meanwhile, the Reuters feed produces multiple lines (up to 3 is typical) for the same article headline, with different URLS (e.g., one is in "topnews" and one is in "worldnews").
- Reuters and Associated Press produce far more headlines than anyone else, and I typically have to split requests for these sources. So far reqesting data from 2-hour periods (12 intervals per day) seems to work out.
- With the free version, you can only request data from the past month. Ouch.

Notes
^^^^^^^^^^^^^^
- NewsAPI pagination starts at 1


NYT API
-----------
On the third day of successfully pulling New York Times headlines from newsAPI.org, that source was dropped from the newsapi results. The last day they produced was January 11, 2020. As of April 2020 newsAPI.org does include nytimes.com results. But now I don't trust them. So instead I use https://developer.nytimes.com/apis

Article Search
^^^^^^^^^^^^^^

This provides a pretty straightforward feed of articles. Each request is paginated by 10 results, and they say they limit results to 100 pages (i.e., 1000 results). Requesting one day at a time produces 100-200 articles per day. Cool.

However, it turns out that they do to have a request rate limiter, and I hit it by asking for 168 results (16 pages) within the speed of a sequential python loop. I tried putting in a 5 second wait between requests, but also hit the error. I put in a 10 second wait. It worked. I checked the API FAQ:

.. pull-quote::

  there are two rate limits per API: 4,000 requests per day and 10 requests per minute. You should sleep 6 seconds between calls to avoid hitting the per minute rate limit. If you need a higher rate limit, please contact us at code@nytimes.com.

OK FINE. With 6 seconds between requests I could hit their server continuously for over 6 hours.

Notes
^^^^^^^^^^^^^^
- NYT API pagination starts at 0
- The NYT API kicks back a lot of information, including links to every photo in every article. This is overkill for my purposes, but means that I'll need to process the json files in a different way to put them into the format of the newsAPI dataframe.