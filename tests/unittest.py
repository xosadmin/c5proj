import unittest
from ..app import *
from .. import llm

class TestAuth(unittest.TestCase):
    def test_email_exists(self):
        email = "test@test.com"
        getReturn = app.checkEmail(email)
        self.assertEqual(getReturn, 0) 
        # Test checkEmail() function
        # The "test@test.com" already in the database. It is expected to return 0

class TestLLM(unittest.TestCase):
    def test_llmreq(self):
        llmReqGen = llm.llmRequests()
        if "." or "?" in llmReqGen:
            self.assertTrue()
    # Test LLM to generate Request
    
    def test_llmans(self):
        llmAnsGen = llm.llmAnswers()
        if "." in llmAnsGen:
            self.assertTrue()
    # Test LLM to generate Answers

if __name__ == '__main__':
    unittest.main()