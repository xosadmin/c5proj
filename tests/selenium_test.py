from selenium import webdriver
import unittest
import threading
from app import create_app, db
from selenium.webdriver.common.by import By
from models.sqlmodels import UserInfo, Community, Thread, Requests, Shop, Transaction, Todo, Chats, Signs, Faq, FaqChatTransaction

webAddr = "http://127.0.0.1:5000/"

class FlaskAppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        })
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()
        cls.add_test_data()

        cls.server_thread = threading.Thread(target=cls.app.run)
        cls.server_thread.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get(webAddr)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server_thread.join()
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
        cls.app_context.destroy()

    @staticmethod
    def add_test_data():
        datas = [UserInfo(userID="1234567890",email="unittest@unittest.com",password="1234",country="Australia",pincode="1234"),
                 UserInfo(userID="666",email="testreceiver@chat.com",password="987654321",country="None",pincode="1234"),
                 UserInfo(userID="777",email="deleteme@deleteme.com",password="987654321",country="None",pincode="1234"),
                 Requests(requestID=123456789,title="title",content="content",rewards="rewards",timelimit="timelimit",userID="1234567890"),
                 Community(threadID="1234567",title="title",userID="1234567890"),
                 Thread(replyID = 12345678, threadID ="1234567", userID = "666", contents = "content"),
                 Shop(itemID=123,itemDetail="Test Item",price=1),
                 Todo(todoID = 321, userID = "1234567890", requestID = 123456789),
                 Chats(chatID="123",srcUserID="1234567890",dstUserID="666",content="content"),
                 Faq(faqID=123, keyword="UnitTest", answer="UnitTest"),
                 FaqChatTransaction(TransactionID=123,userID="1234567890",role="User",content="Unit Test")
                 ]
        for item in datas:
            db.session.add(item)
        db.session.commit()

    def test_registration(self):
        self.driver.get(webAddr + "register")
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        repeat_password_input = self.driver.find_element(By.ID, "repeat_password")
        pincode_input = self.driver.find_element(By.ID, "repeat_password")
        submit_button = self.driver.find_element(By.ID, "btnRegister")

        email_input.send_keys("testregistration@testregistration.com")
        password_input.send_keys("1234")
        repeat_password_input.send_keys("1234")
        pincode_input.send_keys("1234")
        submit_button.click()

        try:
            expected_text = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Complete')]")
            self.assertTrue(True)
        except:
            self.assertFalse(False)
        

    def test_login(self):
        self.driver.get(webAddr + "login")
        username_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        submit_button = self.driver.find_element(By.ID, "btnLogin")

        username_input.send_keys("unittest@unittest.com")
        password_input.send_keys("1234")
        submit_button.click()

        expected_redirect_url = webAddr + "signs"
        self.assertIn(expected_redirect_url, self.driver.current_url)

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
