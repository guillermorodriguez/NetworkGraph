import os
import argparse
import pstats

from pyvis.network import Network

def createNetworkGraph(_matrix):
   
    _network = Network()
    _network.show_buttons(filter_=True)

    # Create nodes
    for key, value in _matrix.items():
        # New node
        _node_weight = len(value)
        _color = "#{0:02x}{1:02x}FF".format(int(200/(_node_weight+1)), int(75.0/(_node_weight+1)))
        _network.add_node(key, label=key, title="Node: {0} - Weight: {1}".format(key, _node_weight), value=10+_node_weight, color=_color)
    
    # Create relationships
    for row in range(len(_matrix)):
        for column in range(len(_matrix[row])):

            if _matrix[row][column] == 1:
                # New relationship
                _network.add_edge(row, column)

    _network.show('nodes.html')

def createHistograph(_matrix):
    pass

print('Started')

parser = argparse.ArgumentParser(prog='netowrk.py')
parser.add_argument('-file', help='Network path file to process')
parser.add_argument('-lines', help='Maximum number of lines to process, negative values denote complete processing of file')
parse = parser.parse_args()

if parse.file and parse.lines:
    _source_file = os.getcwd() + '//' + parse.file;         # File to process
    _matrix = {}

    try:
        # Create data dictionary
        with open(_source_file, 'r') as _network_paths:
            for entry in _network_paths:
                _source, _sink = int(entry.strip('\n').split('\t')[0]), int(entry.strip('\n').split('\t')[1])
                
                if _source in _matrix.keys():
                    _matrix[_source].append(_sink)
                else:
                    _matrix[_source] = [_sink]

        print('Relational Matrix', _matrix)

        # Create network chart
        createNetworkGraph(_matrix)

        # Create histograph
        createHistograph(_matrix)

    except Exception as err:
        print(err)
    
else:
    parser.print_help()

print('Completed')