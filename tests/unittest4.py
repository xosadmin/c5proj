import unittest
from ..app import dologin

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_dologin_success(self):
        with self.app as client:
            response = client.post('/dologin', data={
                'username': 'validUser',  
                'password': 'validPassword'
            })
            self.assertEqual(response.status_code, 302)  
            self.assertTrue('/home' in response.location, "Should redirect to the home page")

    def test_dologin_failure(self):
        """Test that an invalid login returns to the login page with an error."""
        with self.app as client:
            response = client.post('/dologin', data={
                'username': 'invalidUser',
                'password': 'wrongPassword'
            })
           
            self.assertEqual(response.status_code, 302)  
            self.assertTrue('/login?error' in response.location, "Should redirect back to login with an error")
    



if __name__ == '__main__':
    unittest.main()