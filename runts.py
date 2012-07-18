#!/usr/bin/env python
import argparse
import time
import os
import shutil

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

    to_dir = "/tmp/tsung-tsunami-%s" % time.time()    
    os.makedirs(to_dir)

    tb = TsungBuilder(config, to_dir)
    to_filename = os.path.join(to_dir, "tsung.xml")
    with open(to_filename, "w+") as f:
        f.write(tb.get_xml())    

    cmd = "cd %s && tsung -f tsung.xml start && cd - " % to_dir
    os.system(cmd)
    shutil.rmtree(to_dir)
