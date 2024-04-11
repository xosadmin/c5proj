import unittest
from ..app import *
from ..randomprofile import *

generatedEmail = randomEmail()
generatedPassword = generatePassword(10)

class TestAuth(unittest.TestCase):
    # def setUp(self):
    #     app.config['TESTING'] = True
    #     self.app = app.test_client()

    def test_email_exists(self):
        email = "test@test.com"
        getReturn = app.checkEmail(email)
        self.assertEqual(getReturn, 0) 
        # Test checkEmail() function
        # The "test@test.com" already in the database. It is expected to return 0

    def test_dologin_success(self):
        with self.app as client:
            response = client.post('/dologin', data={
                'username': 'test@test.com',  
                'password': '123'
            })
            self.assertEqual(response.status_code, 302)  
            self.assertTrue('/requests' in response.location, "Should redirect to the home page")

    def test_dologin_failure(self):
        #Test that an invalid login returns to the login page with an error.
        with self.app as client:
            response = client.post('/dologin', data={
                'username': 'invalidUser@test.com',
                'password': 'wrongPassword'
            })
           
            self.assertEqual(response.status_code, 302)  
            self.assertTrue('/login?errormsg' in response.location, "Should redirect back to login with an error")

    def test_register_post(self):
        with self.app as client:
            response = self.app.post('/doregister', data={'email': generatedEmail, 'password': generatedPassword})

            self.assertEqual(response.status_code, 200)  
            self.assertTrue('/doregister' in response.location)


if __name__ == '__main__':
    unittest.main()