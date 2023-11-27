from netapi import * #<1>

client = NetAPIClient.fromConfig("default") #<2>

req = GraphQueryRequest()\
      .setSource("InputStreamReplayToSource", "MiniGraph.dgs") #<3>
res = client.query(req) #<4>

graphModel = res.getGraphModel() #<5>
graph = graphModel.asMultiDiGraph() #<6>

print(graph)