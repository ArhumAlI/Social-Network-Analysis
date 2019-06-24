import snap
import matplotlib.pyplot as plt

# Global Variable
betweeness=0
ModularityList=[]
CommunityList=[]
CheckModularity=0

# Load File Data
Graphkarateclub = snap.LoadEdgeList(snap.PUNGraph,"karateclub.txt",0,1)
GraphkarateclubMaintainForDeleteEdges = snap.LoadEdgeList(snap.PUNGraph,"karateclub.txt",0,1)

# Display Nodes and Edges of Graph
TotalNumberOfNodes=Graphkarateclub.GetNodes()
TotalBumberOfEdges=Graphkarateclub.GetEdges()
print("Total # of Nodes in Graph %d",TotalNumberOfNodes)
print("Total # of Edges in Graph %d",TotalBumberOfEdges)

# Iterate No. Of Edges time
while GraphkarateclubMaintainForDeleteEdges.GetEdges()!=0:
    betweennessList = []
    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    ''' Compute the edge betweeness of all the edges in the graph '''
    snap.GetBetweennessCentr(GraphkarateclubMaintainForDeleteEdges, Nodes, Edges, 1.0)
    # Prepare BetweenessList Of List
    for edge in Edges:
        betweennessSubList=[edge.GetVal1(), edge.GetVal2(),Edges[edge]]
        betweennessList.append(betweennessSubList)

    # Descending  Order Sort Betweenness and take  highest betweenness
    betweennessList.sort(key=lambda x: x[-1], reverse=True)
    # Remove the edge with highest betweenness
    ''' NOTE: ONLY FIRST ROW USE FOR DELETE EDGES( HIGHEST BETWEENESS )'''
    GraphkarateclubMaintainForDeleteEdges.DelEdge(betweennessList[0][0], betweennessList[0][1])


    '''Compute the modularity of the resultant graph'''
    Components = snap.TCnComV()
    # GetSccs For Components
    snap.GetSccs(GraphkarateclubMaintainForDeleteEdges, Components)
    Modularity = snap.GetModularity(Graphkarateclub, Components)

    # Add Modularity Value Append in Global List ModularityList
    ModularityList.append(Modularity)
    ''' community structure for which the graph has highest modularity'''
    if Modularity > CheckModularity:
        CheckModularity=Modularity
        CommunityList=Components

print "The modularity of the network is %f" % max(ModularityList)

'''Output the community structure for which the graph has highest modularity'''
for Cmty in CommunityList:
    print "Community: "
    for NI in Cmty:
        print NI

'''plot a graph of modularity for each iteration'''
Epoch=range(Graphkarateclub.GetEdges())
plt.plot(Epoch, ModularityList)
plt.xlabel('Iteration')
plt.ylabel('Modularity')
plt.title('Iteration VS  Modularity : Karate Club Graph')
plt.show()