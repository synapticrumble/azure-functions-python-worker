import unittest

from azure.worker import testutils


class TestFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.webhost = testutils.start_webhost()

    @classmethod
    def tearDownClass(cls):
        cls.webhost.stop()
        cls.webhost = None

    def test_return_str(self):
        r = self.webhost.request('GET', 'return_str')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, 'Hello World!')

    def test_return_context(self):
        r = self.webhost.request('GET', 'return_context')
        self.assertEqual(r.status_code, 200)

        data = r.json()

        self.assertEqual(data['method'], 'GET')
        self.assertEqual(data['ctx_func_name'], 'return_context')
        self.assertIn('return_context', data['ctx_func_dir'])
        self.assertIn('ctx_invocation_id', data)

    def test_get_method_request(self):
        r = self.webhost.request(
            'GET', 'return_request',
            params={'a': 1, 'b': ':%)'},
            headers={'xxx': 'zzz'})

        self.assertEqual(r.status_code, 200)

        req = r.json()

        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['params'], {'a': '1', 'b': ':%)'})
        self.assertEqual(req['headers']['xxx'], 'zzz')

        self.assertIn('return_request', req['url'])

    def test_post_method_request(self):
        r = self.webhost.request(
            'POST', 'return_request',
            params={'a': 1, 'b': ':%)'},
            headers={'xxx': 'zzz'},
            data={'key': 'value'})

        self.assertEqual(r.status_code, 200)

        req = r.json()

        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['params'], {'a': '1', 'b': ':%)'})
        self.assertEqual(req['headers']['xxx'], 'zzz')

        self.assertIn('return_request', req['url'])

        self.assertEqual(req['get_body'], 'key=value')