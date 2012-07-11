import re 
from pprint import pprint

class LoadParser(object):
    def __init__(self):  
        self.stack = []
        self.line_number = 0
        self.state = {
            'sessions': []
        }

    def parse(self, code):
        sessions = []

        self.add_code(code) 
        operations = [
            (r"create session with weight (\d+) as '(\w+)'", \
                self.create_session),
            (r"^$", self.no_op)
        ]

        self.process_lines(operations)
                  
        return self.state['sessions']

    def process_lines(self, operations):
        line = self.get_next_line()
        while True:
            line = self.get_next_line()
            if not line: 
                break
            matched = False;
            for pattern, method in operations:
                match = re.search(pattern, line)
                if match:
                    method(match.groups())
                    matched = True
                    break
                
            if not matched:
                self.error("Unrecognized Statement")
                 

    def add_code(self, code):
        self.stack.extend(code.split("\n"))

    def get_next_line(self):
        if (self.stack):
            self.line_number += 1
            self.current_line = self.stack.pop(0).strip()
            return self.current_line
        return None
        

    def error(self, msg):
        print "Error: %s on line %s:" % (msg, self.line_number)
        print self.current_line
        exit()

    def create_session(self, (weight, name)):
        session = {
            'weight': int(weight),
            'name': name,
            'actions': []
        }


        self.state['sessions'].append(session)
        
        operations = [
            (r"(get|delete) '([^']+)'", self.request),
            (r"^$", self.no_op)
        ]
        self.process_lines(operations)

    def request(self, (method, url)):
        print "Creating Request: %s" % method

        session = self.state['sessions'][-1]
        action = {
            'type': 'request',
            'method': method,
            'url': url
        }
        session["actions"].append(action)

    def no_op(self, (params)):
        pass 
