import os
import argparse
from turtle import title
from pyvis.network import Network

def createNetworkGraph(_matrix):
    _network = Network()
    _network.show_buttons(filter_=True)

    # Create nodes
    for row in range(len(_matrix)):
        # New node
        _node_weight = getWeight(_matrix, row)
        _color = "#{0:02x}{1:02x}FF".format(int(100.0/(_node_weight+1)), int(100.0/(_node_weight+1)))
        _network.add_node(row, label=row, title="Node: {0} - Weight: {1}".format(row, _node_weight), value=10+_node_weight, color=_color)
    
    # Create relationships
    for row in range(len(_matrix)):
        for column in range(len(_matrix[row])):

            if _matrix[row][column] == 1:
                # New relationship
                _network.add_edge(row, column)

    _network.show('nodes.html')

def createHistogram(_weight):
    pass

def getWeight(_matrix, _node):
    weight = 1

    for row in range(len(_matrix)):
        if _matrix[row][_node] == 1 or _matrix[_node][row] == 1:
            weight += 1;

    return weight-1

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

        # Create network chart
        createNetworkGraph(_matrix)

        # Create histograph
        createHistogram(_matrix)

    except Exception as err:
        print(err)
    
else:
    parser.print_help()

print('Completed')