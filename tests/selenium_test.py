from selenium import webdriver
import unittest
from app import create_app,db
import apps.randomprofile as rp
from models.sqlmodels import UserInfo,Community,Thread,Requests,Shop,Transaction,Todo,Chats,Signs,Faq,FaqChatTransaction
from sqlalchemy import update,delete,and_,or_

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.add_test_data()

        # self.server_thread = multiprocessing.Process(target=self.app.run)
        # self.server_thread.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        # self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def add_test_data(self):
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

    def test_login(self):
        self.driver.get("http://127.0.0.1:5000/login")
        username_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        submit_button = self.driver.find_element(By.ID, "doSubmit")

        username_input.send_keys("unittest@unittest.com")
        password_input.send_keys("1234")
        submit_button.click()

        expected_redirect_url = "http://127.0.0.1:5000/signs"
        self.assertIn(expected_redirect_url, self.driver.current_url)

    def test_new_request(self):
        self.driver.get("http://127.0.0.1:5000/newrequest")
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

        self.assertIn("/requests",self.driver.current_url)



if __name__ == "__main__":
    unittest.main(verbosity=2)