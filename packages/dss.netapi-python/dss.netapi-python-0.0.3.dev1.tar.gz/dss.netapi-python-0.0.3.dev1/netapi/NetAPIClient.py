import requests
import json
import configparser
import os.path
from os.path import expanduser
import networkx as nx
import logging

from .NetAPIGraph import *

class NetAPIClient:
    
    @staticmethod
    def fromConfig(profile = 'default'):
        logger = logging.getLogger('NetAPIClient')
        
        # Konfiguration einlesen
        config = configparser.ConfigParser()
        configPath = expanduser("~/.netapi/config")
        if os.path.isfile(configPath):
            logger.debug("Using config - " + configPath) 
            config.read(configPath)
        else:
            logger.debug("No config found")
        
        host = config.get(profile, "host", fallback=None)
        if host == None:
            raise NetAPIException(
                "The profile " + profile + " in '" + configPath + 
                "' has no property 'host'.")
         
        token = config.get(profile, "token", fallback=None)
        
        client = NetAPIClient(host)
        client.__setToken(token)
        
        return client
        
    
    def __init__(self, base_url):
        self.base_url = base_url
        
        # base_url *darf nicht* mit / enden...
        if self.base_url.endswith('/'): 
            self.base_url = self.base_url[:-1]
        
        self.final_url = self.base_url + "/netapi/query"
        self.token = None
        
        self.logger = logging.getLogger('NetAPIClient')
        
    def __setToken(self, token):
        self.token = token    
                
    def query(self, graphQueryRequest):
        if not isinstance(graphQueryRequest, GraphQueryRequest):
            raise TypeError("The input is not of type GraphQueryRequest: " + str(type(graphQueryRequest)))
        
        self.logger.debug("sending query: " + graphQueryRequest.toJSON())
        headers = {
            'Content-type': 'application/json', 
        }
       
        # Authentifizierung über Token
        if self.token != None:
            headers['token'] = self.token
        
        self.logger.debug("using url: " + self.final_url)
        self.logger.debug("using headers: " + str(headers))
        
        httpRes = requests.post(
            self.final_url, 
            data = graphQueryRequest.toJSON(), 
            headers=headers)
        httpRes.raise_for_status()
        
        self.logger.debug("httpRes.body: " + httpRes.text)
        
        res = GraphQueryResponse(httpRes)
        
        return(res)


class GraphQueryRequest:
    def __init__(self):
        self.tagger = []
        self.format = "dgs"
        
    def setFormat(self, q_format):
        self.format = q_format
        return(self)
    
    def setSource(self, q_type, q_name):
        self.source = Source(q_type, q_name)
        return(self)
    
    def setSourceObject(self, source):
        self.source = source;
        return(self)
    
    def setAggregator(self, algo):
        self.aggregator = algo
        return self
    
    def addTagger(self, algo):
        # todo: nur Algo-Objekte übergeben!
        self.tagger.append(algo)
        return self
    
    def setSelection(self, selection):
        self.selection = selection
        return self
    
    def toJSON(self):
        return(json.dumps(self, default=lambda o: o.__dict__, indent=4))
        

class Source:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        
    def setArgs(self, **kwargs):
        self.args = kwargs
        return self
    
class Algo:
    def __init__(self, name, args):
        self.name = name
        self.args = args
        
class Selection:
    
    def setNodePredicate(self, nodePredicate: str):
        self.nodePredicate = nodePredicate
        return self
    
    def setEdgePredicate(self, edgePredicate: str):
        self.edgePredicate = edgePredicate
        return self
   
class GraphQueryResponse: 
    def __init__(self, httpResponse):
        self.httpResponse = httpResponse
        
        self.response = json.loads(self.httpResponse.text)
        self.result = self.response["result"];
        
        if self.response["success"] == False:
            raise GraphQueryException(self.response["errorMessage"])
        
    
    def getResult(self):
        """Return the plain text of the "result"-field"""
        return(self.result)

    def getGraphModel(self):
        """Returns the GraphModel transferred with the response"""
        return GraphModel.parseFromDGS(self.getResult())
    
    
class NetAPIException(Exception):
    
    def __init__(self, *args:object)->None:
        Exception.__init__(self, *args)
    
class GraphQueryException(NetAPIException):
    
    def __init__(self, *args:object)->None:
        Exception.__init__(self, *args)
