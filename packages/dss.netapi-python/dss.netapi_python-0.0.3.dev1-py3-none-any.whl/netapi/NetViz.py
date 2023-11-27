from abc import ABC, abstractmethod

import logging
import math
import networkx as nx

from netgraph import Graph

import matplotlib
import matplotlib.pyplot as plt

from netapi import GraphModel

# TODO: Selektionen + Pfade: das ist dasgleiche!
# TODO: z-order: das ist bei NetGraph möglich. Umgekehrt nach size. (grosse unten)

class NetViz(ABC):
    
    def __init__(self, nx_graph: nx.Graph):
        self.logger = logging.getLogger("NetViz")
        self.nx_graph = nx_graph
        self.nodeSizeMin = 1
        self.nodeSizeMax = 100
        self.edgeLayout = 'straight'
        self.nodeLabelsFunc = lambda n: ""
        
        # Properties für Textscaling
        self.nodeLabelSizeScaleWithNodeSize = False
        self.nodeLabelMinSize = 8
        self.nodeLabelMaxSize = 24
        
        # Properties for Plotting
        self.figsize = (15, 15)
        
    def setNodeSize(self, func, scale = lambda s: s, min = 1, max = 100):
        self.nodeSizeFunc = func
        self.nodeSizeScale = scale
        self.nodeSizeMin = min
        self.nodeSizeMax = max
        return self
        
    def setNodeLabels(self, func):
        self.nodeLabelsFunc = func
        return self
        
    def setNodeLabelScaleWithNodeSize(self, scaleWithNodeSize: bool):
        self.nodeLabelSizeScaleWithNodeSize = scaleWithNodeSize
        return self;
        
    def setNodeLabelSize(self, _min: int, _max: int):
        self.nodeLabelMinSize = _min
        self.nodeLabelMaxSize = _max
        return self
    
    def _getNodeLabels(self):
        if hasattr(self, 'nodeLabelsFunc') == False:
            self.nodeLabelsFunc = lambda n: n.get('id')
            
        nodeLabels = dict()
        for n in self.nx_graph:
            nodeLabels[n] = self.nodeLabelsFunc(NxNodeWrapper(self.nx_graph, n))
        
        return nodeLabels      
        
    def setNodePositions(self, nodePositions: dict):
        """Sets the positions of nodes.  
        
        If the positions of nodes are *not* provided the positions are 
        derived from the nodes' attributes "x" and "y". 
        
        Keys: Nodes, Values: (x,y)
        """ 
        self.nodePositions = nodePositions
        return self
        
    def _getNodePositions(self): 
        if hasattr(self, 'nodePositions') == False:
            # nodePositions anhand x,y-Attribute der Knoten bestimmen
            xPositions = nx.get_node_attributes(self.nx_graph, "x")
            yPositions = nx.get_node_attributes(self.nx_graph, "y")
            
            self.nodePositions = dict()
            for n in self.nx_graph:
                x = xPositions.get(n)
                y = yPositions.get(n)
                if x and y:
                    self.nodePositions[n] = (x, y)
                else:
                    self.logger.warn("Node " + n + ". x or y missing. Using (0, 0)")
                    self.nodePositions[n] = (0, 0)
        
        # Rescale, damit die Werte zwischen -1 und 1 sind
        # Ansonsten kann es passieren, dass man ausserhalb der Zeichenfläche ist.
        self.nodePositions = nx.rescale_layout_dict(self.nodePositions)
        
        self.logger.debug("nodePositions: " + str(self.nodePositions))
        
        return self.nodePositions
        
    def setNodeColor(self, func):
        """Sets the color of nodes."""
        self.nodeColorFunc = func
        return self

    def _computeNodeColors(self):
        if hasattr(self, 'nodeColorFunc') == False:
            # Default-Grösse
            colorFunc = lambda n: 'white'
        else: 
            colorFunc = self.nodeColorFunc
       
        res = dict()
        for n in self.nx_graph:
            color = colorFunc(NxNodeWrapper(self.nx_graph, n))
            if color: 
                res[n] = color
            else: 
                res[n] = 'grey'
            
        self.logger.debug("nodeColors: " + str(res))    
        return res  
        
    def _computeNodeSizes(self):
        """Return a dictionary nx_node => Size"""
        if hasattr(self, 'nodeSizeFunc') == False:
            # Default-Grösse
            sizeFunc = lambda n: 3
        else: 
            sizeFunc = self.nodeSizeFunc
       
        res = dict()
        for n in self.nx_graph:
            # Grösse bestimmen
            v1 = sizeFunc(NxNodeWrapper(self.nx_graph, n))
            
            # Skalieren
            if (hasattr(self, 'nodeSizeScale')) == False:
                scale = lambda s: s
            else:
                scale = self.nodeSizeScale
            res[n] = scale(v1)
        
        # Normalisieren der Grössen
        # https://en.wikipedia.org/wiki/Feature_scaling
        # TODO: Funktion drauflegen? (z.B. Log)
        return NetViz.normalizeMap(res, self.nodeSizeMin, self.nodeSizeMax)
        
    def setEdgeLayout(self, layout):
        """Sets the Layout of drawing the edges"""
        self.edgeLayout = layout
        return self
    
    def setEdgeWidth(self, func):
        """Set a lambda-Expression for computing the width of an edge."""
        self.edgeWidthFunc = func
        return self
        
    def _computeEdgeWidth(self):
        if hasattr(self, 'edgeWidthFunc') == False:
            # Default-Grösse
            f = lambda e: 0.1
        else: 
            f = self.edgeWidthFunc
       
        res = dict()
        for (u, v, ddict) in self.nx_graph.edges(data=True):
            res[(u, v)] = f(NxEdgeWrapper(self.nx_graph, u, v, ddict))
        return res
     
    def setEdgeColor(self, func):
        """Set a lambda-Expression for computing the rgba-color of an edge."""
        self.edgeColorFunc = func
        return self 
    
    def setEdgeAlpha(self, func):
        """Set a lambda-Expression for computing the Alpha-Color of an edge."""
        self.edgeAlphaFunc = func
        return self
        
    def _computeEdgeColors(self):
        if hasattr(self, 'edgeColorFunc') == False:
            # Default-Farbe
            f = lambda e: 'grey'
        else: 
            f = self.edgeColorFunc
       
        res = dict()
        for (u, v, ddict) in self.nx_graph.edges(data=True):
            res[(u, v)] = f(NxEdgeWrapper(self.nx_graph, u, v, ddict))
        return res
        
    def _computeEdgeAlpha(self):
        if hasattr(self, 'edgeAlphaFunc') == False:
            f = lambda e: 0.25
        else: 
            f = self.edgeAlphaFunc

        res = dict()
        for (u, v, ddict) in self.nx_graph.edges(data=True):
            res[(u, v)] = f(NxEdgeWrapper(self.nx_graph, u, v, ddict))
        return res  
    
    @staticmethod
    def normalizeMap(data: dict, minimum: int, maximum: int):
        """Normalizes the values in the given dict and remaps them to
           to a new dictionary with values between 'min' and 'max'.
           
        Returns: a new dictionary with the mapped values. 
        """
        # Normalisieren der Grössen
        # https://en.wikipedia.org/wiki/Feature_scaling
        
        _min = min(data.values())
        _max = max(data.values())
        
        if _min == _max:
            _maximum = maximum + 1 # div by zero vermeiden
        
        #self.logger.debug("Rescale: min: " + str(_min) + ", max: " + str(_max))
        res = dict()
        for key in data.keys():
            size = data[key]
            
            res[key] = minimum + \
                (((size - _min) * (maximum - minimum)) / \
                (_max - _min)) 
            
        #self.logger.debug("Rescaled sizes: " + str(res.values()))
        return res
        
        
    @abstractmethod
    def plot(self, path: str):
        pass
        
    @staticmethod
    def getInstance(graph):
        """Returns a new instance of the 'default'-NetViz implementation 
        prepared for rendering the given Graph.
        
        Arguments: 
        graph: an instance of a GraphModel or an NetworkX-Graph. 
        
        """ 
        logger = logging.getLogger("NetViz")
        
        theGraph = None
        if isinstance(graph, GraphModel):
            logger.warn("Using a directed version of the MultiDiGraph. Possible information loss!")
            nx_graph = graph.asMultiDiGraph()
            theGraph = nx.DiGraph(nx_graph)
        elif isinstance(graph, nx.Graph):
            theGraph = graph    
        else:
            raise ValueError("Only GraphModel- or nx.Graph instances are accepted.")
        
        return NetgraphNetViz(theGraph)
        
class NxNodeWrapper:
    """A simple wrapper for a NetworkX-Node, used as argument in lambda-callbacks"""
    
    def __init__(self, nx_graph: nx.Graph, nx_node):
        self.nx_graph = nx_graph;
        self.nx_node = nx_node
    
    def get(self, name: str):
        """Return the property with the 'name' of this node"""
        return self.nx_graph.nodes[self.nx_node].get(name)
        
    def degree(self): 
        return self.nx_graph.degree(self.nx_node)
    
    def in_degree(self):
        return self.nx_graph.in_degree(self.nx_node)
        
    def out_degree(self):
        return self.nx_graph.out_degree(self.nx_node)
    

class NxEdgeWrapper:
    """A simple wrapper for a NetworkX-Edge"""
    
    def __init__(self, nx_graph: nx.Graph, u, v, ddict):
        self.nx_graph = nx_graph;
        self.u = u
        self.v = v
        self.ddict = ddict
    
    def get(self, name: str):
        """Return the property with the 'name' of this edge"""
        return None
        #return self.nx_graph.nodes[self.nx_node].get(name)
    
    def getFrom(self):
        return NxNodeWrapper(self.nx_graph, self.u)
        
    def getTo(self):
        return NxNodeWrapper(self.nx_graph, self.v)
    
class NetgraphNetViz(NetViz):
    
    def _fixLabels(self, plotter: Graph):
        sizes = self._computeNodeSizes()
        fontSizes = NetViz.normalizeMap(sizes, 
            self.nodeLabelMinSize, 
            self.nodeLabelMaxSize)
            
        for n in self.nx_graph: 
            label_artist = plotter.node_label_artists.get(n)
            if label_artist != None:
                label_artist.set_size(fontSizes.get(n))


    def plot(self, path: str): 
        self.logger.info("Plotting " + str(self.nx_graph) + " to " + path + "...")
        
        fig, ax = plt.subplots()
        fig.set_size_inches(self.figsize[0], self.figsize[1])
        
        
        # see: https://netgraph.readthedocs.io/en/latest/graph_classes.html#netgraph.Graph
        plotter = Graph(self.nx_graph,
            node_layout = self._getNodePositions(),
            node_size = self._computeNodeSizes(),
            node_color = self._computeNodeColors(),
            node_edge_width = 0,
            node_edge_color = "red",
            node_labels = self._getNodeLabels(),
            #node_label_fontdict = SEE_BELOW,
            #node_label_offset = -0.3,
            node_shape = 'o', # https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
            edge_width = self._computeEdgeWidth(),
            edge_color = self._computeEdgeColors(),
            edge_alpha = self._computeEdgeAlpha(),
            edge_layout = self.edgeLayout,  
            arrows=True)
        
        # Labels anpassen
        self._fixLabels(plotter)
             
        fig.canvas.draw() # force redraw to display changes
        fig.savefig(path, dpi=300)  
         
        self.logger.info("Plotting to " + path + " finished.")     

        
class NetworkxNetViz(NetViz): 

    def plot(self, path: str):
        fig, ax = plt.subplots()
        fig.set_size_inches(self.figsize[0], self.figsize[1])
        
        pos = self._getNodePositions()
        sizes = list(self._computeNodeSizes().values())
        
        #print("sizes: " + str(sizes))
        
         # Nodes
        nx.draw_networkx_nodes(
            self.nx_graph, 
            pos, 
            node_size = sizes, 
            node_color = list(self._computeNodeColors().values()), 
            alpha = None)
        
        # Edges
        edgeWidths = self._computeEdgeWidth()
        #print("edgeWidth: " + str(edgeWidths))
        nx.draw_networkx_edges(
            self.nx_graph, 
            pos, 
            connectionstyle='arc3,rad=0.1',
            arrowsize = 5,
            node_size = sizes,
            alpha = None, 
            width = list(edgeWidths.values()), 
            edge_color="m")
        
        # Labels
        #label_options = {"ec": "k", "fc": "white", "alpha": 0.7}
        nx.draw_networkx_labels(
            self.nx_graph, 
            pos, 
            font_size=10, 
            verticalalignment='center')
            
        fig.canvas.draw() # force redraw to display changes
        ax.set_axis_off()
        fig.savefig(path, dpi=300)     

    