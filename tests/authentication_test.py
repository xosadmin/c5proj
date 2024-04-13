import unittest
import app
import getandset as gs
import llm
import login_process as lp
import randomprofile as rp

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = app.app
        self.gs = gs
        self.llm = llm
        self.lp = lp
        app.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.generatedEmail = str(rp.randomEmail())
        self.generatedPassword = str(rp.generatePassword(10))

    def test_email_exists(self):
        with self.app.test_request_context():
            email = "test@test.com"
            getReturn = self.gs.checkEmail(email)
            self.assertEqual(getReturn, -1)

    def test_register_post(self):
        response = self.client.post('/doregister', data={
            'email': self.generatedEmail, 
            'password': self.generatedPassword,
            'pincode': "1234"
        })
        self.assertEqual(response.status_code, 200)

    def test_dologin_success(self):
        response = self.client.post('/dologin', data={
            'email': "test@test.com",
            'password': "123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/profile', response.headers['Location'])

    def test_dologin_failure(self):
        response = self.client.post('/dologin', data={
            'email': 'invalidUser@test.com',
            'password': 'wrongPassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?errormsg', response.headers['Location'])

if __name__ == '__main__':
    unittest.main()