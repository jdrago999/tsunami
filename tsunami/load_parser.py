
from pyparsing import Keyword, Word, nums, QuotedString, OneOrMore, \
    Forward, Group

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

        action_list = Group( OneOrMore(request) ).setResultsName("actions")
        session = Group( Keyword("create") + \
            Keyword("session") + Keyword("with") + \
            Keyword("weight") + \
            intNum.setResultsName("weight")  + Keyword("as") + \
            string.setResultsName("name")  + \
            ":" + action_list)

        session_list = OneOrMore(session).setResultsName("sessions")
        self.grammar = session_list
        self.symbols = {
            'sessions': []
        }


    def parse(self, code):
        result = self.grammar.parseString(code)
        return result

