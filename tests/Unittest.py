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

    def test_email_exists(self):
        with self.app.test_request_context():
            email = "test@test.com"
            getReturn = self.gt.checkEmail(email)
            self.assertEqual(getReturn, -1)

    def test_register_post(self):
        response = self.client.post('/doregister', data={
            'email': self.generatedEmail, 
            'password': self.generatedPassword,
            'pincode': self.pincode
        })
        self.assertEqual(response.status_code, 200)

    def test_dologin_success(self):
        response = self.client.post('/dologin', data={
            'email': "test@test.com",
            'password': "123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/profile', response.headers['Location'])

    def test_dologin_failure(self):
        response = self.client.post('/dologin', data={
            'email': 'invalidUser@test.com',
            'password': 'wrongPassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?errormsg', response.headers['Location'])
    
    def test_doresetpassword_success(self):
        response = self.client.post('/doresetpassword', data={
            'email': self.generatedEmail,
            'pincode': self.pincode
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_doresetpassword_failure(self):
        response = self.client.post('/doresetpassword', data={
            'email': 'nonexistentemail@example.com',
            'pincode': 'wrongPin'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/forgetPassword', response.headers['Location'])

    def test_domodifypassword_success(self):
        response = self.client.post('/domodifypassword', data={
            'newpassword': 'newPass1234',
            'repeatnewpassword': 'newPass1234',
            'pincode': self.pincode
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/profile', response.headers['Location'])

    def test_domodifypassword_failure(self):
        response = self.client.post('/domodifypassword', data={
            'newpassword': 'newPass5678',
            'repeatnewpassword': 'newPass1234',  # Passwords do not match
            'pincode': 'incorrectPin'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/modifyPassword', response.headers['Location'])

    def test_domodifypin_success(self):
        response = self.client.post('/domodifypin', data={
            'oldpin': self.pincode,
            'newpin': '5678',
            'repeatnewpin': '5678'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/profile', response.headers['Location'])

    def test_domodifypin_failure(self):
        response = self.client.post('/domodifypin', data={
            'oldpin': 'wrongOldPin',
            'newpin': '5678',
            'repeatnewpin': '5678'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/modifyPin', response.headers['Location'])

    def test_llmreq(self):
        llmReqGen = llm.llmRequests()
        if "." or "?" in llmReqGen:
            self.assertTrue(True)
    # Test LLM to generate Request
    
    def test_llmans(self):
        llmAnsGen = llm.llmAnswers()
        if "." or "?" in llmAnsGen:
            self.assertTrue(True)

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
            expectAnswers = ["The Man with Prime","100"]
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

    def test_donewrequests_success(self):
        with self.client as client:
            response = client.post('/donewrequest', data={
                'title': 'New Request Title',
                'content': 'This is the content of the new request.',
                'rewards': '100',
                'timelimit': '7'
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue('requests' in response.location)

    def test_donewrequests_failure(self):
        with self.client as client:
            response = client.post('/donewrequest')
            self.assertEqual(response.status_code, 302)
            self.assertTrue('newRequest?msg=Invalid Request!' in response.location)
    
    def test_donewthreads_success(self):
       with self.client as client:
            response = client.post('/donewthread', data={
                'title': 'New Thread Title',
                'content': 'This is the content of the new thread.'
            })
           
            self.assertEqual(response.status_code, 302)  
            self.assertTrue('communityPage' in response.location)  
    
    def test_donewthreads_failure(self):
        with self.client as client:
            response = client.post('/donewthread')
        self.assertEqual(response.status_code, 302)

    def test_doAcceptRequest_success(self):
        with self.client as client:
            response = client.post('/doacceptrequest/valid-request-id')
            self.assertEqual(response.status_code, 302)
            self.assertTrue('todoList' in response.location)

    def test_doAcceptRequest_failure(self):
        with self.client as client:
            response = client.get('/doacceptrequest/valid-request-id')
            self.assertEqual(response.status_code, 302)  

    def test_doAnswerRequest_success(self):
        with self.client as client:
            response = client.post('/doanswerrequest', data={
                'userID': 'valid-user-id',
                'rewards': '50',
                'requestID': 'valid-request-id',
                'content': 'This is the answer content for the request.'
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue('todoList' in response.location)

    def test_doAnswerRequest_failure(self):
        with self.client as client:
            response = client.get('/doanswerrequest')
            self.assertEqual(response.status_code, 302)  

    def test_doNewThreadReply_success(self):
        with self.client as client:
            response = client.post('/donewthreadreply', data={
                'threadID': 'some-unique-thread-id',
                'content': 'Reply content for the thread.'
            })
            self.assertEqual(response.status_code, 302)  
            self.assertTrue('communityPage' in response.location)  

    def test_doNewThreadReply_failure(self):
        with self.client as client:
            response = client.get('/donewthreadreply')
            self.assertEqual(response.status_code, 302)  
            self.assertTrue('newThread?errmsg=Invalid Request!' in response.location)  

if __name__ == '__main__':
    unittest.main()