import unittest


from currency_api.utils.metrics import global_metrics, global_cache, cache_and_log


class TestMetrics(unittest.TestCase):

    def setUp(self):
        """ Clear cache. """
        global_cache.clear()
        global_metrics.clear()

    def test_log_two_unique_requests(self):
        obj = 'obj'
        @cache_and_log
        def logger(obj, key):
            return {'result': key}
        
        logger(obj, 'hello')
        logger(obj, 'data')

        self.assertEqual(len(global_cache), 1)
        logger_cache = global_cache[obj]
        logger_metrics = global_metrics[obj]
        self.assertEqual(len(logger_cache), 2)
        self.assertEqual(logger_cache['hello'], {'result': 'hello'})
        self.assertEqual(logger_cache['data'], {'result': 'data'})

        self.assertEqual(len(global_metrics), 1)
        self.assertEqual(logger_metrics['cached_calls'], 0)
        self.assertEqual(logger_metrics['requests'], 2)
        self.assertEqual(logger_metrics['responses'], 2)

    def test_log_two_unique_requests_and_cache(self):
        obj = 'obj_1'
        @cache_and_log
        def logger(obj, key):
            return {'result': key}
        
        logger(obj, 'hello')
        logger(obj, 'data')
        logger(obj, 'hello')

        self.assertEqual(len(global_cache), 1)
        logger_cache = global_cache[obj]
        logger_metrics = global_metrics[obj]
        self.assertEqual(len(logger_cache), 2)
        self.assertEqual(logger_cache['hello'], {'result': 'hello'})
        self.assertEqual(logger_cache['data'], {'result': 'data'})

        self.assertEqual(len(global_metrics), 1)
        self.assertEqual(logger_metrics['cached_calls'], 1)
        self.assertEqual(logger_metrics['requests'], 2)
        self.assertEqual(logger_metrics['responses'], 2)

    def test_log_two_unique_requests_and_two_cached(self):
        obj = 'obj'
        @cache_and_log
        def logger(obj, key):
            return {'result': key}
        
        logger(obj, 'hello')
        logger(obj, 'test')
        logger(obj, 'hello')
        logger(obj, 'test')

        self.assertEqual(len(global_cache), 1)
        logger_cache = global_cache[obj]
        logger_metrics = global_metrics[obj]
        self.assertEqual(len(logger_cache), 2)
        self.assertEqual(logger_cache['hello'], {'result': 'hello'})
        self.assertEqual(logger_cache['test'], {'result': 'test'})

        self.assertEqual(len(global_metrics), 1)
        self.assertEqual(logger_metrics['cached_calls'], 2)
        self.assertEqual(logger_metrics['requests'], 2)
        self.assertEqual(logger_metrics['responses'], 2)

    def test_log_request_only_no_response(self):
        obj = 'obj'
        
        @cache_and_log
        def logger(obj, key):
            raise Exception('error')
        
        try:
            logger(obj, 'hello')
        except:
            pass

        self.assertEqual(len(global_cache), 1)
        logger_cache = global_cache[obj]
        logger_metrics = global_metrics[obj]
        self.assertEqual(len(logger_cache), 0)  # Nothing is logged since it failed.
        self.assertIsNone(logger_cache.get('hello'))

        self.assertEqual(len(global_metrics), 1)
        self.assertEqual(logger_metrics['cached_calls'], 0)
        self.assertEqual(logger_metrics['requests'], 1)
        self.assertEqual(logger_metrics['responses'], 0)



if __name__ == '__main__':
    unittest.main()