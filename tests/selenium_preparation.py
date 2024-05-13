from selenium import webdriver
from app import create_app, db
from apps.get import encryptPassword
from selenium.webdriver.common.by import By
from models.sqlmodels import UserInfo, Community, Thread, Requests, Shop, Transaction, Todo, Chats, Signs, Faq, FaqChatTransaction

webAddr = "http://127.0.0.1:5000/"
encryptPasswords = encryptPassword("1234")
def add_test_data():
        datas = [UserInfo(userID="1234567890",email="unittest@unittest.com",password=encryptPasswords,country="Australia",pincode="1234"),
                 UserInfo(userID="666",email="testreceiver@chat.com",password=encryptPasswords,country="None",pincode="1234"),
                 UserInfo(userID="777",email="deleteme@deleteme.com",password=encryptPasswords,country="None",pincode="1234"),
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