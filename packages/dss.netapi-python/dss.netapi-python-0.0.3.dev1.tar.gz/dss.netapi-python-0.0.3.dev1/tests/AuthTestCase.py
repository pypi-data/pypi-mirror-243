import unittest

from context import *
import networkx

class AuthTestCase(unittest.TestCase): 
    
    def testReadGraph(self):
        """Tests the configuration of a NetAPIClient via a config-file.
        
        Not included in AllTests.py as it depends on a local config
        """
        client = NetAPIClient.fromConfig("default")
         
        """Verifies the (authenticated) reading of the MiniGraph.dgs"""
        req = GraphQueryRequest()\
            .setSource("InputStreamReplayToSource", "MiniGraph.dgs")

        res = client.query(req);

        #print("res:" + str(res))
        
        graphModel = res.getGraphModel()
        
        graph = graphModel.asMultiDiGraph()