import unittest
from app import create_app,db
from apps.randomprofile import uuidGen
from models.sqlmodels import UserInfo,Community,Thread,Requests,Shop,Transaction,Todo,Chats,Signs,Faq,FaqChatTransaction
from sqlalchemy import update,delete,and_,or_

threadUUID = uuidGen()

class testDB(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.add_test_data()

    def tearDown(self):
        if self.app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:':  # Avoid from drop production DB
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

# Unit Test Setup

    def test_regist_newuser(self):
        user = UserInfo(userID="666777",email="unittest2@unittest.com",password="1234",country="Australia",pincode="1234")
        db.session.add(user)
        db.session.commit()
        self.assertEqual(UserInfo.query.filter(UserInfo.userID == "666777").first().email, 'unittest2@unittest.com')

    def test_changePassword(self):
        db.session.execute(update(UserInfo).filter(UserInfo.userID == "1234567890").values(password="12345678"))
        db.session.commit()
        self.assertEqual(UserInfo.query.first().password, "12345678")

    def test_changeCountry(self):
        db.session.execute(update(UserInfo).filter(UserInfo.userID == "1234567890").values(country="New Zealand"))
        db.session.commit()
        self.assertEqual(UserInfo.query.first().country, "New Zealand")

    def test_removeUser(self):
        db.session.delete(UserInfo.query.filter(UserInfo.userID == "777").first())
        checkIfDelete = UserInfo.query.filter(UserInfo.userID == "777").first()
        self.assertIsNone(checkIfDelete)

# UserInfo Test
    def test_addRequests(self):
        request = Requests(requestID=12345678912,title="title",content="content",rewards="rewards",timelimit="timelimit",userID="1234567890")
        db.session.add(request)
        db.session.commit()
        self.assertEqual(Requests.query.filter(Requests.requestID == 12345678912).first().title, "title")

    def test_answerRequest(self):
        request = update(Requests).filter(Requests.requestID == 123456789).values(status="Completed",answer="content")
        db.session.execute(request)
        db.session.commit()
        self.assertEqual(Requests.query.filter(Requests.requestID == 123456789).first().answer, "content")
    
    def test_deleteRequest(self):
        request = delete(Requests).filter(Requests.requestID == 123456789)
        db.session.execute(request)
        db.session.commit()
        checkIfDelete = Requests.query.filter(Requests.requestID == 123456789).first()
        self.assertIsNone(checkIfDelete)

# Request Test
    def test_addShopItem(self):
        addShop = Shop(itemID=1234,itemDetail="Test Item 2",price=1)
        db.session.add(addShop)
        db.session.commit()
        self.assertEqual(Shop.query.filter(Shop.itemID == 1234).first().price, 1)

    def test_purchaseItem(self):
        purchaseRequest = Transaction(userID="1234567890",itemID="123")
        db.session.add(purchaseRequest)
        db.session.commit()
        self.assertEqual(Transaction.query.filter(Transaction.userID == "1234567890").first().itemID, 123)

# Shop item and purchase transaction

    def test_addNewSigns(self):
        newSigns = Signs(signID="123",userID="1234567890",time="1/1/1970",emotion="Happy",comments="comments",rewards=1)
        db.session.add(newSigns)
        db.session.commit()
        self.assertEqual(Signs.query.filter(Signs.signID == "123").first().userID, "1234567890")

# Signs Unit Test

    def test_sendNewChat(self):
        processes = Chats(chatID="1234",srcUserID="1234567890",dstUserID="666",content="content")
        db.session.add(processes)
        db.session.commit()
        self.assertEqual(Chats.query.filter(Chats.chatID == "1234").first().content, "content")
    
    def test_doNewReply(self):
        newReply = Chats(chatID="123",srcUserID="666",dstUserID="1234567890",content="Received")
        db.session.add(newReply)
        db.session.commit()
        self.assertEqual(Chats.query.filter(and_(Chats.chatID == "123",Chats.srcUserID == "666")).first().content, "Received")

    def test_removeChat(self):
        chat_to_delete = Chats.query.filter(Chats.chatID == "123").first()
        db.session.delete(chat_to_delete)
        db.session.commit()
        checkIfDelete = Chats.query.filter(Chats.chatID == "123").first()
        self.assertIsNone(checkIfDelete)

# Chatroom Test

    def test_addNewThread(self):
        inserts = [Community(threadID=threadUUID,title="New Thread Test",userID="666777"),
                    Thread(threadID=threadUUID,userID="666777",contents="content")]
        for item in inserts:
            db.session.add(item)
        db.session.commit()
        checks = [Community.query.filter(Community.threadID == threadUUID).first().userID,
                  Thread.query.filter(Thread.threadID == threadUUID).first().userID]
        for item in checks:
            if item != "666777":
                self.assertFalse(False)
        self.assertTrue(True)
    
    def test_doNewReply(self):
        insert = Thread(threadID=threadUUID,userID="1234567890",contents="reply content")
        db.session.add(insert)
        db.session.commit()
        self.assertEqual(Thread.query.filter(Thread.threadID == threadUUID).first().contents, "reply content")
    
    def test_removeThread(self):
        deleteCommands = [delete(Community).filter(Community.threadID == threadUUID),
                          delete(Thread).filter(Thread.threadID == threadUUID)]
        for item in deleteCommands:
            db.session.execute(item)
        db.session.commit()
        checkScripts = [Community.query.filter(Community.threadID == threadUUID).first(),
                        Thread.query.filter(Thread.threadID == threadUUID).first()]
        for item in checkScripts:
            if item is not None:
                self.assertFalse(False)
        self.assertTrue(True)

# Tests Community & Threads
    
    def test_addtodo(self):
        new_todo = Todo(userID="1234567890", requestID=47897484)
        db.session.add(new_todo)
        db.session.commit()
        added_todo = Todo.query.filter(Todo.requestID == 47897484).first().userID
        self.assertEqual(added_todo,"1234567890")

    def test_answertodo(self):
        todo_to_update = update(Todo).where(Todo.todoID == 321).values(status="Completed")
        db.session.execute(todo_to_update)
        db.session.commit()
        updated_todo = Todo.query.filter(Todo.todoID == 321).first().status
        self.assertEqual(updated_todo, "Completed")

# Todo Tests

    def test_chatbot(self):
        existing_faq = Faq.query.filter(Faq.faqID == 123).first().answer
        self.assertEqual(existing_faq, "UnitTest")

    def test_faqChat(self):
        getChat = FaqChatTransaction.query.filter(FaqChatTransaction.TransactionID == 123).first().content
        self.assertEqual(getChat, "Unit Test")

    def test_answerChat(self):
        getAsk = FaqChatTransaction.query.filter(FaqChatTransaction.TransactionID == 123).first()
        if getAsk:
            getAskSplit = getAsk.content.split(" ")
            for item in getAskSplit:
                getReply = Faq.query.filter(or_(Faq.keyword.ilike(f'%{item}%'), Faq.answer.ilike(f'%{item}%'))).first()
            newReply = FaqChatTransaction(TransactionID=124, userID="1234567890",role="Bot",content=getReply.answer)
            db.session.add(newReply)
            db.session.commit()
            self.assertEqual(FaqChatTransaction.query.filter(FaqChatTransaction.TransactionID == 124).first().content, "UnitTest")
        else:
            self.assertFalse(False)
    
    def test_deleteChat(self):
        query = FaqChatTransaction.query.filter(FaqChatTransaction.userID == "1234567890").all()
        for item in query:
            db.session.delete(item)
        db.session.commit()
        self.assertEqual(FaqChatTransaction.query.filter(FaqChatTransaction.userID == "1234567890").count(), 0)

# Chatbot & FAQ Tests

if __name__ == '__main__':
    unittest.main(verbosity=2)
