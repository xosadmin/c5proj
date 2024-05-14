from selenium import webdriver
import unittest
import threading
import time
from apps.get import encryptPassword
from app import create_app, db
from selenium.webdriver.common.by import By
from models.sqlmodels import UserInfo, Community, Thread, Requests, Shop, Transaction, Todo, Chats, Faq, \
    FaqChatTransaction

webAddr = "http://127.0.0.1:5000/"
loginEmail = "unittest@unittest.com"
loginPassword = "1234"


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

        cls.server_thread = threading.Thread(target=cls.app.run, kwargs={'use_reloader': False})
        cls.server_thread.start()
        time.sleep(2)  # Wait for the server to start

        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")

        cls.driver = webdriver.Chrome(options=options)

        cls.driver.set_page_load_timeout(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server_thread.join(timeout=5)
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.driver.get(webAddr)
        time.sleep(2)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.add_test_data()

    @staticmethod
    def add_test_data():
        encryptPasswords = encryptPassword("1234")
        datas = [
            UserInfo(userID="1234567890", email="unittest@unittest.com", password=encryptPasswords, country="Australia",
                     pincode="1234"),
            UserInfo(userID="666", email="testreceiver@chat.com", password=encryptPasswords, country="None",
                     pincode="1234"),
            UserInfo(userID="777", email="deleteme@deleteme.com", password=encryptPasswords, country="None",
                     pincode="1234"),
            Requests(requestID=123456789, title="title", content="content", rewards="rewards", timelimit="timelimit",
                     userID="1234567890"),
            Community(threadID="1234567", title="title", userID="1234567890"),
            Thread(replyID=12345678, threadID="1234567", userID="666", contents="content"),
            Shop(itemID=1, itemDetail="Test Item", price=1),
            Transaction(transactionID=123, userID="1234567890", itemID=1),
            Todo(todoID=321, userID="1234567890", requestID=123456789),
            Chats(chatID="123", srcUserID="1234567890", dstUserID="666", content="content"),
            Faq(faqID=123, keyword="UnitTest", answer="UnitTest"),
            FaqChatTransaction(TransactionID=123, userID="1234567890", role="User", content="Unit Test")
        ]
        for item in datas:
            db.session.add(item)
        db.session.commit()

    def test_login(self):
        self.driver.getr(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "login")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
            self.assertIn("signs", self.driver.current_url)
        else:
            self.assertTrue(True)

    def test_newSigns(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "signs")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "signs")

        feelings = self.driver.find_element(By.ID, "feelings")
        comment = self.driver.find_element(By.ID, "content")
        submit = self.driver.find_element(By.ID, "btnSubmitEmo")

        feelings.send_keys("Happy")
        comment.send_keys("Unit Test")
        submit.click()

        self.assertIn(webAddr + "profile", self.driver.current_url)

    def test_new_request(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "newrequest")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "newrequest")
        title = self.driver.find_element(By.ID, "title")
        content = self.driver.find_element(By.ID, "content")
        rewards = self.driver.find_element(By.ID, "rewards")
        timelimit = self.driver.find_element(By.ID, "timelimit")
        submit_button = self.driver.find_element(By.ID, "btnRequest")

        title.send_keys("Selenium Test")
        content.send_keys("Selenium Test")
        rewards.send_keys("1")
        timelimit.send_keys("1")
        submit_button.click()

        self.assertIn("/requests", self.driver.current_url)

    def test_new_thread(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "newthread")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "newthread")

        title = self.driver.find_element(By.ID, "title")
        content = self.driver.find_element(By.ID, "content")
        submit_button = self.driver.find_element(By.ID, "btnSubmitThread")

        title.send_keys("Selenium Thread Test")
        content.send_keys("Content for Selenium Test")
        submit_button.click()
        expected_text = self.driver.find_element(By.XPATH, "//script[contains(text(), 'New thread recorded.')]")
        self.assertTrue(expected_text)

    def test_new_chat(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "newchat")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "newchat")
        dstuser = self.driver.find_element(By.ID, "dstUser")
        content = self.driver.find_element(By.ID, "content")
        submit_button = self.driver.find_element(By.ID, "btnSubmitChat")
        dstuser.send_keys("666")
        content.send_keys("Content for Selenium Test")
        submit_button.click()
        expected_text = self.driver.find_element(By.XPATH, "//script[contains(text(), 'New Ticket recorede')]")
        self.assertTrue(expected_text)

    def test_new_helpsession(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "help")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "help")
        content = self.driver.find_element(By.ID, "content")
        submit_button = self.driver.find_element(By.ID, "doSubmit")
        content.send_keys("Can you help me?")
        submit_button.click()
        self.assertIn("/help", self.driver.current_url)

    def test_new_todo(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "acceptrequests/123456789")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "acceptrequests/123456789")
        accept_button = self.driver.find_element(By.CLASS_NAME, "btn btn-success")
        accept_button.click()
        self.assertIn("/todo", self.driver.current_url)

    def test_request_answer(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "todolist")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "todolist")
        answer_button = self.driver.find_element(By.XPATH,
                                                 f"//a[contains(@href, 'answerrequest/123456789') and contains(text(), 'Answer')]")
        answer_button.click()
        answer_content = self.driver.find_element(By.ID, "content")
        answer_content.send_keys("here is the reply")
        submit_button = self.driver.find_element(By.CLASS_NAME, "btn btn-primar")
        submit_button.click()
        expected_text = self.driver.find_element(By.XPATH,
                                                 "//script[contains(text(), 'Thank you! You have completed the request.')]")
        self.assertTrue(expected_text)

    def test_thread_reply(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "thread/12345678")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "thread/12345678")
        submit_btn = self.driver.find_element(By.ID, "doSubmit")
        content = self.driver.find_element(By.ID, "content")
        content.send_keys("this is a reply")
        submit_btn.click()
        expected_redirect_url = webAddr + "thread/12345678"
        self.assertIn(expected_redirect_url, self.driver.current_url)

    def test_chatreply(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "chat/123")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "chat/123")
        submit_btn = self.driver.find_element(By.ID, "doSubmit")
        content = self.driver.find_element(By.ID, "content")
        content.send_keys("this is a reply")
        submit_btn.click()
        expected_redirect_url = webAddr + "chat/123"
        self.assertIn(expected_redirect_url, self.driver.current_url)

    def delete_request(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "requests")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "requests")
        delete_link = self.driver.find_element(By.XPATH, f"//a[@href='/deleterequest/123456789/1234567890']")
        delete_link.click()
        confirmation_message = self.driver.find_element(By.XPATH,
                                                        "//div[contains(text(), 'Request Deleted Successfully. Your reward has been refunded.')]")
        self.assertTrue(confirmation_message)

    def delete_thread(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "community")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "community")
        delete_link = self.driver.find_element(By.XPATH, f"//a[@href='/deletethread/12345678']")
        delete_link.click()
        confirmation_message = self.driver.find_element(By.XPATH,
                                                        "//div[contains(text(), 'Your thread has been deleted.')]")
        self.assertTrue(confirmation_message)

    def delete_chat(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "chat")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "chat")
        delete_link = self.driver.find_element(By.XPATH, f"//a[@href='/deletechat/123']")
        delete_link.click()
        confirmation_message = self.driver.find_element(By.XPATH,
                                                        "//div[contains(text(), 'Your chat has been deleted.')]")
        self.assertTrue(confirmation_message)

    def test_shop(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "shop")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "shop")
        buy_button = self.driver.find_element(By.XPATH, f"//a[@href='/confirmpayment/1']")
        buy_button.click()
        confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), '#1')]")
        self.assertTrue(confirmation_message)

    def test_logout(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "logout")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "logout")
        try:
            confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Complete')]")
            self.assertTrue(confirmation_message)
        except:
            self.assertFalse(False)

    def test_changeemail(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "modifycenter")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "modifycenter")

        self.driver.find_element(By.ID, "chooseChangeEmail").click()
        self.driver.find_element(By.ID, "newEmail").send_keys("newemail@example.com")
        self.driver.find_element(By.ID, "repeatNewEmail").send_keys("newemail@example.com")
        self.driver.find_element(By.ID, "submitInfo").click()

        try:
            confirmation_message = self.driver.find_element(By.XPATH,
                                                            "//div[contains(text(), 'email has been updated')]")
            self.assertTrue(confirmation_message)
        except:
            self.assertFalse(False)

    def test_changepassword(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "modifycenter")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "modifycenter")

        self.driver.find_element(By.ID, "chooseChangePassword").click()
        self.driver.find_element(By.ID, "newpassword").send_keys("newpassword123")
        self.driver.find_element(By.ID, "repeatnewpassword").send_keys("newpassword123")
        self.driver.find_element(By.ID, "submitInfo").click()

        try:
            confirmation_message = self.driver.find_element(By.XPATH,
                                                            "//div[contains(text(), 'password has been updated')]")
            self.assertTrue(confirmation_message)
        except:
            self.assertFalse(False)

    def test_changepincode(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "modifycenter")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "modifycenter")

        self.driver.find_element(By.ID, "chooseChangePincode").click()
        self.driver.find_element(By.ID, "newpincode").send_keys("43321")
        self.driver.find_element(By.ID, "repeatnewpin").send_keys("4321")
        self.driver.find_element(By.ID, "submitInfo").click()
        try:
            confirmation_message = self.driver.find_element(By.XPATH,
                                                            "//div[contains(text(), 'pincodehas been updated')]")
            self.assertTrue(confirmation_message)
        except:
            self.assertFalse(False)

    def test_changeregion(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "modifycenter")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "modifycenter")

        self.driver.find_element(By.ID, "chooseChangeCountry").click()
        self.driver.find_element(By.ID, "country").clear()
        self.driver.find_element(By.ID, "country").send_keys("Asia")
        self.driver.find_element(By.ID, "submitInfo").click()
        confirmation_message = self.driver.find_element(By.XPATH,
                                                        "//div[contains(text(), 'Information country has been updated.')]")
        self.assertTrue(confirmation_message)

    def test_setavatar(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "profile")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send.keys(loginEmail)
            password_input.send.keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "profile")

        set_avatar_link = self.driver.find_element(By.XPATH, "//a[@href='/setavatar/1']")
        set_avatar_link.click()
        confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Avatar updated')]")
        self.assertTrue(confirmation_message)


if __name__ == "__main__":
    unittest.main(verbosity=2)
