import unittest
from networkx.classes.multidigraph import MultiDiGraph

from context import *

#
# Testet den SimpleTestGraph
# 
def queryEdgeAttrNX(nxG, fromNode, toNode,  attr, val, directed=True, 
                    print_output=False):
        """ Tested ob eine Tie zwischen fromNode und toNode ist, mit
        der Eigenschaft attr und dem Wert val """
        # TO DO: In eigenen networkx Wrapper erstellen (Fassade). 
        #attr: the edge attribute. A string
        #val: the value of the attribute
        if directed == True:
            out = ((u,v) for u,v,d in nxG.edges(data=True) if 
                   (d[attr]==val) and ((u==fromNode) and (v==toNode)))
        else:
            out = ((u,v) for u,v,d in nxG.edges(data=True) if 
                   (d[attr]==val) and ((u==fromNode) and (v==toNode) or
                                       (v==fromNode) and (u==toNode)))
        if print_output:
            return(list(out))
        else:
           if(len(list(out))) > 0:
               return(True)
           else:
               return(False)

    
class SimpleTestGraphTestCase(unittest.TestCase): 
    
    def setUp(self):
         # Init Client
         self.client = NetAPIClient("http://localhost:8080/")
 

 
    def testSimpleRead(self):
        """Keine Aggregation, kein Tagging, keine Selektion"""
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "SimpleTestGraph.dgs")

        res = self.client.query(req)
        
        graphModel = res.getGraphModel()
        #print("graphModel: " + graphModel.toJSON())
        
        
        graph = graphModel.asMultiDiGraph()
        
        assert isinstance(graph, MultiDiGraph)
        
        #print("Graph: " + str(graph))
        #print("edges: " + str(graph.edges))
        
        assert len(graph.nodes) == 6
        assert len(graph.edges) == 8
        
        #print("graph.nodes.items():")
        #for n in graph.nodes.items():
        #    print(n)
        
        #print("graph.nodes.values():")
        #for n in graph.nodes.values():
        #    print(n)
            
        graph2 = graphModel.asMultiDiGraph(lambda n : n == "A")
        #print("filtered graph: " + str(graph2))
        
    def testTagger(self):
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "SimpleTestGraph.dgs")\
            .addTagger(Algo("EgoNetGraphTagger", {
                "startNodes": "id='A'",
                "edges": "attributes.type='a'", 
                "depth": 1, 
                "attributeName": "egoA"}))

        res = self.client.query(req)
        
        graph = res.getGraphModel().asMultiDiGraph()
        
        #print("Graph: " + str(graph))
            
        assert len(graph.nodes) == 6
        assert len(graph.edges) == 8
        
        assert graph.nodes["A"]["egoA"] == True
        assert graph.nodes["B"]["egoA"] == True
        assert graph.nodes["E"]["egoA"] == True
        
        # Zugriff auf AssociativeArray mit .get und default-Wert (hier None)
        assert graph.nodes["D"].get("egoA") == None
        
    def testSelection(self):
        """Tests the Selection-Feature: Selects A and B"""
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "SimpleTestGraph.dgs")\
            .setSelection(Selection()\
                .setNodePredicate("id='A' or id='B'")\
            )
            
        res = self.client.query(req)
        
        graphModel = res.getGraphModel()
        assert len(graphModel.getNodes()) == 2
        
        graph = graphModel.asMultiDiGraph()
        #print(graph)
    
        
    def testAggregator(self):
        """Tests the Aggregation-Feature: aggregates on edges of type b"""
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "SimpleTestGraph.dgs")\
            .setAggregator(Algo("EgoAggregator", {
                "edgePredicate": "attributes.type='b'"
            }))
            
        res = self.client.query(req)
        
        graph = res.getGraphModel().asMultiDiGraph()
        
        #print(graph)
        #print(graph.edges.items())
        
        #print("graph.nodes.items():")
        #for n in graph.nodes.items():
        #    print(n)
            
        #print("graph.nodes.edges():")
        #for e in graph.edges.items():
        #    print(e)
            
            
        
    def testMultiDiGraph(self):
        """Tests the MultiDiGraph function - SECONDARY"""
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "SimpleTestGraph.dgs")
        res = self.client.query(req)
        graphModel = res.getGraphModel()
        graph = graphModel.asMultiDiGraph()
        #1.) Test if there are edges between the according nodes
        # WARNING: in directed graphs out ties count as neighbors
        # So if A--> B then B is a neighbor of A, but not vice versa
        assert "B" in list(graph.neighbors("A"))
        assert len(list(graph.neighbors("A")))  == 1
        #
        assert "D" in list(graph.neighbors("B"))
        assert len(list(graph.neighbors("B")))  == 1
        #
        assert "D" in list(graph.neighbors("C"))
        assert len(list(graph.neighbors("C")))  == 1
        #
        assert set(["C","B"]).issubset(set(list(graph.neighbors("D"))))
        assert len(list(graph.neighbors("D")))  == 2
        #
        assert "A" in list(graph.neighbors("E"))
        assert len(list(graph.neighbors("E")))  == 1 
        #
        #2.) Undirected Edges of type c should be transformed to two directed
        assert queryEdgeAttrNX(graph,"B", "D", "type", "c", True) == True   
        assert queryEdgeAttrNX(graph,"D", "B", "type", "c", True) == True   
        assert queryEdgeAttrNX(graph,"D", "C", "type", "c", True) == True   
        assert queryEdgeAttrNX(graph,"C", "D", "type", "c", True) == True
        #3.) Directed Edges of type a should be left as they are
        assert queryEdgeAttrNX(graph,"D", "B", "type", "a", True) == True   
        assert queryEdgeAttrNX(graph,"B", "D", "type", "a", True) == False 
        assert queryEdgeAttrNX(graph,"A", "B", "type", "a", True) == True   
        assert queryEdgeAttrNX(graph,"B", "A", "type", "a", True) == False
        
        
    def testMultiGraph(self):
        """Tests the MultiGraph function - SECONDARY"""
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "SimpleTestGraph.dgs")
        res = self.client.query(req)
        graphModel = res.getGraphModel()
        #graph = graphModel.asMultiGraph()
        graph = graphModel.asMultiGraph()

        # 
        # Undirected Edges of type c should should be left as they are
        assert queryEdgeAttrNX(graph,"B", "D", "type", "c", False) == True     
        assert queryEdgeAttrNX(graph,"D", "C", "type", "c", False) == True  
        # Directed Edges should be one undirected edge
        assert queryEdgeAttrNX(graph,"D", "B", "type", "a", False) == True   
        assert queryEdgeAttrNX(graph,"B", "D", "type", "a", False) == True   
        assert queryEdgeAttrNX(graph,"A", "B", "type", "a", False) == True   
        assert queryEdgeAttrNX(graph,"B", "A", "type", "a", False) == True   




        