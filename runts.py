#!/usr/bin/env python
import argparse
import time
import os

from tsunami import TsungBuilder
from tsunami import LoadParser

if __name__ == '__main__':
    cmd_parser = argparse.ArgumentParser('Load Testing DSL to Tsung Parser')

    cmd_parser.add_argument('--source', type=str, help='tsunami source file',
        required=True)
    cmd_parser.add_argument('--environment', type=str, 
                            help='testing environment',
                            default="tsung")
    args = cmd_parser.parse_args()

    with open(args.source) as f:
        code = f.read()
    lp = LoadParser()
    config = lp.parse(code) 

    
    tb = TsungBuilder(config)
    to_filename = "/tmp/tsung-tsunami-%s.xml" % time.time()
    with open(to_filename, "w+") as f:
        f.write(tb.get_xml())    

    cmd = "tsung -f test/files/simple_working.xml start"
    os.system(cmd)
    os.remove(to_filename)
