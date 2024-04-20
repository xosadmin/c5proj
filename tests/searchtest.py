import unittest
import app
from flask import Flask

class TestSearchOperations(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__).test_client()
        self.app.testing = True

    def test_doChatSearch_post_success(self):
        with self.app as client:
            response = client.post('/dochatsearch', data={
                'keyword': 'hello'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn("We have found result(s)", str(response.data))

    def test_doChatSearch_get_invalid(self):
        with self.app as client:
            response = client.get('/dochatsearch')
            self.assertEqual(response.status_code, 302)
            self.assertTrue('search_result.html' in response.location)

    def test_doCommSearch_post_success(self):
        with self.app as client:
            response = client.post('/docommsearch', data={
                'keyword': 'community topic'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn("We have found result(s)", str(response.data))

    def test_doCommSearch_get_invalid(self):
        with self.app as client:
            response = client.get('/docommsearch')
            self.assertEqual(response.status_code, 302)
            self.assertTrue('search_result.html' in response.location)

    def test_doReqSearch_post_success(self):
        with self.app as client:
            response = client.post('/doreqsearch', data={
                'keyword': 'request query'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn("We have found result(s)", str(response.data))

    def test_doReqSearch_get_invalid(self):
        with self.app as client:
            response = client.get('/doreqsearch')
            self.assertEqual(response.status_code, 302)
            self.assertTrue('search_result.html' in response.location)

if __name__ == '__main__':
    unittest.main()
