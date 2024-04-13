import unittest
import app
from flask import Flask

class TestDonewThreads(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__).test_client()
        self.app.testing = True

    def test_donewthreads_post_success(self):
       with self.app as client:
            response = client.post('/donewthread', data={
                'title': 'New Thread Title',
                'content': 'This is the content of the new thread.'
            })
           
            self.assertEqual(response.status_code, 302)  
            self.assertTrue('communityPage' in response.location)  
    
    def test_donewthreads_get_invalid(self):
        with self.app as client:
            response = client.get('/donewthread')
        self.assertEqual(response.status_code, 302)

    def test_doNewThreadReply_post_success(self):
        with self.app as client:
            response = client.post('/donewthreadreply', data={
                'threadID': 'some-unique-thread-id',
                'content': 'Reply content for the thread.'
            })
            self.assertEqual(response.status_code, 302)  
            self.assertTrue('communityPage' in response.location)  

    def test_doNewThreadReply_get_invalid(self):
        with self.app as client:
            response = client.get('/donewthreadreply')
            self.assertEqual(response.status_code, 302)  
            self.assertTrue('newThread?errmsg=Invalid Request!' in response.location)  

if __name__ == '__main__':
    unittest.main()
