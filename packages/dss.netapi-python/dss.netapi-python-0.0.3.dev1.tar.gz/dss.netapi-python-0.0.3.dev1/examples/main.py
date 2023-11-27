from netapi import *
import json 
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
#print("File      Path:", Path(__file__).absolute())

client = NetAPIClient("http://localhost:8080/")

req = GraphQueryRequest()\
    .setFormat("gml")\
    .setSource("InputStreamReplayToSource","MiniGraph.dgs")
    # SimpleTestGraph.dgs # MiniGraph.dgs

res = client.query(req);
#print("Graph: " + (str(res.getGraph())))

nx.draw(res.getGraph(), with_labels = True)
plt.savefig("./plots/" + "MiniGraph.png")

#print("res:" + str(res))
#print("WOW")
#print(type(res.text))
#print(json.loads(res.text)["result"])
#nx.read_gexf(json.loads(res.text)["result"])