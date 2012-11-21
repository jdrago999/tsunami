from lxml.builder import E
from lxml import etree
import re
import os
from pprint import pprint

# TODO: Grep out non local http requests for request_all

class TsungBuilder(object):
    def __init__(self, config={}, output_path=".",
                 server_hostname="localhost", server_port=80):
        self.config = config
        self.output_path = output_path
        self.server_hostname = server_hostname
        self.server_port = server_port
        self.csvs = []
        self.using_vars = set()


    def get_xml(self):
        pieces = []
        pieces.append('<?xml version="1.0"?>')
        pieces.append('<!DOCTYPE tsung' + 
                      ' SYSTEM "/usr/share/tsung/tsung-1.0.dtd" [] >')
        xml = etree.tostring(self.get_tsung_tags(), pretty_print=True)
        pieces.append(xml)
        return "\n".join(pieces)

    def tags_to_string(self, elements):
        pieces = [etree.tostring(e, pretty_print=True) for e in elements] 
        return "\n".join(pieces)

    def get_tsung_tags(self):
        clients = self.get_clients()
        servers = self.get_servers()
        load = self.get_load()
        sessions = self.get_sessions()
        options = self.get_options()


        tags = E.tsung(*[clients, servers, load, options, sessions], 
                       loglevel="info", dumptraffic="false")
        return tags

    def get_options(self):
        options = [self.get_option(file_id, filename) \
            for file_id, filename in self.csvs] 
        return E.options(*options)

    def get_option(self, file_id, filename):
        return E.option(id=file_id, name="file_server", value=filename)

    def get_clients(self):
        return E.clients(
            E.client(host="localhost", use_controller_vm="true"))
        
    def get_servers(self):
        return E.servers(
            E.server(host=self.server_hostname, \
                         port=str(self.server_port), type="tcp"))

    def get_load(self):
        load = self.config.load
        load.phase_count = 0
        arrival_phase_tags = [self.get_arrival_phase(p, load) 
                              for p in load.spawns]

        return E.load(*arrival_phase_tags)

    def get_arrival_phase(self, p, load):
        load.phase_count += 1
        user_attrs = dict(arrivalrate=p.user_time,
                          unit=p.user_time_units[:-1])
        if p.max_users:
            user_attrs["maxnumber"] = p.max_users

        return E.arrivalphase(
            E.users(**user_attrs), phase=str(load.phase_count),
                duration=p.max_duration, unit=p.max_duration_units[:-1])

    def get_sessions(self):
        total_weight = sum([ int(s.weight) for s in self.config.sessions])

        session_tags = [self.get_session(s, total_weight) \
                            for s in self.config.sessions ]
        return E.sessions(*session_tags)

    def get_session(self, s, total_weight):
        action_tags = self.get_actions(s)
        probability = str(int(float(s.weight) / total_weight * 100.0))
        return E.session(*action_tags, 
                          name=s.name, probability=probability, type="ts_http")

    def get_actions(self, session):
        tags = []
        for a in session.actions:
            action = self.get_action(a)
            if isinstance(action, list): 
                tags.extend(action)
            else:
                tags.append(action)

        return tags

    def get_action(self, a):
        if a.type == "var":
            return self.get_var(a)
        if a.type == "using":
            return self.get_using(a)
        if a.type == "pause":
            return self.get_pause(a)
        else:
            regex_matches = [m.regex for m in a.matches]
            return self.get_request(method=a.method, url=a.url, \
                regex_matches=regex_matches, retrieve_all=a.all, \
                data=a.data)
    
    def get_using(self, u):
        for v in u.vars:
            self.using_vars.add(v) 
        var_tags = [E.var(name=v) for v in u.vars]
        base_filename = os.path.splitext(u.filename)[0]
        file_id = "%s_file" % base_filename
        self.add_csv(file_id, u.filename)
        return E.setdynvars(*var_tags, sourcetype="file", \
            fileid=file_id, delimiter=";", order="random")

    def get_pause(self, p):
        return E.thinktime(max=p.upper_time, min=p.lower_time, random="true")

    def get_var(self, v):
        attrs = {}
        if v.data_type == "string":
            attrs["sourcetype"] = "random_string"
            attrs["length"] = v.length            
        else:
            if v.ordering == "random":
                attrs["sourcetype"] = "random_number"
                attrs["start"] = v.min
                attrs["end"] = v.max
            else:
                filename = "_%s.csv" % v.name
                file_id = "%s_file" % v.name
                attrs["sourcetype"] = "file"
                attrs["order"] = "iter"
                attrs["fileid"] = file_id
                attrs["delimiter"] = ";"
                self.create_range_file( \
                    filename, int(v.min), int(v.max))
                self.add_csv(file_id, filename)

        return E.setdynvars(E.var(name=v.name), **attrs)

    def add_csv(self, file_id, filename):
        self.csvs.append((file_id, filename))

    def get_request(self, url, method, regex_matches,
                    retrieve_all=False, data=None):
        outer_tags = []
        method = method.upper()

        new_url = self.substitute(url)
        inner_tags = [self.get_match(regex) for regex in regex_matches] 
        # TODO: make sure vars and match have the correct order
        # TODO: Make sure we can have multiple set vars with the same name
        if retrieve_all:
            inner_tags.extend(self.get_dependency_vars())
        http_attrs = dict(url=new_url, method=method, version="1.1")
        if data:
            http_attrs["contents"] = self.substitute(data)
        inner_tags.append(E.http(**http_attrs))

        req_attrs = dict()

        # figure out if any matches have substitutions.  This happens
        # when any of the match regexes contian '$word'
        data_has_substitutions = self.substitute(data) != data
        match_has_substitutions = bool([regex for regex in regex_matches 
            if self.substitute(regex) != regex])
        url_has_substitutions = url != new_url
        if (url_has_substitutions or match_has_substitutions or 
            data_has_substitutions):
            req_attrs["subst"] = "true"
        outer_tags.append(E.request(*inner_tags, **req_attrs)) 
        if retrieve_all:
            for name in ("css", "img", "script"):
                outer_tags.append(self.get_dependency_forecach(name))

        return outer_tags

    def get_dependency_forecach(self, name):
        list_name = "%s_list" % name
        exclude = r'^(https?:)?\/\/(?!%s\b)' % \
            re.escape(self.server_hostname)

        url = ''.join(['%%', "_", name, '%%' ])
        http = E.http(url=url, method="GET", version="1.1")
        request = E.request(http, subst="true")
        return E.foreach(request, **{'name':name, 'in':list_name, \
                                     'exclude': exclude})

    def get_dependency_vars(self):
        tag_attrs = [
            {'name': 'css_list', \
                 'xpath': "//link[@rel='stylesheet']/@href"},
            {'name': 'img_list', \
                 'xpath': "//img/@src"},
            {'name': 'script_list', \
                 'xpath': "//script/@src"},
        ]
        return [E.dyn_variable(**attrs) for attrs in tag_attrs]

    def get_match(self, regex):
        sub_regex = self.substitute(regex)

        return E.match(sub_regex, do="log", when="nomatch") 

    def substitute(self, string):
        """replace $word with %%word%% for normal variables and
        %%_word%% for variables from `using` clauses"""

        using_string = string
        for v in self.using_vars:
            using_string = using_string.replace("$%s" % v, '%%_' + v +
                                                '%%')
        return re.sub(r'\$(\w+)', r'%%\1%%', using_string)

    def create_range_file(self, name, range_min, range_max):
        self.create_ouptupt_path()
        filename = os.path.join(self.output_path, name)
        with open(filename, "w+") as f:
            for num in xrange(range_min, range_max + 1):
                f.write(str(num) + "\n")  

    def create_ouptupt_path(self):
        dir = self.output_path
        if not os.path.exists(dir):
            os.makedirs(dir)
