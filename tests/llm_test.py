import unittest
import os, sys
import apps.llm as llm

class TestLLM(unittest.TestCase):
    def test_llmreq(self):
        llmReqGen = llm.llmRequests()
        if "." or "?" in llmReqGen:
            self.assertTrue(True)
    # Test LLM to generate Request
    
    def test_llmans(self):
        llmAnsGen = llm.llmAnswers()
        if "." or "?" in llmAnsGen:
            self.assertTrue(True)
    # Test LLM to generate Answers

if __name__ == '__main__':
    unittest.main()