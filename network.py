import os
import argparse

print('Started')


parser = argparse.ArgumentParser(prog='netowrk.py')
parser.add_argument('-file', help='Network path file to process')
parser.add_argument('-lines', help='Maximum number of lines to process')
parse = parser.parse_args()

if parse.file and parse.lines:
    _source_file = os.getcwd() + '\\' + parse.file;         # File to process
    _max_nodes = 0                                          # Maximum network nodes in landscape

    try:
        _current_line = 1;
        with open(_source_file, 'r') as _network_paths:
            for entry in _network_paths:
                _source, _sink = int(entry.strip('\n').split('\t')[0]), int(entry.strip('\n').split('\t')[1])
                print(_source, _sink)

                if _current_line >= int(parse.lines):
                    break

                _current_line += 1

    except Exception as err:
        print(err)
    
else:
    parser.print_help()

print('Completed')