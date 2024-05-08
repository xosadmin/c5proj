import unittest
from app import *
from models.sqlmodels import *

class testDB(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

# Unit Test Setup

    def test_regist_newuser(self):
        user = UserInfo(userID="1234567890",email="unittest@unittest.com",password="1234",country="Australia",pincode="1234")
        db.session.add(user)
        db.session.commit()
        self.assertEqual(UserInfo.query.filter(UserInfo.userID == "1234567890").first().email, 'unittest@unittest.com')

    def test_changePassword(self):
        db.session.execute(update(UserInfo).filter(UserInfo.userID == "1234567890").values(password="12345678"))
        db.session.commit()
        self.assertEqual(UserInfo.query.first().password, "12345678")

    def test_changeCountry(self):
        db.session.execute(update(UserInfo).filter(UserInfo.userID == "1234567890").values(country="New Zealand"))
        db.session.commit()
        self.assertEqual(UserInfo.query.first().country, "New Zealand")
    
    def test_removeUser(self):
        user = UserInfo(userID="666",email="deleteme@deleteme.com",password="987654321",country="None",pincode="1234") 
            # Create a new user for deletion
        db.session.add(user)
        db.session.execute(delete(UserInfo).filter(UserInfo.userID == "666"))
        checkIfDelete = UserInfo.query.filter(userID="666").first()
        self.assertIsNone(checkIfDelete)

# UserInfo Test

    def test_addRequets(self):
        request = Requests(requestID=123456789,title="title",content="content",rewards="rewards",timelimit="timelimit",userID="1234567890")
        db.session.add(request)
        db.session.commit()
        self.assertEqual(Requests.query.filter(Requests.userID == "1234567890").first().title, "title")

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
        addShop = Shop(id=123,itemDetail="Test Item",price=1)
        db.session.add(addShop)
        db.session.commit()
        self.assertEqual(Shop.query.filter(Shop.id == 123).first().price, 1)

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
        processes = [UserInfo(userID="666",email="testreceiver@chat.com",password="987654321",country="None",pincode="1234"),
                     Chats(chatID="123",srcUserID="1234567890",dstUserID="666",content="content")]
        for item in processes:
            db.session.add(item)
        db.session.commit()
        self.assertEqual(Chats.query.filter(Chats.chatID == "123").first().content, "content")
    
    def test_doNewReply(self):
        newReply = Chats(chatID="123",srcUserID="666",dstUserID="1234567890",content="Received")
        db.session.add(newReply)
        db.session.commit()
        self.assertEqual(Chats.query.filter(and_(Chats.chatID == "123",Chats.srcUserID == "666")).first().content, "Received")

    def test_removeChat(self):
        deletion = delete(Chats).filter(Chats.chatID == "123")
        db.session.add(deletion)
        db.session.commit()
        checkIfDelete = Chats.query.filter(Chats.chatID == "123").first()
        self.assertIsNone(checkIfDelete)

# Chatroom Test

if __name__ == '__main__':
    unittest.main(verbosity=2)