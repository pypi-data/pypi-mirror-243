import unittest

from context import *

import matplotlib.pyplot as plt
import networkx as nx

class NetVizTestCase(unittest.TestCase):
    
    @unittest.skip    
    def testDirectMatlab(self):
        return 
        """Tests the direct use of the drawing-funktionality with networkx""" 
        self.client = NetAPIClient("http://localhost:8080/")
        req = GraphQueryRequest()\
            .setSourceObject(
                Source("InputStreamReplayToSource", "SimpleTestGraph.dgs")
                    .setArgs(limit = 1000, another = "A")
            )
        res = self.client.query(req)
        
        graphModel = res.getGraphModel()
        
        nx_graph = graphModel.asMultiDiGraph()
        
        # Positionen
        #pos = nx.kamada_kawai_layout(nx_graph)
        pos = nx.circular_layout(nx_graph)
        
        nodesize = [1 * 150 for v in nx_graph]
        
        nx.draw_networkx_edges(
            nx_graph, pos, 
            connectionstyle='arc3,rad=0.1',
            alpha=0.3, width=3, edge_color="m")
        
        nx.draw_networkx_nodes(nx_graph, pos, node_size=nodesize, node_color="#210070", alpha=0.9)
        
        label_options = {"ec": "k", "fc": "white", "alpha": 0.7}
        nx.draw_networkx_labels(
            nx_graph, pos, 
            font_size=10, 
            verticalalignment='center',
            bbox=label_options)
        
        plt.show()
    
    @unittest.skip    
    def testDirectNetGraph(self):
        """Tests the direct use of the drawing-funktionality with networkx""" 
        
        from netgraph import Graph
        
        self.client = NetAPIClient("http://localhost:8080/")
        req = GraphQueryRequest()\
            .setSourceObject(
                Source("InputStreamReplayToSource", "SimpleTestGraph.dgs")
                    .setArgs(limit = 1000, another = "A")
            )
        res = self.client.query(req)
        
        graphModel = res.getGraphModel()
        
        nx_graph = graphModel.asMultiDiGraph()
        
        # Positionen
        pos = nx.circular_layout(nx_graph)
        
        plot_instance = Graph(nx_graph,
            node_layout=pos,
            node_size = 10,
            node_labels = True,
            node_label_offset = 0.2,
            node_edge_width = 0.1,
            edge_width = 1,
            edge_layout = 'curved',
            arrows=True)
        
        plt.show()
        
    def testNetViz(self):
        """Tests the NetViz-Drawing interface""" 
        self.client = NetAPIClient("http://localhost:8080/")
        req = GraphQueryRequest()\
            .setSourceObject(
                Source("InputStreamReplayToSource", "SimpleTestGraph.dgs")
                    .setArgs(limit = 1000, another = "A")
            )
        res = self.client.query(req)
        
        graphModel = res.getGraphModel()
        nx_graph = graphModel.asMultiDiGraph()
        
        positions = nx.circular_layout(nx_graph)
        print("positions: " + str(positions))
        
        viz1 = NetViz.getInstance(nx_graph)\
            .setNodeSize(lambda n: 15)\
            .setNodeLabels(True)\
            .setNodePositions(positions)
            
        viz1.plot("../tests_output/testNetViz1.svg")
        
        print("DegreeA: " + str(nx_graph.degree['D']))
        
        # das gleiche. Aber mit (impliziten) Positionen über Attribute am Knoten
        viz2 = NetViz.getInstance(nx_graph)\
            .setNodeSize(lambda n: n.degree() * 50, 20, 100) \
            .setNodeLabels(True) \
            .setNodeColor(lambda n: n.get('color')) \
            .setEdgeWidth(lambda e: 1)
            
        viz2.plot("../tests_output/testNetViz2.svg")
        