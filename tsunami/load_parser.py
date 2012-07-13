
from pyparsing import Keyword, Word, nums, QuotedString, OneOrMore, \
    Forward, Group, Optional, restOfLine, Combine

from pprint import pprint
class LoadParser:
    def __init__(self):
        intNum = Word(nums)
        floatNum = Combine(intNum + Optional("." + intNum))
        string = QuotedString("'")
        regex = QuotedString("/")
        time_period = Keyword("minutes") | Keyword("seconds")

        pause = Group(Keyword("pause").setResultsName("type") + \
            Keyword("between") + \
            floatNum.setResultsName("lower_time") + Keyword("and") + \
            floatNum.setResultsName("upper_time") + Keyword("seconds"))

        get = Keyword("get").setResultsName("method")
        post = Keyword("post").setResultsName("method")
        put = Keyword("put").setResultsName("method")
        delete = Keyword("delete").setResultsName("method")
        method = (get | post | put | delete).setResultsName("type")

        url = string.setResultsName("url")
        match = Group( \
            Keyword("ensure") + Keyword("match") + \
            regex.setResultsName("regex"))
        match_list = Group(OneOrMore(match)).setResultsName("matches")

        request = Group(method + url + Optional(match_list)).setName("request")
        action = request | pause
        action_list = \
            Group(OneOrMore(action)).setResultsName("actions")

        session = Group( Keyword("create") + \
            Keyword("session") + Keyword("with") + \
            Keyword("weight") + \
            intNum.setResultsName("weight")  + Keyword("as") + \
            string.setResultsName("name")  + \
            ":" + action_list)
        session_list = OneOrMore(session).setResultsName("sessions")
        
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

        comment = "#" + restOfLine

        script = session_list + load
        script.ignore(comment)

        self.grammar = script
        self.symbols = {
            'sessions': []
        }


    def parse(self, code):
        result = self.grammar.parseString(code)
        return result

