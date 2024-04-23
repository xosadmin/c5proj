import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from apps.get import *

class TestGETPY(unittest.TestCase):
    def test_checkEmail(self):
        Input = "test@test.com" # Email address that existed in the system
        result = checkEmail(Input)
        self.assertEqual(result,"-1")
    
    def test_getThreadTitle(self):
        Input = "117715ff-1b38-4410-b8f2-23ead632642e" # Thread ID
        result = getThreadTitle(Input)
        self.assertEqual(result,"ehgjreh")

    def test_getCoins(self):
        Input = "b56b9e05-0823-480b-aace-e14c698e99b9" # UserID
        result = getCoins(Input)
        self.assertEqual(result,"10")

    def test_getRequestInfo(self):
        Input1 = 21 # RequestID
        testCases = ["userID","state","rewards"]
        expectAnswers = ["0", "Completed", "123"] # [userid, status, rewards]
        for i in range(0,testCases):
            result = getRequestInfo(Input1,testCases[i])
            if result != expectAnswers[i]:
                self.assertFalse()
        self.assertTrue()
    
    def test_getUserInfo(self):
        input1 = "0" # User ID
        testCases = ["email","pincode","coins","avatar"]
        expectAnswers = ["test2@test2.com","1234","10","default"]
        for i in range(0,testCases):
            result = getUserInfo(input1,testCases[i])
            if result != expectAnswers[i]:
                self.assertFalse()
        self.assertTrue()

    def test_verifyPinCode(self):
        inputs = ["0","test@test.com"] # User ID and Email Address
        for i in range(0,len(inputs)):
            if verifyPinCode(inputs[i],"1234") != 0:
                self.assertFalse()
        self.assertTrue()

    def test_ifUserPurchased(self):
        input1 = "0" # UserID
        input2 = "1" # ItemID
        if ifUserPurchased(input1,input2) == 0:
            self.assertTrue()
        else:
            self.assertFalse()
    
    def test_getItemInfo(self):
        input1 = "1"
        testCases = ["detail","price"]
        expectAnswers = ["The Man with Prime","100"]
        for i in range(0,testCases):
            if getItemInfo(input1,testCases[i]) != expectAnswers[i]:
                self.assertFalse()
        self.assertTrue()
    
    def test_ifSign(self):
        input1 = "b56b9e05-0823-480b-aace-e14c698e99b9" # UserID
        result = ifSign(input1)
        self.assertEqual(result,False)

    def test_encryptPassword(self):
        input1 = "hello"
        result = encryptPassword(input1)
        self.assertEqual(result,"5d41402abc4b2a76b9719d911017c592")

if __name__ == '__main__':
    unittest.main()