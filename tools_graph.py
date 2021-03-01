import networkx as nx
from datetime import datetime
import pydot
from networkx.drawing.nx_pydot import write_dot

def printTimeStamp(tag):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time," at :",tag)

#==================
#  Tools (isoNode)
#==================

def searchIsoEdges(G,node,colorRec,labelRec):
    color = 0 # 0:grey,1:others
    InOut = [] # ismaxlabel out-arrow ?
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
    
def getIsoNodes(G,cR,lR):
    NodeList = []
    nodes=nx.nodes(G)
    edges = nx.get_edge_attributes(G, "color")
    for node in nodes:
        nNeighbor = len(set(nx.all_neighbors(G,node)))
        if nNeighbor == 1:
            color,outArrow,maxV,link,deg=searchIsoEdges(G,node,cR,lR)
            NodeList.append([node,color,outArrow,maxV,link,deg])
    return NodeList

def removeVib(G):
    ## 1. Remove non-reactive vibrations
     # 1.1 remove inner-molecular interaction (Gray)
    colorRec = nx.get_edge_attributes(G, "color")
    labelRec = nx.get_edge_attributes(G, "label")
    listN = getIsoNodes(G,colorRec,labelRec)
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
                G.remove_node(isoNode[0])
    ## 2 remove conjuncted Red/blue vibrations
     # 2.1 find conjuntion nodes
    listN = getIsoNodes(G,colorRec,labelRec)
    conj_pair=[]
    for i in range(len(listN)-1):
        for j in range(i+1,len(listN)):
            if(listN[i][3] == listN[j][3] and listN[i][5][0]==listN[i][5][1]):
                conj_pair.append((i,j))
     # 2.2 Remove conjuntion nodes
    removed = []
    for ele in conj_pair:
        i = ele[0]
        j = ele[1]
        if( len(listN[i][3]) > 1):
            if(abs(listN[i][3][0] - listN[i][3][1]) < 5 ):
                if (listN[i][0] not in removed):
                    G.remove_node(listN[i][0])
                    removed.append(listN[i][0])
                if (listN[j][0] not in removed):
                    G.remove_node(listN[j][0])
                    removed.append(listN[j][0])
    listN = getIsoNodes(G,colorRec,labelRec)
    return G,len(listN)
