import unittest
from apps.get import *
from app import app, db
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

class TestGETPY(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_checkEmail(self):
        with self.app.app_context():
            Input = "test@test.com" # Email address that existed in the system
            result = checkEmail(Input)
            self.assertEqual(result,-1)
    
    def test_getThreadTitle(self):
        with self.app.app_context():
            Input = "117715ff-1b38-4410-b8f2-23ead632642e" # Thread ID
            result = getThreadTitle(Input)
            self.assertEqual(result,"ehgjreh")

    def test_getCoins(self):
        with self.app.app_context():
            Input = "b56b9e05-0823-480b-aace-e14c698e99b9" # UserID
            result = getCoins(Input)
            self.assertEqual(result,10)

    def test_getRequestInfo(self):
        with self.app.app_context():
            Input1 = 21 # RequestID
            testCases = ["userID","state","rewards"]
            expectAnswers = ["0", "Completed", "123"] # [userid, status, rewards]
            for i in range(0,len(testCases)):
                result = getRequestInfo(Input1,testCases[i])
                if result != expectAnswers[i]:
                    self.assertFalse(False)
            self.assertTrue(True)
    
    def test_getUserInfo(self):
        with self.app.app_context():
            input1 = "0" # User ID
            testCases = ["email","pincode","coins","avatar"]
            expectAnswers = ["test2@test2.com","1234","10","default"]
            for i in range(0,len(testCases)):
                result = getUserInfo(input1,testCases[i])
                if result != expectAnswers[i]:
                    self.assertFalse(False)
            self.assertTrue(True)

    def test_verifyPinCode(self):
        with self.app.app_context():
            inputs = ["0","test@test.com"] # User ID and Email Address
            for i in range(0,len(inputs)):
                if verifyPinCode(inputs[i],"1234") != 0:
                    self.assertFalse(False)
            self.assertTrue(True)

    def test_ifUserPurchased(self):
        with self.app.app_context():
            input1 = "0" # UserID
            input2 = "1" # ItemID
            if ifUserPurchased(input1,input2) == 0:
                self.assertTrue(True)
            else:
                self.assertFalse(False)
    
    def test_getItemInfo(self):
        with self.app.app_context():
            input1 = "1"
            testCases = ["detail","price"]
            expectAnswers = ["The Man with Prime","100"]
            for i in range(0,len(testCases)):
                if getItemInfo(input1,testCases[i]) != expectAnswers[i]:
                    self.assertFalse(False)
            self.assertTrue(True)
    
    def test_ifSign(self):
        with self.app.app_context():
            input1 = "b56b9e05-0823-480b-aace-e14c698e99b9" # UserID
            result = ifSign(input1)
            self.assertEqual(result,False)

    def test_encryptPassword(self):
        with self.app.app_context():
            input1 = "hello"
            result = encryptPassword(input1)
            self.assertEqual(result,"5d41402abc4b2a76b9719d911017c592")

if __name__ == '__main__':
    unittest.main()