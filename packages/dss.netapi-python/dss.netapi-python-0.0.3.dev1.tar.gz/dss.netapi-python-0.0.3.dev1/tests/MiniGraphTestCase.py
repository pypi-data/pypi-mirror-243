import unittest

from context import *

class MiniGraphTestCase(unittest.TestCase): 
    
    def setUp(self):
         # Init Client
         #self.client = NetAPIClient("http://localhost:8080/")
         self.client = NetAPIClient.fromConfig("qknow-live")

 
    def testMiniGraph(self):
        """Verifies the reading of the MiniGraph.dgs"""
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "MiniGraph.dgs")

        res = self.client.query(req);

        #print("res:" + str(res))
        
        graphModel = res.getGraphModel()
        
        graph = graphModel.asMultiDiGraph()

        #print("Graph: " + str(graph))

        # Tests
        # Edge von 1 => 2
        assert graph.number_of_edges("1","2") == 1
        assert graph.get_edge_data(*("1","4"))[0]["type"] == "legal"
        assert graph.get_edge_data(*("6","9"))[0]["type"] == "interaction"
        assert graph.get_edge_data(*("1","2"))[0]["type"] == "coordinative"
        # print("")
        # 
        #print("Graph Nodes :" + str(graph.nodes))
        #print(graph.get_edge_data(*("6","9")))
        #print(graph.edges(data=True))
        #print(graph.get_edge_data(*("5","2")))

        
    
    def test_1a(self):
        """Aggregation mit EgoAggregator mit Tiefe inf"""
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
            .setAggregator(Algo("EgoAggregator", {
                "edgePredicate": "attributes.type='legal'", 
                "depth": -1
            }))
        res = self.client.query(req)
        graphModel = res.getGraphModel()
        
        #print(graphModel)
        #print(graphModel.getNodes())
       # print(graphModel.getEdges())
        # 
        # Don't use  the networkx methods. GraphModel has its own methods
        #
        # 1.) Tests for amounts of Nodes and Edges
        assert len(graphModel.getNodes()) == 4
        assert len(graphModel.getEdges()) == 3
        # 2.) Tests for specific nodes
        assert graphModel.hasNodesById("1", "2", "3", "9")
        assert not graphModel.hasNodesById("4", "5", "6", "7", "8")
        # 3.) Tests for aggregated nodes
        n1 = graphModel.getNodeById("1").getAttributes()["aggregator_sources"]
        assert set(n1) == set(['1', '4', '5','6'])
        n2 = graphModel.getNodeById("2").getAttributes()["aggregator_sources"]
        assert set(n2) == set(['2', '7'])
        n3 = graphModel.getNodeById("3").getAttributes()["aggregator_sources"]
        assert set(n3) == set(['3', '8'])
        #
        # 
        # 4.) Tests for specific ties
        edges12 = graphModel.getEdgesBetween("1", "2")
        assert len(edges12) == 2 
        # 
        assert len(graphModel.getEdgesBetween("1", "2",
                                    types = {EdgeType.UNDIRECTED },
                                        f = lambda e: e.getAttribute("type") 
                                        == "coordinative" ) ) == 1
        assert len(graphModel.getEdgesBetween("1", "2",
                                    types = {EdgeType.UNDIRECTED },
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        assert len(graphModel.getEdgesBetween("1", "9",
                                    types = {EdgeType.UNDIRECTED },
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        
        assert not graphModel.hasEdgeBetween("4", "7") 
        assert not graphModel.hasEdgeBetween("4", "1") 
        assert not graphModel.hasEdgeBetween("4", "2") 
        
        
    
    def test_1b(self):
        """Aggregation mit EgoAggregator, aber nur der Tiefe 1"""
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
            .setAggregator(Algo("EgoAggregator", {
                "edgePredicate": "attributes.type='legal'", 
                "depth": 1 # nur tiefe 1!!
            }))
        res = self.client.query(req)
        graphModel = res.getGraphModel()
        
        #print(graphModel.getNodes())
        
        # 
        assert len(graphModel.getNodes()) == 5
        
        #
        #n1 = graphModel.getNodeById("1").getAttributes()["aggregator_sources"]
        #assert set(n1) == set(['1', '4', '5','6'])
        #n2 = graphModel.getNodeById("2").getAttributes()["aggregator_sources"]
        #assert set(n2) == set(['2', '7'])
        #n3 = graphModel.getNodeById("3").getAttributes()["aggregator_sources"]
        #assert set(n3) == set(['3', '8'])

    
    def test_2(self):
        """Aggregation and selection"""
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
            .setAggregator(Algo("EgoAggregator", {
                "edgePredicate": "attributes.type='legal'",
                "depth": -1
            })).setSelection(Selection()\
                .setNodePredicate("id='1'"))
            
            
        res = self.client.query(req)
        graphModel = res.getGraphModel()
        #print(graphModel.getNodes())
        #print(graphModel.getEdges())
        #
        # 1.) Tests for amounts of nodes and edges
        assert len(graphModel.getNodes()) == 1
        assert len(graphModel.getEdges()) == 0
        # 2.) Tests for specific nodes
        assert graphModel.hasNodesById("1")
        assert not graphModel.hasNodesById("2", "3","4", "5", "6","7", "8", "9")
        # 3.) Tests for aggregated nodes
        n1 = graphModel.getNodeById("1").getAttributes()["aggregator_sources"]
        assert set(n1) == set(['1', '4', '5','6'])
        # 4.) Tests for specific ties

         
        #print(graphModel.getNodes())
        
    def test_3(self):
        """Ego network in combination with aggregation and selection"""
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
            .setAggregator(Algo("EgoAggregator", {
                "edgePredicate": "attributes.type='legal'",
                "depth": -1
            }))\
            .addTagger(Algo("EgoNetGraphTagger", {
                "startNodes": "id='1'",
                "edges": "attributes.type='coordinative'", 
                "depth": -1, 
                "attributeName": "egoA"}))\
            .setSelection(Selection()\
                .setNodePredicate("attributes.egoA=true"))
            
        res = self.client.query(req)
        graphModel = res.getGraphModel()
        #
        #print(graphModel.getNodes())
        #print(graphModel.getEdges())
        #
        #
        # 1.) Tests for amounts of nodes and edges
        assert len(graphModel.getNodes()) == 2
        assert len(graphModel.getEdges()) == 2
        #
        # 2.) Tests for specific nodes
        assert graphModel.hasNodesById("1", "2")
        assert not graphModel.hasNodesById("3","4", "5", "6","7", "8", "9")
        # 3.) Tests for aggregated nodes
        n1 = graphModel.getNodeById("1").getAttributes()["aggregator_sources"]
        assert set(n1) == set(['1', '4', '5','6'])
        n2 = graphModel.getNodeById("2").getAttributes()["aggregator_sources"]
        assert set(n2) == set(['2', '7'])
        # 4.) Tests for specific ties
        assert len(graphModel.getEdgesBetween("1", "2",
                                    types = {EdgeType.UNDIRECTED },
                                        f = lambda e: e.getAttribute("type") 
                                        == "coordinative" ) ) == 1
        assert len(graphModel.getEdgesBetween("1", "2",
                                    types = {EdgeType.UNDIRECTED },
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        assert len(graphModel.getEdgesBetween("1", "9") ) == 0
        

    def test_4(self):
        """Ego network in combination with aggregation and selection"""
        req = GraphQueryRequest()\
                 .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
                 .setAggregator(Algo("EgoAggregator", {
                     "edgePredicate": "attributes.type='legal'",
                     "depth": -1
                 })).addTagger(Algo("EgoNetGraphTagger", {
                     "startNodes": "id='1'",
                     "edges": "attributes.type='coordinative'", 
                     "depth": -1, 
                     "attributeName": "egoA"}))\
                         .setSelection(Selection()\
                                       .setNodePredicate("attributes.egoA=true and id='2'"))
        res = self.client.query(req)
        graphModel = res.getGraphModel()
         #
         #print(graphModel.getNodes())
         #print(graphModel.getEdges())
         #
         # 1.) Tests for amounts of nodes and edges
        assert len(graphModel.getNodes()) == 1
        assert len(graphModel.getEdges()) == 0
         # 2.) Tests for specific nodes
        assert graphModel.hasNodesById("2")
        assert not graphModel.hasNodesById("1","3","4", "5", "6","7", "8", "9")
         # 3.) Tests for aggregated nodes
        n2 = graphModel.getNodeById("2").getAttributes()["aggregator_sources"]
        assert set(n2) == set(['2', '7'])
        # 4.) Tests for specific ties

    
    def test_5(self):
        """Ego networks of several egos"""
        req = GraphQueryRequest()\
                 .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
                 .addTagger(Algo("EgoNetGraphTagger", {
                     "startNodes": "id='1' or id='2'",
                     "edges": "attributes.type='legal'", 
                     "depth": -1, 
                     "attributeName": "egoA"}))\
                         .setSelection(Selection()\
                                       .setNodePredicate("attributes.egoA=true"))
        res = self.client.query(req)
        graphModel = res.getGraphModel()
        #
        #print(graphModel.getNodes())
        #print(graphModel.getEdges())
        #
        # 1.) Tests for amounts of nodes and edges
        assert len(graphModel.getNodes()) == 6
        assert len(graphModel.getEdges()) == 9
        #
        # 2.) Tests for specific nodes
        assert graphModel.hasNodesById("1","2","4","5","6","7")
        assert not graphModel.hasNodesById("3","8","9")
        # 3.) Tests for aggregated nodes
        #
        # 4.) Tests for specific ties
        assert len(graphModel.getEdgesBetween("1", "4",
                                    types = {EdgeType.DIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "legal" ) ) == 1
        assert len(graphModel.getEdgesBetween("1", "6",
                                    types = {EdgeType.DIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "legal" ) ) == 1
        assert len(graphModel.getEdgesBetween("6", "5",
                                    types = {EdgeType.DIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "legal" ) ) == 1
        assert len(graphModel.getEdgesBetween("2", "7",
                                    types = {EdgeType.DIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "legal" ) ) == 1
        assert len(graphModel.getEdgesBetween("1", "2",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "coordinative" ) ) == 1
        assert len(graphModel.getEdgesBetween("2", "6",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "coordinative" ) ) == 1
        assert len(graphModel.getEdgesBetween("4", "7",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        assert len(graphModel.getEdgesBetween("4", "5",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        assert len(graphModel.getEdgesBetween("7", "6",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1


   
         

    def test_6(self):
        """Ego networks over interaction ties"""
        req = GraphQueryRequest()\
                .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
                .addTagger(Algo("EgoNetGraphTagger", {
                    "startNodes": "id='6'",
                    "edges": "attributes.type='interaction'", 
                    "depth": 2, 
                    "attributeName": "egoA"})).setSelection(Selection()\
                              .setNodePredicate("attributes.egoA=true"))
                    
                
        res = self.client.query(req);
        graphModel = res.getGraphModel()
        #graph = graphModel.asMultiDiGraph()
        #
        # 1.) Tests for amounts of nodes and edges
        assert len(graphModel.getNodes()) == 4
        assert len(graphModel.getEdges()) == 3
        # 2.) Tests for specific nodes
        assert graphModel.hasNodesById("4","6","7","9")
        assert not graphModel.hasNodesById("1","2","3","5","8")
        # 3.) Tests for aggregated nodes
        #
        # 4.) Tests for specific ties
        assert len(graphModel.getEdgesBetween("4", "7",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        assert len(graphModel.getEdgesBetween("7", "6",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        assert len(graphModel.getEdgesBetween("6", "9",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        
        
    def test_7(self):
        """ Several different ego networks """
        req = GraphQueryRequest()\
             .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
             .addTagger(Algo("EgoNetGraphTagger", {
                 "startNodes": "id='2'",
                 "edges": "attributes.type='legal'", 
                 "depth": -1, 
                 "attributeName": "egoA"}))\
                 .addTagger(Algo("EgoNetGraphTagger", {
                     "startNodes": "id='2'",
                     "edges": "attributes.type='interaction'", 
                     "depth": 2, 
                     "attributeName": "egoB"}))\
                     .setSelection(Selection()\
                           .setNodePredicate("attributes.egoA=true or \
                                             attributes.egoB=true"))
                 
        res = self.client.query(req);
        graphModel = res.getGraphModel()
        #print(graphModel.getNodes())
        #print(graphModel.getEdges())
        #
        # 1.) Tests for amounts of nodes and edges
        assert len(graphModel.getNodes()) == 2    
        assert len(graphModel.getEdges()) == 1
        # 2.) Tests for specific nodes
        assert graphModel.hasNodesById("2","7")
        assert not graphModel.hasNodesById("1","3","4","5","6","8","9")
        # 3.) Tests for aggregated nodes
        # 4.) Tests for specific ties
        assert len(graphModel.getEdgesBetween("2", "7",
                                    types = {EdgeType.DIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "legal" ) ) == 1

        
        
    def test_8(self):
        """ Chained tagging """
        req = GraphQueryRequest()\
          .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
          .addTagger(Algo("EgoNetGraphTagger", {
              "startNodes": "id='2'",
              "edges": "attributes.type='legal'", 
              "depth": -1, 
              "attributeName": "egoA"}))\
              .addTagger(Algo("EgoNetGraphTagger", {
                  "startNodes": "attributes.egoA=true",
                  "edges": "attributes.type='interaction'", 
                  "depth": 1, 
                  "attributeName": "egoB"}))\
                  .setSelection(Selection()\
                        .setNodePredicate("attributes.egoB=true"))
              
        res = self.client.query(req);
        graphModel = res.getGraphModel()
        #print(graphModel.getNodes())
        #print(graphModel.getEdges())
        #print(len(graphModel.getNodes()))
        #
        # 1.) Tests for amounts of nodes and edges
        assert len(graphModel.getNodes()) == 4    
        assert len(graphModel.getEdges()) == 4
        # 2.) Tests for specific nodes
        assert graphModel.hasNodesById("2","4","6","7")
        assert not graphModel.hasNodesById("1","3","5","8","9")
        # 3.) Tests for aggregated nodes
        # 4.) Tests for specific ties
        assert len(graphModel.getEdgesBetween("2", "7",
                                    types = {EdgeType.DIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "legal" ) ) == 1
        assert len(graphModel.getEdgesBetween("2", "6",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "coordinative" ) ) == 1
        assert len(graphModel.getEdgesBetween("4", "7",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        assert len(graphModel.getEdgesBetween("7", "6",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
     
 
    def test_9(self):
        """ Selection on node attribute city """
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
               .setSelection(Selection()\
                             .setNodePredicate("attributes.geo='1' or \
                                               attributes.geo='2'" )\
                            .setEdgePredicate("attributes.type='interaction'"))
                            
        res = self.client.query(req);
        graphModel = res.getGraphModel()
        #print(graphModel.getNodes())    
        #print(graphModel.getEdges())
        # 1.) Tests for amounts of nodes and edges
        assert len(graphModel.getNodes()) == 4  
        assert len(graphModel.getEdges()) == 1
        # 2.) Tests for specific nodes
        assert graphModel.hasNodesById("1","2","4","7")
        assert not graphModel.hasNodesById("3","5","6","8","9")
        # 3.) Tests for aggregated nodes
        # 4.) Tests for specific ties
        assert len(graphModel.getEdgesBetween("4", "7",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        
        
    def test_10(self):
        """ Selection on edge attribute subjects """
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
                .setSelection(Selection()\
                 .setEdgePredicate("attributes.subjects CONTAINS ('Biology')"))
                # Does NOT work
                #.setEdgePredicate("attributes.subjects LIKE ('Biology') \
                #                  and attributes.subjects not NULL"))
                #.setEdgePredicate("attributes.subjects IN ('Biology') \
                #                 and attributes.subjects not NULL"))
                                
        res = self.client.query(req);
        graphModel = res.getGraphModel()
        #print(graphModel.getNodes())    
        #print(graphModel.getEdges())
        # 1.) Tests for amounts of nodes and edges
        assert len(graphModel.getNodes()) == 9 
        assert len(graphModel.getEdges()) == 2
        # 2.) Tests for specific nodes
        assert graphModel.hasNodesById("1","2","3","4","5","6","7","8","9")
        # 3.) Tests for aggregated nodes
        # 4.) Tests for specific ties
        #print(graphModel.getAttributeEdges("6","7", "subjects")["i_0706"])
       
        assert len(graphModel.getEdgesBetween("6", "7",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: "Biology" in e.getAttribute("subjects")
                                        )) == 1
        assert len(graphModel.getEdgesBetween("6", "9",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: "Biology" in e.getAttribute("subjects")
                                        )) == 1

    def test_11(self):
        """ Tests node attribute level aggregation """
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
            .setAggregator(Algo("NodeAttributeAggregator", {
                    "attribute": 'geo' }))\
                .setSelection(Selection()\
                .setEdgePredicate("attributes.type='interaction'"))
                                    
        res = self.client.query(req);
        #print(res.getResult())
        graphModel = res.getGraphModel()

        
        # neue lesbarere Version der String-Ausgabe eines Graphen. 
        #print(graphModel.toJSON()) 
        #print(graphModel.getNodes())    
        #print(graphModel.getEdges())
        
        #assert False
        #@Pavel: Test werden evtl anders benannt, je nachdem was unsere
        # labelling Strategie bei der Aggregation ist.
        #
        # 1.) Tests for amounts of nodes and edges
        assert len(graphModel.getNodes()) == 5
        assert len(graphModel.getEdges()) == 4
        # 2.) Tests for specific nodes
        # WARNING: Nodes are city names
        assert graphModel.hasNodesById("1","2","3","4","NULL")
        assert not graphModel.hasNodesById('5','6','7', '8', '9')
        # 3.) Tests for aggregated nodes
        #print(graphModel.getNodeById("1").getAttributes()["aggregator_sources"])
        n1 = graphModel.getNodeById("1").getAttributes()["aggregator_sources"]
        assert set(n1) == set(['2', '4'])
        n2 = graphModel.getNodeById("2").getAttributes()["aggregator_sources"]
        assert set(n2) == set(['1', '7'])
        n3 = graphModel.getNodeById("3").getAttributes()["aggregator_sources"]
        assert set(n3) == set(['3','6'])
        n4 = graphModel.getNodeById("4").getAttributes()["aggregator_sources"]
        assert set(n4) == set(['5'])
        n4 = graphModel.getNodeById("NULL").getAttributes()["aggregator_sources"]
        assert set(n4) == set(['8','9'])
        
        # 4.) Tests for specific ties
        # WARNING: These are cities
        assert len(graphModel.getEdgesBetween("1", "2",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        assert len(graphModel.getEdgesBetween("2", "3",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        assert len(graphModel.getEdgesBetween("3", "NULL",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        assert len(graphModel.getEdgesBetween("1", "4",
                                    types = {EdgeType.UNDIRECTED},
                                        f = lambda e: e.getAttribute("type") 
                                        == "interaction" ) ) == 1
        
        
    def test_12(self):
            """ Tests node attribute level aggregation + ego network"""
            req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "MiniGraph.dgs")\
                .addTagger(Algo("EgoNetGraphTagger", {
                    "startNodes": "attributes.geo ='1' ",
                    "edges": "attributes.type='interaction'", 
                    "depth": 1, 
                    "attributeName": "egoGeo"}))\
                    .setSelection(Selection()\
                          .setNodePredicate("attributes.egoGeo = true"))
            
            res = self.client.query(req);
            graphModel = res.getGraphModel()
            #
            #print(graphModel.hasNodesById("999"))
            #print(graphModel.hasNodesById("2","999"))
            #print(graphModel.hasNodesById("999", "2"))
            #Tests
            assert graphModel.hasNodesById("2", "4","5", "7")
            assert len(graphModel.getNodes())==4

