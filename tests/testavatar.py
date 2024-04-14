import unittest
import app
import randomprofile as rp

class TestAvatarOperations(unittest.TestCase):
    def setUp(self):
        self.app = app.app
        app.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.generatedUserID = '12345'  
        self.generatedAvatarID = 'avatar123'  

    def test_doSetAvatar_success(self):
        response = self.client.get(f'/setavatar/{self.generatedAvatarID}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Avatar updated.', str(response.data))

    def test_doSetAvatar_failure(self):
        invalid_avatar_id = 'invalid123'  
        response = self.client.get(f'/setavatar/{invalid_avatar_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', str(response.data))

if __name__ == '__main__':
    unittest.main()