import unittest
from ..app import checkEmail

class TestAuth(unittest.TestCase):
    def test_email_exists(self):
        email = "test@test.com"
        getReturn = app.checkEmail(email)
        self.assertEqual(getReturn, 0) 
        # Test checkEmail() function
        # The "test@test.com" already in the database. It is expected to return 0



if __name__ == '__main__':
    unittest.main()