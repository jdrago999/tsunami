#!/usr/bin/env python
import argparse
import time
import os
import shutil
import glob

from tsunami import TsungBuilder
from tsunami import LoadParser

if __name__ == '__main__':
    cmd_parser = argparse.ArgumentParser('Load Testing DSL to Tsung Parser')

    cmd_parser.add_argument('--source', type=str, help='tsunami source file',
        required=True)
    cmd_parser.add_argument('--source_files_dir', 
        help='directory where this source files supplimentary csv files live')
    cmd_parser.add_argument('--environment', type=str, 
                            help='testing environment',
                            default="tsung")
    args = cmd_parser.parse_args()

    if not args.source_files_dir:
        args.source_files_dir = os.path.split(args.source)[0]

    with open(args.source) as f:
        code = f.read()
    lp = LoadParser()
    config = lp.parse(code) 

    to_dir = "/tmp/tsung-tsunami-%s" % time.time()    
    os.makedirs(to_dir)
    # copy all the suplimental files to our working directory
    for filename in glob.glob(os.path.join(args.source_files_dir, '*.*')):
        shutil.copy(filename, to_dir)

    tb = TsungBuilder(config, to_dir)
    to_filename = os.path.join(to_dir, "tsung.xml")
    with open(to_filename, "w+") as f:
        f.write(tb.get_xml())    

    cmd = "cd %s && tsung -f tsung.xml start && cd - " % to_dir
    os.system(cmd)
    shutil.rmtree(to_dir)
