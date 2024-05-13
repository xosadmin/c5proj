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






    

    def test_new_thread(self):
        self.driver.get(webAddr + "newthread")
        title = self.driver.find_element(By.ID, "title")
        content = self.driver.find_element(By.ID, "content")
        submit_button = self.driver.find_element(By.ID, "doSubmit")

        title.send_keys("Selenium Thread Test")
        content.send_keys("Content for Selenium Test")
        submit_button.click()
        expected_text = self.driver.find_element(By.XPATH, "//script[contains(text(), 'New thread recorded.')]")
        self.assertTrue(expected_text)
        
    
    
    def test_new_chat(self):
        self.driver.get(webAddr + "newchat")
        dstuser = self.driver.find_element(By.ID, "dstUser")
        content = self.driver.find_element(By.ID, "content")
        submit_button = self.driver.find_element(By.ID, "doSubmit")
        dstuser.send_keys("666")
        content.send_keys("Content for Selenium Test")
        submit_button.click()
        expected_text = self.driver.find_element(By.XPATH, "//script[contains(text(), 'New Ticket recorede')]")
        self.assertTrue(expected_text)
        
        
        

    
    def test_new_helpsession(self):
        self.driver.get(webAddr + "help")
        content = self.driver.find_element(By.ID, "content")
        submit_button = self.driver.find_element(By.ID, "doSubmit")
        content.send_keys("Can you help me?")
        submit_button.click()
        self.assertIn("/help", self.driver.current_url)
    
    
    
    def test_new_todo(self):
        reqid = "123456789"
        self.driver.get(webAddr + "acceptrequests" + reqid)
        accept_button = self.driver.find_element(By.Class, "btn btn-success")
        accept_button.click()
        self.assertIn("/todo", self.driver.current_url)


    def test_request_answer(self):
        reqid = "123456789"
        self.driver.get(webAddr + "/todolist")
        answer_button= self.driver.find_element(By.XPATH, f"//a[contains(@href, 'answerrequest/{reqid}') and contains(text(), 'Answer')]")
        answer_button.click()
        answer_content = self.driver.find_element(By.ID, "content")
        answer_content.send_keys("here is the reply")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, ".btn btn-primar")
        submit_button.click()
        expected_text = self.driver.find_element(By.XPATH, "//script[contains(text(), 'Thank you! You have completed the request.')]")
        self.assertTrue(expected_text)
    

       
    

    def test_thread_reply(self):
        threadID = "12345678"
        self.driver.get(webAddr + "/thread/" + threadID)
        submit_btn = self.driver.find_element(By.ID, "doSubmit")
        content = self.driver.find_element(By.ID,"content")
        content.send_keys("this is a reply")
        submit_btn.click()
        expected_redirect_url = webAddr + "/thread/" + threadID
        self.assertIn(expected_redirect_url, self.driver.current_url)

    
    def test_chatreply(self):
        chatID= "123"
        self.driver.get(webAddr + "/chat/" + chatID)
        submit_btn = self.driver.find_element(By.ID, "doSubmit")
        content = self.driver.find_element(By.ID,"content")
        content.send_keys("this is a reply")
        submit_btn.click()
        expected_redirect_url = webAddr + "/chat/" + chatID
        self.assertIn(expected_redirect_url, self.driver.current_url)
        
        
    def delete_request(self):
        requestID = "1234567890"
        userID = 123456789
        self.driver.get(webAddr + "/requests")
        delete_link = self.driver.find_element(By.XPATH, f"//a[@href='/deleterequest/{userID}/{requestID}']")
        delete_link.click()
        confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Request Deleted Successfully. Your reward has been refunded.')]")
        self.assertTrue(confirmation_message)
    

    def delete_thread(self):
        threadID = "12345678"
        self.driver.get(webAddr + "/community")
        delete_link = self.driver.find_element(By.XPATH, f"//a[@href='/deletethread/{threadID}']")
        delete_link.click()
        confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Your thread has been deleted.')]")
        self.assertTrue(confirmation_message)
        


    def delete_chat(self):
        chatID = "123"
        self.driver.get(webAddr + "/chat")
        delete_link = self.driver.find_element(By.XPATH, f"//a[@href='/deletechat/{chatID}']")
        delete_link.click()
        confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Your chat has been deleted.')]")
        self.assertTrue(confirmation_message)

    
    def test_shop(self):
        itemID = "123"
        self.driver.get(webAddr + "/shop")
        buy_button = self.driver.find_element(By.XPATH, f"//a[@href='/confirmpayment/{itemID}']")
        buy_button.click()
        confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Purchase successful')]")
        self.assertTrue(confirmation_message)
    

    def test_logout(self):
        self.driver.get(webAddr + "/profile")  
        logout_button = self.driver.find_element(By.XPATH, f"//a[@href='/logout']")  
        logout_button.click()
        expected_redirect_url = webAddr + "/logout"
        self.assertIn(expected_redirect_url, self.driver.current_url)

    
    
    def test_changeemail(self):
        self.driver.get(webAddr + "/modifycenter")
        self.driver.find_element(By.ID, "chooseChangeEmail").click()
        self.driver.find_element(By.ID, "newEmail").send_keys("newemail@example.com")
        self.driver.find_element(By.ID, "repeatNewEmail").send_keys("newemail@example.com")
        self.driver.find_element(By.ID, "submitInfo").click()
        confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Email updated successfully')]")
        self.assertTrue(confirmation_message)

    
    
    def test_changepassword(self):
        self.driver.get(webAddr + "/modifycenter")
        self.driver.find_element(By.ID, "chooseChangePassword").click()
        self.driver.find_element(By.ID, "newpassword").send_keys("newpassword123")
        self.driver.find_element(By.ID, "repeatnewpassword").send_keys("newpassword123")
        self.driver.find_element(By.ID, "submitInfo").click()
        confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Information password has been updated.')]")
        self.assertTrue(confirmation_message)

    
    
    def test_changepincode(self):
        self.driver.get(webAddr + "/modifycenter")
        self.driver.find_element(By.ID, "chooseChangePin").click()
        self.driver.find_element(By.ID, "oldpin").send_keys("1234")
        self.driver.find_element(By.ID, "newpin").send_keys("5678")
        self.driver.find_element(By.ID, "repeatnewpin").send_keys("5678")
        self.driver.find_element(By.ID, "submitInfo").click()
        confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Information pin has been updated.')]")
        self.assertTrue(confirmation_message)

    
    
    def test_changeregion(self):
        self.driver.get(webAddr + "/modifycenter")
        self.driver.find_element(By.ID, "chooseChangeCountry").click()
        self.driver.find_element(By.ID, "country").clear()
        self.driver.find_element(By.ID, "country").send_keys("Asia")
        self.driver.find_element(By.ID, "submitInfo").click()
        confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Information country has been updated.')]")
        self.assertTrue(confirmation_message)

    

    
    def test_setavatar(self):
        self.driver.get(webAddr + "/profile")  
        set_avatar_link = self.driver.find_element(By.XPATH, "//a[@href='/setavatar/123']")  
        set_avatar_link.click() 
        confirmation_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Avatar updated')]")  
        self.assertTrue(confirmation_message)  



    


            

if __name__ == "__main__":
    unittest.main(verbosity=2)






    




