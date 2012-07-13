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
    post '/view?name=view2&value=foo'
        ensure match /^{"success": "View 'view2' created"}$/
        ensure match /success/


create session with weight 1 as 'test2':
    get '/foo'

create load:
    spawn 1 users every 1 seconds for 1 seconds
""")
        
        self.assertEqual(len(result.sessions), 2)
        session = result.sessions[0]
        self.assertEqual(session.weight, "4")
        self.assertEqual(session.name, "test1")        
        self.assertEqual(len(session.actions), 3)
        get_action = session.actions[0]
        self.assertEqual(get_action.method, "get")
        self.assertEqual(get_action.url, "/api")
        self.assertEqual(get_action.type, "get")

        delete_action = session.actions[1]
        self.assertEqual(delete_action.method, "delete")
        self.assertEqual(delete_action.url, "/view/view1")
        post_action = session.actions[2]
        self.assertEqual(len(post_action.matches), 2)
        match = post_action.matches[1]
        self.assertEqual(match.regex, "success")


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

    def test_comment(self):
        parser = LoadParser()
        result = parser.parse("""
# Here is a big comment
# That spans multiple lines

create session with weight 1 as 'test1':
    get '/foo'

create load:                
    spawn 1 users every 1 seconds for 1 seconds
""")
        # as long as we got here and the above didn't die, we're good
        self.assertTrue(True) 

    def test_pause(self):
        parser = LoadParser()
        result = parser.parse("""
create session with weight 1 as 'test1':
    get '/bar'
    pause between 1.5 and 3.2 seconds
    get '/foo'

create load:                
    spawn 1 users every 1 seconds for 1 seconds
""")
        session = result.sessions[0]
        self.assertEquals(len(session.actions), 3)
        pause_action = session.actions[1]
        self.assertEqual(pause_action.type, "pause")
        self.assertEqual(pause_action.lower_time, "1.5")
        self.assertEqual(pause_action.upper_time, "3.2")
        self.assertEqual(pause_action.time_units, "seconds")

if __name__ == '__main__':
    unittest.main()

