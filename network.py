import os
import argparse
import pstats
from pyvis.network import Network
import plotly.graph_objects as go

print('Started')

parser = argparse.ArgumentParser(prog='network.py')
parser.add_argument('-file', help='Network path file to process')
parse = parser.parse_args()

def createNetworkGraph(_matrix):
   
    _network = Network()
    #_network.show_buttons(filter_=['physics'])

    # Create nodes
    for key, value in _matrix.items():
        # New node
        _node_weight = len(value)
        _color = "#{0:02x}{1:02x}FF".format(int(200/(_node_weight+1)), int(75.0/(_node_weight+1)))
        _network.add_node(key, label=key, title="Node: {0} - Weight: {1}".format(key, _node_weight), value=10+_node_weight, color=_color)
    
    # Create relationships
    for source, sinks in _matrix.items():
        for sink in sinks:
            if sink not in _matrix.keys():
                # New node
                _node_weight = 1
                _color = "#{0:02x}{1:02x}FF".format(int(200/(_node_weight+1)), int(75.0/(_node_weight+1)))
                _network.add_node(sink, label=sink, title="Node: {0} - Weight: {1}".format(sink, _node_weight), value=10+_node_weight, color=_color)

            # New relationship
            _network.add_edge(source, sink)

    _network.show('routers_data_undirected_result.html')

def createHistogram(_matrix):
    _plot = go.Figure()

    x = []
    y = []

    for key, value in _matrix.items():
        x.append(key);
        y.append(len(value))

    _plot.add_trace(go.Histogram(y=y, x=x, name='Node Links'))
    _plot.show()

if parse.file:
    _source_file = os.path.join( os.getcwd(), parse.file);      
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
        # createNetworkGraph(_matrix)

        # Create histogram
        createHistogram(_matrix)

    except Exception as err:
        print(err)
    
else:
    parser.print_help()

print('Completed')