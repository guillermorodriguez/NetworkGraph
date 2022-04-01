import os
import argparse
from pyvis.network import Network
import plotly.graph_objects as go

print('Started')

parser = argparse.ArgumentParser(prog='network.py')
parser.add_argument('-file', help='Network path file to process')
parser.add_argument('-slice', help='Individual 200 records to start to take into consideration from')
parse = parser.parse_args()

def createNetworkGraph(_matrix):
   
    _network = Network(notebook=True)
    #_network.show_buttons(filter_=['physics'])
    _network.width = 1000
    _network.height = 800

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

    _network.show(os.path.join(os.getcwd(), 'output', parse.file + '_network_graph.html'))

def createHistogram(_x, _y):
    _plot = go.Figure()

    _plot.add_trace(go.Histogram(y=_y, x=_x, name='Node Links'))
    _plot.show()
    _plot.write_html(os.path.join(os.getcwd(), 'output', parse.file + '_histogram.html'))

if parse.file and parse.slice:
    _source_file = os.path.join( os.getcwd(), 'data', parse.file);      
    _matrix = {}
    _SAMPLE_SIZE = 200

    try:
        # Create data dictionary & histogram data entries
        _entry = 1
        _x = []
        _y =[]
        with open(_source_file, 'r') as _network_paths:
            for entry in _network_paths:
                _source, _sink = int(entry.strip('\n').split('\t')[0]), int(entry.strip('\n').split('\t')[1])

                if _entry > int(parse.slice) and len(_matrix.keys()) < _SAMPLE_SIZE:
                    _x.append(_source)
                    _y.append(_sink)

                    if _source in _matrix.keys():
                        _matrix[_source].append(_sink)
                    else:
                        _matrix[_source] = [_sink]

                _entry += 1

        print('Relational Matrix', _matrix)

        # Create network chart
        createNetworkGraph(_matrix)

        # Create histogram
        createHistogram(_x, _y)

    except Exception as err:
        print(err)
    
else:
    parser.print_help()

print('Completed')