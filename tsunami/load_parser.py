
from pyparsing import Keyword, Word, nums, QuotedString, OneOrMore, \
    Forward, Group, Optional

from pprint import pprint
class LoadParser:
    def __init__(self):
        intNum = Word(nums)
        string = QuotedString("'")

        method = (Keyword("get") | Keyword("post") | Keyword("put") \
            | Keyword("delete")).setResultsName("method")
        url = string.setResultsName("url")
        request = Group(method + url)
        action = request
        action_list = \
            Group(OneOrMore(request)).setResultsName("actions")

        session = Group( Keyword("create") + \
            Keyword("session") + Keyword("with") + \
            Keyword("weight") + \
            intNum.setResultsName("weight")  + Keyword("as") + \
            string.setResultsName("name")  + \
            ":" + action_list)
        session_list = OneOrMore(session).setResultsName("sessions")
        
        time_period = Keyword("minutes") | Keyword("seconds")
        spawn = Group( Keyword("spawn") + \
            intNum.setResultsName("user_count") + \
            Keyword("users") + Keyword("every") + \
            intNum.setResultsName("user_time") + \
            time_period.setResultsName("user_time_units") + \
            Keyword("for") + \
            intNum.setResultsName("max_duration") + \
            time_period.setResultsName("max_duration_units") + \
            Optional( Keyword("up") + Keyword("to") + \
            intNum.setResultsName("max_users") +  Keyword("users")))
        spawn_list = OneOrMore(spawn).setResultsName("spawns")
        load = Group( Keyword("create") + Keyword("load") + ":" + \
            spawn_list).setResultsName("load")
        script = session_list + load
       

        self.grammar = script
        self.symbols = {
            'sessions': []
        }


    def parse(self, code):
        result = self.grammar.parseString(code)
        return result

