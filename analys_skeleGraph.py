import networkx as nx
import pydot
from networkx.drawing.nx_pydot import write_dot

def buildSkeG(G):
    dic = nx.get_node_attributes(G,'label')
    newG = nx.DiGraph()
    for inode in G.nodes():
        outEdges = list(G.out_edges(inode,data=True))
        if(len(outEdges) == 0):
            continue
        if(len(outEdges) == 1):
            print(outEdges[0])
            Node1 = outEdges[0][0]
            Node2 = outEdges[0][1]
            newG.add_edge(Node1,Node2)
            newG.nodes[Node1]["label"] = dic[Node1]
            newG.nodes[Node2]["label"] = dic[Node2]
            newG.edges[Node1,Node2].update(outEdges[0][2])
            
        else:
            if(outEdges[-1][2]['color'] == 'blue'):
                Node1 = outEdges[-1][0]
                Node2 = outEdges[-1][1]
                newG.add_edge(Node1,Node2)
                newG.edges[Node1,Node2].update(outEdges[-1][2])
                newG.nodes[Node1]["label"] = dic[Node1]
                newG.nodes[Node2]["label"] = dic[Node2]
                
                Node1 = outEdges[-2][0]
                Node2 = outEdges[-2][1]
                newG.add_edge(Node1,Node2)
                newG.edges[Node1,Node2].update(outEdges[-2][2])
                newG.nodes[Node1]["label"] = dic[Node1]
                newG.nodes[Node2]["label"] = dic[Node2]
            else:
                Node1 = outEdges[-1][0]
                Node2 = outEdges[-1][1]
                newG.add_edge(Node1,Node2)
                newG.edges[Node1,Node2].update(outEdges[-1][2])
                newG.nodes[Node1]["label"] = dic[Node1]
                newG.nodes[Node2]["label"] = dic[Node2]
    return newG



G = nx.drawing.nx_pydot.read_dot("nes.dot")
nx.draw(G,with_labels=False)
newG = buildSkeG(G)
nx.draw(newG,with_labels=False)
write_dot(newG, "nes2.dot")




