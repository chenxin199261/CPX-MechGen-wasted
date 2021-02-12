
"""
CPX-MechGen: 
Discover reaction mechanism from complex reaction network.

-Author      : Chen Xin
-Email       : chenxin199261@gmail.com
-Create Date : 2021/2/4 
-Inputs:
    1. reactionGraph.data fill the paths in variable 'fnames'.

-Outputs:
    In local file ./subgraph
    1. Orginal subgraph: For debug.
    2. Processed subgraph: Analysed. 

"""

import os
import networkx as nx

# and the following code block is not needed
# but we want to see which module is used and
# if and why it fails
try:
    import pygraphviz
    from networkx.drawing.nx_agraph import write_dot
except ImportError:
    try:
        import pydot
        from networkx.drawing.nx_pydot import write_dot
    except ImportError:
        raise

#========
#  Tools
#========
def searchIsoEdges(G,node):
    color = 0 # 0:grey,1:others
    InOut = [] # ismaxlabel out-arrow ?
    colorRec = nx.get_edge_attributes(G, "color")
    labelRec = nx.get_edge_attributes(G, "label")
    # search Inarrow
    deg = [0,0]
    stepRec=[]
    for key in colorRec:
        if (node in key):
            if(colorRec[key] == "grey"):
                color = 0
            else:
                color = 1
            deg[0] = G.in_degree(node)
            deg[1] = G.out_degree(node)
            stepRec.append(int(labelRec[key].strip('\"' )))
            if (key.index(node)==0):
                InOut.append("O")
                link = key[1]
            else:
                InOut.append("I")
                link = key[0]

    # search Outarrow
    return color,InOut,stepRec,link,deg
    
def getIsoNodes(G):
    NodeList = []
    nodes=nx.nodes(G)
    print(len(nodes))
    edges = nx.get_edge_attributes(G, "color")
    for node in nodes:
        nNeighbor = len(set(nx.all_neighbors(G,node)))
        if nNeighbor == 1:
            color,outArrow,maxV,link,deg=searchIsoEdges(G,node)
            NodeList.append([node,color,outArrow,maxV,link,deg])
    return NodeList

def removeVib(G):
    ## 1. Remove non-reactive vibrations
     # 1.1 remove inner-molecular interaction (Gray)
    listN = getIsoNodes(G)
    for isoNode in listN:
        edgesRec = G.edges(isoNode[0])
        if(isoNode[1]==0 and isoNode[5][0]==isoNode[5][1]):
            for i in range(len(isoNode[2])):
                keep_node= True
                for j in range(len(isoNode[2])):
                    if( abs(isoNode[3][i]-isoNode[3][j])<5 and isoNode[2][i] !=isoNode[2][j]):
                        keep_node= False
                        break
                if(keep_node):
                    break
    
            if(keep_node):
                pass
            else:
                print("removed gray: ",isoNode)
                G.remove_node(isoNode[0])
    ## 2 remove conjuncted Red/blue vibrations
     # 2.1 find conjuntion nodes
    listN = getIsoNodes(G)
    conj_pair=[]
    for i in range(len(listN)-1):
        for j in range(i+1,len(listN)):
            if(listN[i][3] == listN[j][3] and listN[i][5][0]==listN[i][5][1]):
                print(listN[i],"++",i,j)
                print(listN[i][5],listN[j][5],"--",i,j)
                conj_pair.append((i,j))
    print(conj_pair)
    # 2.2 Remove conjuntion nodes
    removed = []
    for ele in conj_pair:
        i = ele[0]
        j = ele[1]
        print(i,j,"for check")
        if( len(listN[i][3]) > 1):
            if(abs(listN[i][3][0] - listN[i][3][1]) < 5 ):
                if (listN[i][0] not in removed):
                    G.remove_node(listN[i][0])
                    removed.append(listN[i][0])
                if (listN[j][0] not in removed):
                    G.remove_node(listN[j][0])
                    removed.append(listN[j][0])
    return G

def anaSubgraph(fname):
#   G = nx.drawing.nx_pydot.read_dot("reactionGraph.data")
#   write_dot(G, "ConvertTotal.dot")
#   ## 1. Divide graph into subgraph
#   sub_set = nx.weakly_connected_components(G)
#   subG = []
#   for nset in sub_set:
#       subG.append(G.subgraph(list(nset)))
#    # 1.1 save subgraph into file
#   Num = 0
#   for rec in subG:
#       name = "./subgraph/Ori_"+str(Num)+".dot"
#       write_dot(rec,name)
#       Num = Num+1
    Num = 0
    for coun in range(0,354):
        name = "./subgraph/Ori_"+str(Num)+".dot"
        print(name+"  :1")
        name2 = "./subgraph/Rev_"+str(Num)+".dot"
        rec = nx.drawing.nx_pydot.read_dot(name)
        recV = removeVib(rec)
        write_dot(recV,name2)
        Num = Num+1
    
    
if __name__ == "__main__":
    fname="reactionGraph.data"   
    anaSubgraph(fname) 
