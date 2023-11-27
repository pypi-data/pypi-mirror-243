import unittest

from context import *
import networkx
from _ast import Or

class QKnowLegacyGraphTestCase(unittest.TestCase):
    """Tests for the QKnowLegacyGraphEventSource.
    
    Works only if the server is started with the qknow-profile    
    """ 
    
    def setUp(self):
         self.client = NetAPIClient("http://localhost:8080/")
         pass
 
    def testRead(self):
        """Reads the complete interaction Graph"""
        req = GraphQueryRequest()\
            .setSource("BeanReplayToSource", "QKnowLegacyGraphEventSource")

        res = self.client.query(req)
        
        graphModel = res.getGraphModel()
        print("graphModel: ", len(graphModel.getNodes()))
        
        assert len(graphModel.getNodes()) > 3300
        
    def testLimit(self):
        """Reads the limited interaction Graph"""
        req = GraphQueryRequest()\
            .setSourceObject(
                Source("BeanReplayToSource", "QKnowLegacyGraphEventSource")
                    .setArgs(limit = 100))

        res = self.client.query(req)
        
        graphModel = res.getGraphModel()
        print("graphModel: ", len(graphModel.getNodes()))
        
        assert len(graphModel.getNodes()) < 500