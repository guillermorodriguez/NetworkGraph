import os
import argparse

print('Started')


parser = argparse.ArgumentParser(prog='netowrk.py')
parser.add_argument('-file', help='Network path file to process')
parser.add_argument('-lines', help='Maximum number of lines to process, negative values denote complete processing of file')
parse = parser.parse_args()

if parse.file and parse.lines:
    _source_file = os.getcwd() + '\\' + parse.file;         # File to process
    _max_nodes = 0                                          # Maximum network nodes in landscape

    try:
        # Determine maximum number of nodes to create
        _current_line = 1;
        with open(_source_file, 'r') as _network_paths:
            for entry in _network_paths:
                _source, _sink = int(entry.strip('\n').split('\t')[0]), int(entry.strip('\n').split('\t')[1])
                
                if _source > _max_nodes:
                    _max_nodes = _source
                if _sink > _max_nodes:
                    _max_nodes = _sink

                if int(parse.lines) > 0 and _current_line >= int(parse.lines):
                    break

                _current_line += 1
        
        print("{0} Nodes in Network".format(_max_nodes))

        # Create blank network matrix for processing of relationships
        #  0 -> No relationship
        _matrix = [] 
        for row in range(_max_nodes + 1):
            _current_row = []
            for column in range(_max_nodes + 1):
                _current_row.append(0)

            _matrix.append(_current_row)

        print('Blank Matrix = ', _matrix)

        # Populate relationship matrix with actual network maps
        #   1 -> Relationship exists
        _current_line = 1;
        with open(_source_file, 'r') as _network_paths:
            for entry in _network_paths:
                _matrix[int(entry.strip('\n').split('\t')[0])][int(entry.strip('\n').split('\t')[1])] = 1;

                if int(parse.lines) > 0 and _current_line >= int(parse.lines):
                    break

                _current_line += 1

        print('Relational Matrix', _matrix)

    except Exception as err:
        print(err)
    
else:
    parser.print_help()

print('Completed')