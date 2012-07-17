from lxml.builder import E
from lxml import etree
import re

class TsungBuilder(object):
    def __init__(self, config):
        self.config = config

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
        
        tags = E.tsung(*[clients, servers, load, sessions], 
                       loglevel="info", dumptraffic="false")
        return tags

    def get_clients(self):
        return E.clients(
            E.client(host="localhost", use_controller_vm="true"))
        
    def get_servers(self):
        return E.servers(
            E.server(host="localhost", port="8000", type="tcp"))

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
        # TODO: Grep out type='request' once we get some other action types
        return [self.get_action(a) for a in session.actions]

    def get_action(self, a):
        if a.type == "var":
            return self.get_var(a)
        if a.type == "pause":
            return self.get_pause(a)
        else:
            return self.get_request(a)
    
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
                attrs["sourcetype"] = "file"
                attrs["order"] = "iter"
                attrs["fileid"] = "_%s.csv" % v.name
                attrs["delimiter"] = ";"

        return E.setdynvars(E.var(name=v.name), **attrs)

    def get_request(self, r):
        url = r.url
        new_url = re.sub(r'\$(\w*)', r'%%\1%%', url)

        method = r.method.upper()
        tags = [E.http(url=new_url, method=method, version="1.1")]
        tags.extend([self.get_match(m) for m in r.matches])

        req_attrs = dict()
        if new_url != url:
            req_attrs["substr"] = "true"

        return E.request(*tags, **req_attrs)

    def get_match(self, m):
        return E.match(m.regex, do="log", when="nomatch") 
