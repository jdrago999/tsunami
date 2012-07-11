#!/usr/bin/env python
import os
import sys
sys.path.append(os.path.dirname(__file__) + '/..')


import unittest2 as unittest
from tsunami import LoadParser
from pprint import pprint

class TestLoadParser(unittest.TestCase):
    
    def test_session(self):
        parser = LoadParser()
        result = parser.parse("""
create session with weight 4 as 'test1':
    get '/api'
    delete '/view/view1'

create session with weight 1 as 'test2':
    get '/foo'
""")
        
        self.assertEqual(len(result.sessions), 2)
        session = result.sessions[0]
        self.assertEqual(session.weight, "4")
        self.assertEqual(session.name, "test1")        
        self.assertEqual(len(session.actions), 2)
        get_action = session.actions[0]
        self.assertEqual(get_action.method, "get")
        self.assertEqual(get_action.url, "/api")
        delete_action = session.actions[1]
        self.assertEqual(delete_action.method, "delete")
        self.assertEqual(delete_action.url, "/view/view1")
                         
if __name__ == '__main__':
    unittest.main()

