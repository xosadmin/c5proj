from selenium import webdriver
import unittest
import threading
import time
import tests.selenium_preparation as sp
from app import create_app, db
from selenium.webdriver.common.by import By
from models.sqlmodels import UserInfo, Community, Thread, Requests, Shop, Transaction, Todo, Chats, Signs, Faq, FaqChatTransaction
import tracemalloc
tracemalloc.start()

webAddr = "http://127.0.0.1:5000/"

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        sp.add_test_data()

        self.server_thread = threading.Thread(target=self.app.run)
        self.server_thread.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=options)
        self.driver.get(webAddr)

    def tearDown(self):
        self.driver.quit()
        self.server_thread.join()
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def test_login(self):
        self.driver.get(webAddr + "login")
        username_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        submit_button = self.driver.find_element(By.ID, "btnLogin")

        username_input.send_keys("unittest@unittest.com")
        password_input.send_keys("1234")
        submit_button.click()

        expected_redirect_url = webAddr + "signs"
        self.assertEqual(expected_redirect_url, self.driver.current_url)

    def test_newSigns(self):
        self.driver.get(webAddr + "signs")
        feelings = self.driver.find_element(By.ID, "feelings")
        comment = self.driver.find_element(By.ID, "content")
        submit = self.driver.find_element(By.ID, "submit")

        feelings.send_keys("Happy")
        comment.send_keys("Unit Test")
        submit.click()

        self.assertIn(webAddr + "profile",self.driver.current_url)

    def test_new_request(self):
        self.driver.get(webAddr + "newrequest")
        title = self.driver.find_element(By.ID, "title")
        content = self.driver.find_element(By.ID, "content")
        rewards = self.driver.find_element(By.ID, "rewards")
        timelimit = self.driver.find_element(By.ID, "timelimit")
        submit_button = self.driver.find_element(By.ID, "doSubmit")

        title.send_keys("Selenium Test")
        content.send_keys("Selenium Test")
        rewards.send_keys("1")
        timelimit.send_keys("1")
        submit_button.click()

        self.assertIn("/requests", self.driver.current_url)

if __name__ == "__main__":
    unittest.main(verbosity=2)
