from functools import wraps


# Since the application is expected to be single threaded a simple cache and log will be started each run.

global_cache = {}


global_metrics = {}


def cache_and_log(func):
    """ Wrapper for function to log and cache results. """

    @wraps(func)
    def wrapper(*args, **kwargs):
        connector = str(args[0])  # First arg is self
        connector_cache = global_cache.setdefault(connector, {})
        connector_metrics = global_metrics.setdefault(connector, {'requests': 0, 'responses': 0, 'cached_calls': 0})
        uri = args[1] # Second arg is uri for connector.get
        if uri in connector_cache:
            connector_metrics['cached_calls'] += 1
            return connector_cache[uri]
        connector_metrics['requests'] += 1
        try:
            result = func(*args, **kwargs)
            connector_metrics['responses'] += 1
            connector_cache[uri] = result  # Cache result
            return result
        except Exception as e:
            raise e  # Re raise exception after logging metrics.
    
    return wrapper


def api_metrics_to_json():
    """ Format metrics to json. """
    return {
        'totalQueries': sum([metrics['requests'] for metrics in global_metrics.values()]),
        'totalCachedQueries': sum([metrics['cached_calls'] for metrics in global_metrics.values()]),
        'apis': [
            {
                'name': key,
                'metrics': {
                    'totalRequests': metrics['requests'],
                    'totalResponses': metrics['responses']
                } 
             } for key, metrics in global_metrics.items()
        ]
    }