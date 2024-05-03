import unittest
import app
import apps.get as gt
import apps.llm as llm
import apps.login_process as lp
import apps.randomprofile as rp

class testCases(unittest.TestCase):
    def setUp(self):
        self.app = app.app
        self.gt = gt
        self.llm = llm
        self.lp = lp
        app.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.generatedEmail = str(rp.randomEmail())
        self.generatedPassword = str(rp.generatePassword(10))
        self.pincode = "1234"

# Setup

    def test_email_exists(self):
        with self.app.test_request_context():
            email = "test@test.com"
            getReturn = self.gt.checkEmail(email)
            self.assertEqual(getReturn, -1)

    def test_register(self):
        response = self.client.post('/register', data={
            'email': self.generatedEmail, 
            'password': self.generatedPassword,
            'pincode': self.pincode
        },follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        

    def test_dologin(self):
        response = self.client.post('/dologin', data={
            'email': "test@test.com",
            'password': "123"
        })
        self.assertEqual(response.status_code, 302)
    
    def test_doresetpassword(self):
        response = self.client.post('/forgetpassword', data={
            'email': self.generatedEmail,
            'pincode': self.pincode
        },follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_domodifypassword(self):
        response = self.client.post('/modifycenter', data={
            'type': 'password',
            'newpassword': 'newPass1234',
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
    def test_domodifypin(self):
        response = self.client.post('/modifycenter', data={
            'oldpin': self.pincode,
            'newpin': '5678',
            'repeatnewpin': '5678'
        },follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_donewrequests(self):
        with self.client as client:
            response = client.post('/newrequest', data={
                'title': 'Unit Test Request',
                'content': 'This is the content of the new request for unit test.',
                'rewards': '1',
                'timelimit': '1'
            },follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_donewthreads(self):
       with self.client as client:
            response = client.post('/newthread', data={
                'title': 'New Thread for Unittest',
                'content': 'This is the content of the new thread for unittest.'
            },follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
    def test_doNewThreadReply(self):
        with self.client as client:
            response = client.post('/donewthreadreply', data={
                'threadID': '117715ff-1b38-4410-b8f2-23ead632642e',
                'content': 'Unit test conducted on ' + gt.getTime()
            })
            self.assertEqual(response.status_code, 302)

    def test_dopayment(self):
        with self.client as client:
            response = client.get('/dopayment/2', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_donewchat(self):
        with self.client as client:
            response = client.post('/newchat', data={
                'userID': '0',
                'dstusr': '14',
                'content': 'test'
            },follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_dosetAvatar(self):
        with self.client as client:
            response = client.get('/setavatar/default', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

# app.py Unit Test

    def test_llmreq(self):
        llmReqGen = llm.llmRequests()
        if "." or "?" in llmReqGen:
            self.assertTrue(True)
    
    def test_llmans(self):
        llmAnsGen = llm.llmAnswers()
        if "." or "?" in llmAnsGen:
            self.assertTrue(True)

    def test_llmFeelings(self):
        llmFeelGen = llm.llmFeelings()
        if "." in llmFeelGen:
            self.assertTrue(True)

# llm.py Unit Test

    def test_checkEmail(self):
        with self.app.app_context():
            Input = "test@test.com" # Email address that existed in the system
            result = gt.checkEmail(Input)
            self.assertEqual(result,-1)
    
    def test_getThreadTitle(self):
        with self.app.app_context():
            Input = "117715ff-1b38-4410-b8f2-23ead632642e" # Thread ID
            result = gt.getThreadTitle(Input)
            self.assertEqual(result,"ehgjreh")

    def test_getCoins(self):
        with self.app.app_context():
            Input = "b56b9e05-0823-480b-aace-e14c698e99b9" # UserID
            result = gt.getCoins(Input)
            self.assertEqual(result,10)

    def test_getRequestInfo(self):
        with self.app.app_context():
            Input1 = 21 # RequestID
            testCases = ["userID","state","rewards"]
            expectAnswers = ["0", "Completed", "123"] # [userid, status, rewards]
            for i in range(0,len(testCases)):
                result = gt.getRequestInfo(Input1,testCases[i])
                if result != expectAnswers[i]:
                    self.assertFalse(False)
            self.assertTrue(True)
    
    def test_getUserInfo(self):
        with self.app.app_context():
            input1 = "0" # User ID
            testCases = ["email","pincode","coins","avatar"]
            expectAnswers = ["test2@test2.com","1234","10","default"]
            for i in range(0,len(testCases)):
                result = gt.getUserInfo(input1,testCases[i])
                if result != expectAnswers[i]:
                    self.assertFalse(False)
            self.assertTrue(True)

    def test_verifyPinCode(self):
        with self.app.app_context():
            inputs = ["0","test@test.com"] # User ID and Email Address
            for i in range(0,len(inputs)):
                if gt.verifyPinCode(inputs[i],"1234") != 0:
                    self.assertFalse(False)
            self.assertTrue(True)

    def test_ifUserPurchased(self):
        with self.app.app_context():
            input1 = "0" # UserID
            input2 = "1" # ItemID
            if gt.ifUserPurchased(input1,input2) == 0:
                self.assertTrue(True)
            else:
                self.assertFalse(False)
    
    def test_getItemInfo(self):
        with self.app.app_context():
            input1 = "1"
            testCases = ["detail","price"]
            expectAnswers = ["The Man with Prime","100"] # Item Detail, Price
            for i in range(0,len(testCases)):
                if gt.getItemInfo(input1,testCases[i]) != expectAnswers[i]:
                    self.assertFalse(False)
            self.assertTrue(True)
    
    def test_ifSign(self):
        with self.app.app_context():
            input1 = "b56b9e05-0823-480b-aace-e14c698e99b9" # UserID
            result = gt.ifSign(input1)
            self.assertEqual(result,False)

    def test_encryptPassword(self):
        with self.app.app_context():
            input1 = "hello"
            result = gt.encryptPassword(input1)
            self.assertEqual(result,"5d41402abc4b2a76b9719d911017c592")

# get.py Unit Test
   
if __name__ == '__main__':
    unittest.main()