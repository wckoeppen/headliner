# headliner
Scripts to pull and track headlines from news APIs.

## NewsAPI.org
This library uses the [NewsAPI.org](https://newsapi.org/) service endpoints.

The API is mostly well documented, but here are some notes:
- The free plan is limited to 500 requests per day
- it requires attribution.

NewsAPI specifically says that the API is throttled by requests, not results. I.e., ["it doesn't mantter how many results you get back"](https://newsapi.org/pricing). That may be technically true. However:
- the results are paginated and a request will only send, at max, 20 results back.
- the developer plan apparently only lets you see the first 100 results from a request. So you cannot see beyond page 5. When I requested data from a single source (e.g., `fox-news`) for a single day, the service said there were 111 results, but the service erros if you try to return results 100-111.
