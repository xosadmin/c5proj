import unittest
import app

class TestPaymentOperations(unittest.TestCase):
    def setUp(self):
        self.app = app.app
        app.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.generatedItemID = 'item123'  
        self.generatedUserID = 'user123'  

    def test_doPayment_success(self):
        response = self.client.get(f'/dopayment/{self.generatedItemID}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Payment for', str(response.data))

    def test_doPayment_failure(self):
        invalid_item_id = 'invalidItem123'  
        response = self.client.get(f'/dopayment/{invalid_item_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', str(response.data))

if __name__ == '__main__':
    unittest.main()

