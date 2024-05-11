from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import apps.randomprofile as rp
import tests.selenium_preparation as sp

randomEmail = rp.randomEmail()
randomPassword = rp.randomSessionKey(10)
pin_code = rp.randomPinCode()

class FlaskAppTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Chrome()
        sp.register_new_account(randomEmail,randomPassword,pin_code) # Create a test account
        print("WARNING: DO NOT CLOSE REGISTRATION COMPLETED PAGE DURING TEST!")

    @classmethod
    def tearDown(cls):
        cls.driver.quit()

    def test_login(cls):
        cls.driver.get("http://127.0.0.1:5000/login")
        username_input = cls.driver.find_element(By.ID, "email")
        password_input = cls.driver.find_element(By.ID, "password")
        submit_button = cls.driver.find_element(By.ID, "doSubmit")

        username_input.send_keys(randomEmail)
        password_input.send_keys(randomPassword)
        submit_button.click()

        expected_redirect_url = "http://127.0.0.1:5000/signs"
        cls.assertIn(expected_redirect_url, cls.driver.current_url)

    def test_new_request(cls):
        sp.login(randomEmail,randomPassword) # Login to account
        cls.driver.get("http://127.0.0.1:5000/newrequest")
        title = cls.driver.find_element(By.ID, "title")
        content = cls.driver.find_element(By.ID, "content")
        rewards = cls.driver.find_element(By.ID, "rewards")
        timelimit = cls.driver.find_element(By.ID, "timelimit")
        submit_button = driver.find_element(By.ID, "doSubmit")

        title.send_keys("Selenium Test")
        content.send_keys("Selenium Test")
        rewards.send_keys("1")
        timelimit.send_keys("1")
        submit_button.click()

        cls.assertIn("/requests",cls.driver.current_url)

    # def test_acceptRequest(cls):
    #     sp.login(randomEmail,randomPassword) # Login to account
    #     cls.driver.get("http://127.0.0.1:5000/newrequest")


if __name__ == "__main__":
    unittest.main(verbosity=2)
