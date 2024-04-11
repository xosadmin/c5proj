import unittest
from ..app import doregister

class TestDoregister(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        

    def test_register_post(self):
        
        response = self.app.post('/doregister', data={'email': 'test@example.com', 'password': 'securepassword'})
        


if __name__ == '__main__':
    unittest.main()