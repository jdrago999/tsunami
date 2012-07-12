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

create load:
    spawn 1 users every 1 seconds for 1 seconds
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

    def test_load(self):
        parser = LoadParser()
        result = parser.parse("""
create session with weight 1 as 'test1':
    get '/foo'

create load:                
    spawn 2 users every 4 seconds for 10 minutes up to 100 users
    spawn 5 users every 10 seconds for 50 minutes

""")
    
        self.assertEqual(len(result.load.spawns), 2)
        spawn1, spawn2 = result.load.spawns
        self.assertEqual(spawn1.user_count, "2")
        self.assertEqual(spawn1.user_time, "4")
        self.assertEqual(spawn1.user_time_units, "seconds")
        self.assertEqual(spawn1.max_duration, "10")
        self.assertEqual(spawn1.max_duration_units, "minutes")
        self.assertEqual(spawn1.max_users, "100")

        self.assertEqual(spawn2.user_count, "5")
        self.assertEqual(spawn2.user_time, "10")
        self.assertEqual(spawn2.user_time_units, "seconds")
        self.assertEqual(spawn2.max_duration, "50")
        self.assertEqual(spawn2.max_duration_units, "minutes")
        self.assertEqual(spawn2.max_users, "")


           
if __name__ == '__main__':
    unittest.main()

