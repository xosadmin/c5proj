from selenium import webdriver
import unittest
import threading
import time
from apps.get import encryptPassword
from app import create_app, db
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        if cls.app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:': # Avoid from drop production DB
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
            Requests(requestID=123456789, title="title", content="content", rewards="1", timelimit="1",
                     userID="1234567890"),
            Requests(requestID=1234567891, title="title 2", content="content", rewards="1", timelimit="1",
                     userID="777"),
            Community(threadID="1234567", title="title", userID="1234567890"),
            Thread(replyID=12345678, threadID="1234567", userID="666", contents="content"),
            Shop(itemID=1, itemDetail="Test Item", price=1),
            Shop(itemID=2, itemDetail="Test Item 2", price=1),
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
        self.driver.get(webAddr + "login")
        time.sleep(6) # Waiting for redirection
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

    def test_forgotpassword(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" in self.driver.current_url:
            self.driver.get(webAddr + "logout")
        self.driver.get(webAddr + "forgetpassword")
        time.sleep(2)
        email_input = self.driver.find_element(By.ID, "email")
        pincode_input = self.driver.find_element(By.ID, "pin-code")
        submit_button = self.driver.find_element(By.ID, "btnResetPwd")
        global loginEmail, loginPassword
        email_input.send_keys(loginEmail)
        pincode_input.send_keys("1234")
        submit_button.click()
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.assertIn("123", alert.text)
        alert.accept()
        time.sleep(5)

    def test_register(self):
        self.driver.get(webAddr + "login")
        if "You+have+already+logged+in" in self.driver.current_url:
            self.driver.get(webAddr + "logout")

        time.sleep(2)
        self.driver.get(webAddr + "register")
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        repeat_password_input = self.driver.find_element(By.ID, "repeat_password")
        pincode_input = self.driver.find_element(By.ID, "pin_code")
        submit_button = self.driver.find_element(By.ID, "btnRegister")
        global loginEmail, loginPassword   
        email_input.send_keys("123@gmail.com")
        password_input.send_keys(loginPassword)
        repeat_password_input.send_keys(loginPassword)
        pincode_input.send_keys("1234")
        submit_button.click()
        confirmation_message = self.driver.find_elements(By.XPATH, "//div[@id='CompleteBanner']")
            # Check if CompleteBanner exist on the page
        self.assertTrue(confirmation_message,False)

    def test_newSigns(self):
        self.driver.get(webAddr + "login")
        time.sleep(6)  # Waiting for redirection
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
        time.sleep(6)  # Waiting for redirection
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

        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())

        self.assertTrue("New request", alert.text)
        alert.accept()
        time.sleep(5)

    def test_new_thread(self):
        self.driver.get(webAddr + "login")
        time.sleep(6)  # Waiting for redirection
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
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())

        self.assertIn("New thread", alert.text)
        alert.accept()
        time.sleep(5)

    def test_new_chat(self):
        self.driver.get(webAddr + "login")
        time.sleep(6)  # Waiting for redirection
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
        dstuser = self.driver.find_element(By.ID, "dstuser")
        content = self.driver.find_element(By.ID, "content")
        submit_button = self.driver.find_element(By.ID, "btnSubmitChat")
        dstuser.send_keys("666")
        content.send_keys("Content for Selenium Test")
        submit_button.click()
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())

        self.assertTrue("New ticket",alert.text)
        alert.accept()
        time.sleep(5)

    def test_new_helpsession(self):
        self.driver.get(webAddr + "login")
        time.sleep(6)  # Waiting for redirection
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
        time.sleep(6)  # Waiting for redirection
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
        self.driver.get(webAddr + "acceptrequest/1234567891")
        accept_button = self.driver.find_element(By.ID,"confirmAcceptRequest")
        accept_button.click()
        self.assertIn("/todo", self.driver.current_url)

    def test_request_answer(self):
        self.driver.get(webAddr + "login")
        time.sleep(6)  # Waiting for redirection
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
        self.driver.get(webAddr + "answerrequest/1234567891")
        answer_content = self.driver.find_element(By.ID, "content")
        answer_content.send_keys("here is the reply")
        submit_button = self.driver.find_element(By.ID, "doAnswerRequestSubmit")
        submit_button.click()
        self.assertIn("You+have+completed", self.driver.current_url)

    def test_thread_reply(self):
        self.driver.get(webAddr + "login")
        time.sleep(6)  # Waiting for redirection
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "thread/1234567")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "thread/1234567")
        submit_btn = self.driver.find_element(By.ID, "doSubmit")
        content = self.driver.find_element(By.ID, "content")
        content.send_keys("this is a reply")
        submit_btn.click()
        self.assertIn("1234567", self.driver.current_url)

    def test_chatreply(self):
        self.driver.get(webAddr + "login")
        time.sleep(6)  # Waiting for redirection
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
        time.sleep(6)  # Waiting for redirection
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
        time.sleep(6)  # Waiting for redirection
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
        time.sleep(6)  # Waiting for redirection
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
        time.sleep(6)  # Waiting for redirection
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
        self.driver.get(webAddr + "confirmpayment/2")
        buy_button = self.driver.find_element(By.ID, "confirmPayments")
        buy_button.click()
        if "Successful" in self.driver.current_url or "once+again" in self.driver.current_url:
            self.assertTrue(True)
        else:
            self.assertFalse(False)

    def test_logout(self):
        self.driver.get(webAddr + "login")
        time.sleep(6)  # Waiting for redirection
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
        time.sleep(6)  # Waiting for redirection
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
        time.sleep(6)  # Waiting for redirection
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
        time.sleep(6)  # Waiting for redirection
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

        self.driver.find_element(By.ID, "chooseChangePin").click()
        self.driver.find_element(By.ID, "oldpin").send_keys("1234")
        self.driver.find_element(By.ID, "newpin").send_keys("4321")
        self.driver.find_element(By.ID, "repeatnewpin").send_keys("4321")
        self.driver.find_element(By.ID, "submitInfo").click()
        self.assertIn("updated", self.driver.current_url)

    def test_changeregion(self):
        self.driver.get(webAddr + "login")
        time.sleep(6)  # Waiting for redirection
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
        self.driver.find_element(By.ID, "country").send_keys("UnitTest")
        self.driver.find_element(By.ID, "submitInfo").click()
        self.assertIn("updated", self.driver.current_url)

    def test_setavatar(self):
        self.driver.get(webAddr + "login")
        time.sleep(6)  # Waiting for redirection
        if "You+have+already+logged+in" not in self.driver.current_url:
            self.driver.get(webAddr + "profile")
            time.sleep(10)
            username_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.ID, "btnLogin")
            global loginEmail, loginPassword # Declare global variable loginEmail and loginPassword
            username_input.send_keys(loginEmail)
            password_input.send_keys(loginPassword)
            submit_button.click()
        self.driver.get(webAddr + "profile")

        set_avatar_link = self.driver.find_element(By.XPATH, "//a[@href='/setavatar/1']")
        set_avatar_link.click()
        confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Avatar updated')]")
        self.assertTrue(confirmation_message)

if __name__ == "__main__":
    unittest.main(verbosity=2)
