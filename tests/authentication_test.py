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
            self.assertEqual(getReturn, 0)

    def test_register_post(self):
        response = self.client.post('/doregister', data={
            'email': self.generatedEmail, 'password': self.generatedPassword
        })
        self.assertEqual(response.status_code, 200)

    def test_dologin_success(self):
        response = self.client.post('/dologin', data={
            'username': self.generatedEmail,
            'password': self.generatedPassword
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/requests', response.headers['Location'])

    def test_dologin_failure(self):
        response = self.client.post('/dologin', data={
            'username': 'invalidUser@test.com',
            'password': 'wrongPassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?errormsg', response.headers['Location'])

if __name__ == '__main__':
    unittest.main()