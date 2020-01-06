# headliner
Scripts to pull and track headlines from news APIs.

## NewsAPI.org
This library uses the [NewsAPI.org](https://newsapi.org/) service endpoints using the [newsapi-python](https://github.com/mattlisiv/newsapi-python) package.

The API itself is [very well documented](https://newsapi.org/docs). The free "Developer" plan is limited to 500 requests per day, and it requires attribution near to the implementation.

NewsAPI specifically says that the API is throttled by requests, not results. I.e., ["it doesn't mantter how many results you get back"](https://newsapi.org/pricing). That may be technically true. However:
- the results are paginated and the service will only send 20 results back at maximum. This means you need to traverse pages.
- the developer plan apparently only lets you see the first 100 results from a request. So you cannot see beyond the fifth page. When I requested data from a single source (e.g., `fox-news`) for a single day, the service said there were 111 results, but the service erros if you try to return results 100-111. This means that you need to request smaller batches (e.g., half days may work) and use the total_results to determine if you missed something.

Of course all these mean more requests. With 500 requests per day, in theory you could pull a max of 10,000 results per day, though we will lose a lot in the partially filled pagination.