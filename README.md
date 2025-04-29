# currency-api

The project uses flask as restful api alongside inbuilt python requests module for making api calls served using waitress.

## How to run

Install module using `python pip -e .` or as a package.

Run the server.py and it will be served at localhost:5000

endpoints:
  /exchangeRates/<currency>?symbols={s1, s2, ...}
  /metrics


# Architecture

/dao -> abstract interface for restful api and future database functionality.

/dao/blueprints -> API endpoint blue prints are described in here.

/data -> Currency data related interfaces.

/data/connectors -> Base api connecting interface that describes the functionality subclasses must implement incase of multiple 
                    data collecting capabalities using apis. Allows for future extendability.
                    
/data/connectors/apis -> Api connector implementations for currency exchange. APIs might have different return results and this allows a consistant interface based on parent connector.

/data/connectors/types -> Simple typing for currency and currency rates. Could be improved later for complex classes etc.

/utils/metrics -> Contains a wrapper that can be placed infront of the `get` call for the api connector that logs and caches the uri and result locally.
                  Method to return the cached metrics as a json format for api response.


# Unit tests

Single unit test file to test the metric and caching collection of api requests.

Ran out of time and would have added some more tests for testing the responses from api get requests.



# Future improvements.

Added cached metric to see when repeat calls are made. Since caching is done based on uri, the currencies provided for the rates are sorted which allows for same keys when order is different.
Improve the caching and metric collection when the application is not single threaded.
Another improvement for caching is setting a timeout when the cache is refreshed. This would be like 1 hour or 2 hours or daily etc.
Storing response codes as metrics, such as timeout, bad requests, internal errors, no content etc.
Project is setup for easy extensibility using inheritance for the api connectors.
Another change would be to remove the get function from the api class into a single function in a utility script, the cache does not need to be specific to a connector object and can be a dictionary of urls mapped to parsed json result. This allows the function to be mocked for testing making it easier to write tests for the api connectors and results when set data can be returned.
Also would add more tests and checks for data validation for the returned results from the apis. There may be edge cases somes values are string or not valid numbers and would crash the application.






