from selenium import webdriver
import unittest

class FlaskAppTest(unittest.TestCase):
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000")

    def tearDown(self):
        self.driver.quit()
    
    def test_title(self):
        self.assertEqual("Adventurer Guild", self.driver.title)


if __name__ == "__main__":
    unittest.main(verbosity=2)