import unittest

from context import *
import networkx
from _ast import Or

class GraphTestCase(unittest.TestCase): 
    
    def setUp(self):
         self.client = NetAPIClient("http://localhost:8080/")
         pass
 
    def testABC(self):
        """A simple Graph with a circle A, B, C"""
        
        graph = GraphModel()
        a = graph.createNode("A")
        a.setAttribute("title", "Node - A")
        a.setAttribute("boolean", True)
        
        # Neu auslesen - Attribute prüfen
        a0 = graph.getNodeById("A")
        assert a0 != None
        assert a0.getAttribute("title") == "Node - A"
        assert a0.getAttribute("boolean") == True
        
        b = graph.createNode("B")
        c = graph.createNode("C")
        
        assert len(graph.getNodes()) == 3
        
        print(graph.getNodes())
        
        ab = graph.createEdge("AB", a.getId(), b.getId())
        bc = graph.createEdge("BC", b.getId(), c.getId())
        ca = graph.createEdge("CA", c.getId(), a.getId())
        
        print(graph.getEdges())
        assert len(graph.getEdges()) == 3
        
        # Attribute Edges
        ca.setAttribute("type", "c")
        
        ca0 = ca.graph.getEdgeById("CA")
        assert ca0.getAttribute("type") == "c"
        
    def testReadFromDGS(self):
        """Reading a GraphModel from DGS-format"""
        
        self.client = NetAPIClient("http://localhost:8080/")
        req = GraphQueryRequest()\
            .setSourceObject(
                Source("InputStreamReplayToSource", "SimpleTestGraph.dgs")
                    .setArgs(limit = 1000, another = "A")
            )
        res = self.client.query(req)
        
        graphModel = res.getGraphModel()
        
        print(graphModel)
        
        assert len(graphModel.getNodes()) == 6
        assert len(graphModel.getEdges()) == 6
        
        edges = graphModel.getEdgesBetween("A", "B")
        for e in edges: 
            assert e.getAttribute("type") == "a" or e.getAttribute("type") == "b"
        
        # Attribute Datentypen: 
        number = graphModel.getNodeById("A").getAttribute("number")
        print("number:" + str(number))
        assert number == 33.3
        
        # Listen
        listOfStrings = graphModel.getNodeById("A").getAttribute("listOfStrings")
        print("listOfStrings: " + str(listOfStrings))
        assert listOfStrings == ["A", "B", "C"]
        
        listOfNumbers = graphModel.getNodeById("A").getAttribute("listOfNumbers")
        print("listOfNumbers: " + str(listOfNumbers))
        assert listOfNumbers == [1, 2, 3]
        
        # boolean
        booleanValue = graphModel.getNodeById("A").getAttribute("boolean")
        print("boolean: " + str(booleanValue))
        assert booleanValue == True
        
        edges = graphModel.getEdgesBetween(
            "A", "B", f = lambda e: e.getAttribute("type") == "a")
        print("edges: " + str(edges))
        assert(len(edges) == 1)
        
        edges = graphModel.getEdgesBetween("A", "B", 
            types = { EdgeType.UNDIRECTED }, 
            f = lambda e: e.getAttribute("type") == "a")
        print("edges2: " + str(edges))
        assert(len(edges) == 0)
        
        
    def testException(self):
        """Verifies an requests which induces an error on the server side"""
        
        self.client = NetAPIClient("http://localhost:8080/")
        req = GraphQueryRequest()\
            .setSourceObject(
                Source("InputStreamReplayToSource", "DoesNotExistGraph.dgs")
            )
           
        try: 
            res = self.client.query(req)
            assert(False)
        except Exception as e:
            assert(isinstance(e, GraphQueryException))
    
    
    def testNetworkX(self):
        """Verifies the NetworkX-Version of the SimpleTestGraph.dgs"""
        
        self.client = NetAPIClient("http://localhost:8080/")
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "SimpleTestGraph.dgs")
        res = self.client.query(req)
        
        graphModel = res.getGraphModel()
        
        graph = graphModel.asMultiDiGraph()
        
        print(graph)
        
        print("graph.nodes.items():")
        for n in graph.nodes.items():
            print(n)
        
        print("graph.edges.items():")
        for n in graph.edges.values():
            print(n)
            
        assert graph.nodes["A"]["label"] == "Node - A"  
        assert graph.nodes["A"]["id"] == "A"  