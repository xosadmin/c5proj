import unittest
import app
from flask import Flask

class TestRequestOperations(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__).test_client()
        self.app.testing = True

    def test_donewrequests_post_success(self):
        with self.app as client:
            response = client.post('/donewrequest', data={
                'title': 'New Request Title',
                'content': 'This is the content of the new request.',
                'rewards': '100',
                'timelimit': '7'
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue('requests' in response.location)

    def test_donewrequests_get_invalid(self):
        with self.app as client:
            response = client.get('/donewrequest')
            self.assertEqual(response.status_code, 302)
            self.assertTrue('newRequest?msg=Invalid Request!' in response.location)

    def test_doAcceptRequest_post_success(self):
        with self.app as client:
            response = client.post('/doacceptrequest/valid-request-id')
            self.assertEqual(response.status_code, 302)
            self.assertTrue('todoList' in response.location)

    def test_doAcceptRequest_get_invalid(self):
        with self.app as client:
            response = client.get('/doacceptrequest/valid-request-id')
            self.assertEqual(response.status_code, 302)  

    def test_doAnswerRequest_post_success(self):
        with self.app as client:
            response = client.post('/doanswerrequest', data={
                'userID': 'valid-user-id',
                'rewards': '50',
                'requestID': 'valid-request-id',
                'content': 'This is the answer content for the request.'
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue('todoList' in response.location)

    def test_doAnswerRequest_get_invalid(self):
        with self.app as client:
            response = client.get('/doanswerrequest')
            self.assertEqual(response.status_code, 302)  

if __name__ == '__main__':
    unittest.main()
