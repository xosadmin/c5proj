import unittest
import app
from flask import Flask

class TestChatOperations(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__).test_client()
        self.app.testing = True

    def test_donewChat_post_success(self):
        with self.app as client:
            response = client.post('/newchat', data={
                'dstuser': '12345',
                'content': 'Hello, this is a new chat message.'
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue('chat' in response.location)

    def test_donewChat_get_invalid(self):
        with self.app as client:
            response = client.get('/newchat')
            self.assertEqual(response.status_code, 302)
            self.assertTrue('chatPage' in response.location)

    def test_doChatReply_post_success(self):
        with self.app as client:
            response = client.post('/dochatreply', data={
                'chatID': 'chat-123',
                'content': 'This is a reply to an existing chat.'
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue('chat' in response.location)

    def test_doChatReply_get_invalid(self):
        with self.app as client:
            response = client.get('/dochatreply')
            self.assertEqual(response.status_code, 302)
            self.assertTrue('chatPage' in response.location)

    

if __name__ == '__main__':
    unittest.main()
