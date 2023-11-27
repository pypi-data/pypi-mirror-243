import re
import logging
import json
from enum import Enum
import warnings

import networkx as nx
from networkx.classes.multidigraph import MultiDiGraph
from networkx.classes.function import set_node_attributes
from networkx.classes.graphviews import subgraph_view
from networkx.classes.filters import no_filter

class EdgeType(Enum):
    DIRECTED = 'D'
    UNDIRECTED = 'U'

class GraphModel:
    """A generic model of a graph with directed *and* undirected edges and 
       multiple edges between nodes.
       
       It is used as an intermediary data-structure and provides factory-methods 
       for creating networkx-views.
       
       Algorithms should seriously use the networkx-view as this class is 
       merely designed for transfering and holding the orginal data.
    """
    def __init__(self):
        self.nodes = {}
        self.edges = {}
    
    def createNode(self, nodeId: str):
        node = Node(self, nodeId)
        self.nodes[nodeId] = node
        return node
    
    def getNodes(self):
        """Returns the set of Node objects"""
        return set(self.nodes.values())
    
    def getNodeById(self, id: str): 
        """Returns a node by id. Returns None if it doesn't exist """
        return self.nodes.get(id)        
    
    def hasNodesById(self, *args):
        """Returns true if all *args are in the nodes """
        #for a in args:
        #    if self.getNodeById(a) == None:
        #        return False
        #    else:
        #        return True
        for a in args:
            if self.getNodeById(a) == None:
                return False
        return True
    
    def createEdge(self, edgeId: str, fromNodeId: str, toNodeId: str):
        """Adds an (directed) Edge between the specified nodes"""
        edge = Edge(self, edgeId, fromNodeId, toNodeId)
        self.edges[edgeId] = edge
        return edge
    
    def getEdges(self):
        return set(self.edges.values())
    
    def getEdgeById(self, id: str):
        return self.edges[id]
    
    def getEdgesBetween(self, fromNodeId: str, toNodeId: str, 
                        types = { EdgeType.DIRECTED, EdgeType.UNDIRECTED }, 
                        f = lambda e: True):
        """
        Returns a set of the edges between the specified nodes which satisfy
        certain conditions
        
        Parameters
        ----------
        fromNodeId: str
            The ID of the node starting the edge.
        toNodeId: str
            The ID of the node to the end of the edge.
        type: set of EdgeTypes
            A set of of EdgeTypes which should be considered
        f: callable(boolean)
            A predicate on edges which can be used to filter resulting edges
        """
        
        res = set()
        # TODO: das ist fürchterlich ineffizient
        # Doch eine Adjazenzliste einführen? 
        for e in self.getEdges():
            if EdgeType.DIRECTED in types:
                if e.isDirected(): 
                    if e.getFromNodeId() == fromNodeId and e.getToNodeId() == toNodeId:
                            res.add(e)
            
            if EdgeType.UNDIRECTED in types:
                if e.isDirected() == False: 
                    if (e.getFromNodeId() == fromNodeId and e.getToNodeId() == toNodeId)\
                        or (e.getFromNodeId() == toNodeId and e.getToNodeId() == fromNodeId):
                            res.add(e)
        
        # filter anwenden
        res = set(filter(f, res))
        
        return res
    
    def getAttributeEdges(self, fromNodeId: str, toNodeId: str, edge_attribute: str):
        warnings.warn(
            "getAttributeEdges is deprecated, use getEdgesBetween instead",
            DeprecationWarning
        )
        res = {}
        edges = self.getEdgesBetween(fromNodeId, toNodeId)
        for e in edges:
            res[e.id] = e.getAttributes()[edge_attribute]
        return res
    
    
    def hasEdgeBetween(self, fromNodeId: str, toNodeId: str) -> bool:
        """Returns True if an edge exists between the two specified nodes"""
        edges = self.getEdgesBetween(fromNodeId, toNodeId)
        return len(edges) > 0
    
    def toJSON(self):
        return(json.dumps(self, default=self.__jsoncallback, indent=4))
    
    def __jsoncallback(self, o):
        tmp = o.__dict__
        tmp.pop("graph", None)
        return tmp
    
    def __repr__(self):
        return "{ type: " + type(self).__name__ + \
            ", nodes: [" + str(self.getNodes()) + "]}" 
           # ", edges: [" + str(self.getEdges()) + "]}"
            
    def asMultiDiGraph(self, node_filter=no_filter, edge_filter=no_filter):
        """Returns a *copy* of this GraphModel as a NetworkX-MultiDiGraph.
        
        Nodes are created with its ID and an attribute "node" with its original
        Node-Object from this GraphModel. 
        
        Edges are created between the IDs and an attribute "edge" with its original
        Edge-Object from this GraphModel.
        
        Any undirected edges are silently converted to two directed edges.
        """
        res = MultiDiGraph()
        
        # Copy nodes and their attributes
        for n in self.getNodes():
            # ID als Key und Node als "Attribute"
            res.add_node(n.getId(), **n.getAttributes())
            
            #nx.set_node_attributes(res, { n.getId(): n.getAttributes() })
            
        # Copy edges and their attributes
        for e in self.getEdges():
            res.add_edge(e.getFromNodeId(), e.getToNodeId(), 
                key=None, **e.getAttributes())
            
            if (e.isDirected() == False):
                res.add_edge(e.getToNodeId(), e.getFromNodeId(), 
                    key=None, **e.getAttributes())

        return subgraph_view(res, filter_node = node_filter, filter_edge = edge_filter)
    
    def asMultiGraph(self, node_filter=no_filter, edge_filter=no_filter):
        """Returns a *copy* of this GraphModel as NetworkX-MultiGraph.
        
        Any directed edges are silently converted to one undirected edge.
        """
        res = self.asMultiDiGraph(node_filter=no_filter, edge_filter=no_filter)\
            .to_undirected()
        return res
        
    @staticmethod
    def parseFromDGS(content: str):
        """Parses a DGS-Formatted string and returns a corresponsing GraphModel"""
        logger = logging.getLogger("NetAPIGraph")
        
        res = GraphModel()
        
        for line in content.splitlines():
            logger.debug("line: " + line)
            
            if (line.startswith("DGS") or 
                line.startswith("null") or 
                line.startswith("#")):
                continue
            
            # Helper: https://regex101.com/
            m = re.search('(\w\w)\s+\"(.*?)\"', line)
            if (m != None):
                command = m.group(1)
                id = m.group(2)
            
                logger.debug("=> command: " + command + ", id: " + id)
                
                if command == "an":
                    res.createNode(id)
                    
                elif command == "ae":
                    ae = re.search(
                        "(\w\w)\s+\"(.+?)\"\s+\"(.*?)\"(.*)\"(.*?)\"",
                        line)
                    if (ae != None):
                        aNodeId = ae.group(3)
                        direction = ae.group(4).strip()
                        bNodeId = ae.group(5)
                        
                        if direction == ">": 
                            edge = res.createEdge(id, aNodeId, bNodeId)
                        elif direction == "<": 
                            edge = res.createEdge(id, bNodeId, aNodeId)
                        else:
                            edge = res.createEdge(id, bNodeId, aNodeId)
                            edge.setDirected(False)
                        
                    else:
                        raise RuntimeError("Could not parse ae-Statement: " + line)    
                elif command == "cn" or command == "ce":
                    if command == "cn": 
                        element = res.getNodeById(id)
                    else: 
                        element = res.getEdgeById(id)
                    
                    #regexA = "(\w\w)\s+\"(.+?)\"\s+\"(\w*?)\":(.*)"
                    regexB = "(\w\w)\s+\"(.+?)\"\s+\"(.*?)\":(.*)"
                    change = re.search(regexB, line)
                    if (change != None):
                        attr = change.group(3)
                        value = change.group(4)
                        logger.debug("==> attr: " + attr + " => " + value)
                        
                       
                        if value.startswith("\""): 
                             # String
                            value = value[1:-1]
                        elif value == "true" or value == "false":
                            # Boolean
                            value = (value == "true")
                        elif value.startswith("{") and value.endswith("}"):
                            # Array
                            value = json.loads("[" + value[1:-1] + "]")
                        else: 
                            # Float/Number 
                            value = float(value)
                            
                        element.setAttribute(attr, value)
                    else: 
                        raise RuntimeError("Could not parse cn/ce-Statement: " + line)    
                else:
                    logger.error("Command " + command + " nicht implementiert!")
        
        return res

class Element:
    def __init__(self, graph, id):
        self.graph = graph
        self.id = id
        self.attributes = { }

    def getId(self):
        return self.id
    
    def getGraph(self):
        return self.graph
    
    def setAttribute(self, name: str, value):
        self.attributes[name] = value
        
    def getAttribute(self, name):
        """Return the value of the specified attribute"""
        return self.getAttributes().get(name, None)
    
    def getAttributes(self):
        self.attributes.update({ "id": self.id})
        return self.attributes
    
    def __key(self):
        return (str(type(self)), self.id)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Element):
            return self.__key() == other.__key()
        return NotImplemented
    
    def __repr__(self):
        return "{ type: " + type(self).__name__ + ", " + str(self.attributes) + "}"

class Node(Element):
    def __init__(self, graph, id):
        super(Node, self).__init__(graph, id)
    
    
class Edge(Element): 
    def __init__(self, graph, id, fromNodeId, toNodeId):
        super(Edge, self).__init__(graph, id)
        self.directed = True
        self.fromNodeId = fromNodeId
        self.toNodeId = toNodeId
        
    def setDirected(self, directed: bool): 
        self.directed = directed
        
    def isDirected(self) -> bool:
        return self.directed
        
    def getFromNodeId(self):
        return self.fromNodeId
    
    def getToNodeId(self):
        return self.toNodeId
        
    def __repr__(self):
        return "{ type: " + type(self).__name__ + \
            ", from:" + self.fromNodeId + ", to: " + self.toNodeId +\
            ", directed: " + str(self.directed) + ", " + str(self.attributes) + "}"
        