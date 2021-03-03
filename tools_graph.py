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


#==================
#  Tools (edges+nodes)
#==================

def Sort(sub_li,iplace): 
  
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of  
    # sublist lambda has been used 
    sub_li.sort(key = lambda x: x[iplace]) 
    return sub_li 

def findConjEdges(NodesRec):
    totRec=[]
    for node in NodesRec:
        # Inedges:
        nodeConjRec = [node[0]]
        inTemp=[]
        for i in range(len(node[4])-1):
            for j in range(i+1,len(node[4])):
                #print(i,j,node[4])
                if(node[4][i][1] == node[4][j][1] ):
                    RecTemp = [node[4][i][0],node[4][j][0],node[4][i][3],node[4][j][3],node[4][j][1]]
                    inTemp.append(RecTemp)
                    break
        nodeConjRec.append(inTemp)
                    
        # Outedges:
        outTemp=[]
        for i in range(len(node[5])-1):
            for j in range(i+1,len(node[5])):
                #print(i,j,node[4])
                if( node[5][i][1] == node[5][j][1] ):
                    RecTemp = [node[5][i][0],node[5][j][0],node[5][i][3],node[5][j][3],node[5][j][1]]
                    outTemp.append(RecTemp)
                    break
        nodeConjRec.append(outTemp)
                    
        totRec.append(nodeConjRec)
    return(totRec) 

def getNodeInfo(G):
    nodesRec = G.nodes()
    TotRec = []
    Nodedic = nx.get_node_attributes(G,'label')
    for inode in nodesRec:
        NodeRec = [inode,0,0,0]
        NodeRec[1] =  Nodedic[inode]
        NodeRec[2] =  G.in_degree(inode)
        NodeRec[3] =  G.out_degree(inode)
        edges = list(dict.fromkeys(G.in_edges(inode)))
        
        InedgeRec = []
        for iedge in edges:
            get = G.get_edge_data(iedge[0],iedge[1])
            for key in get:
                InedgeRec.append([iedge[0],int(get[key]['label'].strip('\"' )),get[key]['color'],int(key)])
        NodeRec.append(Sort(InedgeRec,1))
                
        edges = list(dict.fromkeys(G.out_edges(inode)))
        OutedgeRec = []
        for iedge in edges:
            get = G.get_edge_data(iedge[0],iedge[1])
            for key in get:
                OutedgeRec.append([iedge[1],int(get[key]['label'].strip('\"' )),get[key]['color'],int(key)])
        NodeRec.append(Sort(OutedgeRec,1))
        TotRec.append(NodeRec)
    return(TotRec)

def removeConjEdges(G,conjRec):
    for node in conjRec:
        if(len(node[1]) > 0 and len(node[2]) > 0 ):
            for rec1 in node[1]:
                removeTag = False
                for rec2 in node[2]:
                    # In and Out ConjEdges coupled together. 
                    if(rec1[0] in rec2 and rec1[1] in rec2 and abs(rec1[4]-rec2[4])<40):
                        print(rec1,rec2)
                        #remove edge from:
                        try:
                            G.remove_edge(rec1[0],node[0],key=str(rec1[2]))
                        except:
                            pass

                        try:
                            G.remove_edge(rec1[1],node[0],key=str(rec1[3]))
                        except:
                            pass
                        
                        try:
                            G.remove_edge(node[0],rec2[0],key=str(rec2[2]))
                        except:
                            pass

                        try:
                            G.remove_edge(node[0],rec2[1],key=str(rec2[3]))
                        except:
                            pass
                        removeTag = True
                        break
                if removeTag:
                    node[2].remove(rec2)




