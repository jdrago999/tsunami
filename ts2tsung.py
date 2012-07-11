import argparse
from tsunami import TsungBuilder
from tsunami import LoadParser

if __name__ == '__main__':
    cmd_parser = argparse.ArgumentParser('Load Testing DSL to Tsung Parser')

    cmd_parser.add_argument('--from',
                            type=str, help='.lt source file',
        required=True)
    cmd_parser.add_argument('--to', type=str, help='tsung .xml output file', 
        required=True)
    
    args = cmd_parser.parse_args()

    # 'from' is a reserved word, so we have to use this extended syntax
    # instead of args.from
    from_file = args.__getattribute__("from") 
    with open(from_file) as f:
        code = f.read()
    lp = LoadParser()
    config = lp.parse(code) 

    tb = TsungBuilder(config)
    with open(args.to, "w+") as f:
        f.write(tb.get_xml())    
