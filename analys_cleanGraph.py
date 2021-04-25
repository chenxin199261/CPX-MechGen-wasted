import networkx as nx
import pydot
from networkx.drawing.nx_pydot import write_dot

## Build node information:
def Sort(sub_li,iplace): 
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of  
    # sublist lambda has been used 
    sub_li.sort(key = lambda x: x[iplace]) 
    return sub_li 


def buildBasicInfo(G):
    RawNodeList = G.nodes(data=True)
    rec = []
    for node in RawNodeList:
        # Nodeinfo=[nodeID,nodelabel,[Inedges],[OutEdges]]
        # Get Label
        nodeInfo = [node[0],node[1]['label']]
        #print(nodeInfo)
        
        # GetInEdges:
        InEdge = []
        edgesRawIn = G.in_edges(node[0],data=True)
        for edge in edgesRawIn:
            InEdge.append((edge[0],edge[2]['color'],int(edge[2]['label'].strip('\"' ))))
        InEdge = Sort(InEdge,2)
        #print(InEdge)
        nodeInfo.append(InEdge)
        
        # GetOutEdges:
        OutEdge = []
        edgesRawOut = G.out_edges(node[0],data=True)
        for edge in edgesRawOut:
            OutEdge.append((edge[1],edge[2]['color'],int(edge[2]['label'].strip('\"' ))))
        OutEdge = Sort(OutEdge,2)
        nodeInfo.append(OutEdge)
        for i in range(len(nodeInfo[2]) - 1):
            Type='edge'
            if(nodeInfo[2][i][2] == nodeInfo[2][i+1][2] and nodeInfo[2][i][1]=='red' and nodeInfo[2][i+1][1]=='red'):
                Type='center'
                break
            if(nodeInfo[2][i][2] == nodeInfo[2][i+1][2] and nodeInfo[2][i][1]=='blue' and nodeInfo[2][i+1][1]=='blue'):
                Type='center'
                break
        nodeInfo.append(Type)
            
        rec.append(nodeInfo)
    return rec
    
    
def getConjInfo(G,Totrec):
    Conj = []
    conjDict={}
    for rec in Totrec:
        #print(rec[0])
        redTo = []
        for outnode in rec[3]:
            if(outnode[1] == 'red'):
                redTo.append((outnode[0],outnode[2]))
        #print(redTo)
        #Build conj. List
        conjList = []
        for arrow in redTo:
            edgesRawIn = G.in_edges(arrow[0],data=True)
            for nodeIn in edgesRawIn:
                if( int(nodeIn[2]['label'].strip('\"' )) == arrow[1] 
                    and nodeIn[2]['color'] == 'red'                   
                    and nodeIn[0] != rec[0]):
                    conjList.append( (nodeIn[0],arrow[1]) )
        conjDict[rec[0]]=conjList
        rec.append(conjList)
    return Totrec,conjDict
'''
def delTrans(ori,node,start,end,G,conjDic):
    rmList = [(ori,node,start),(node,ori,end)]
    searchList = [node]
    recorded =[node]
    # find edges in searchList
    while (len(searchList) > 0):
        searchListNew=[]
        for node in searchList:
            outEdges = G.out_edges(node,data=True)
            for edge in outEdges:
                stp = int(edge[2]['label'].strip('\"' ))
                if( stp > start and stp < end and edge[2]['color'] =='grey'):
                    if(edge[1] not in recorded):
                        searchListNew.append(edge[1])
                        rmList.append((edge[0],edge[1],stp))
                        recorded.append(edge[1])

        searchList = searchListNew
    print(rmList,"grey")
'''

def reaction_filter(G,totrec,conjDic):
    for rec in totrec:
        if(rec[4] =="center"):
            continue
        if( len(rec[2]) == 0 or len(rec[3])==0):
            continue
        # j: In edge startpoint
        if( rec[2][0][2] > rec[3][0][2]):
            In_start = 0
            sl = len(rec[2])
        else:
            In_start = 1
            sl = len(rec[2]) - 1
        Garbrecord = []
        rmList=[]
        for i in range( min(sl,len(rec[3]))):
            if(rec[2][i+In_start][2]- rec[3][i][2] <60):
                if(i+In_start > len(rec[2])):
                    break
                # grey out and grey in
                if(rec[3][i][1]=='grey' and 
                   rec[2][i+In_start][1]=='grey' and
                   rec[2][i+In_start][0]==rec[3][i][0]):
                    rmList.append( (rec[0],rec[3][i][0],rec[3][i][2]) )
                    rmList.append( (rec[3][i][0],rec[0],rec[2][i][2]) )
                    
                    #delTrans(rec[0],rec[3][i][0],rec[3][i][2],rec[2][i+In_start][2],G,conjDic)
                    
                
                # Red out and blue in
                if(rec[3][i][1]=='red' and rec[2][i+In_start][1]=='blue'):
                    # Check conj. Node
                    for conjRec in rec[5]:
                        # Get Conj. node
                        if(conjRec[1] == rec[3][i][2]):
                            ConjNode = conjRec[0]
                            # Search out edges of conj. node
                            ConjNodeOutEdges = G.in_edges(ConjNode,data=True)
                            for outedge in ConjNodeOutEdges:
                                if( int(outedge[2]['label'].strip('\"' )) == rec[2][i+In_start][2] and
                                        outedge[0] == rec[2][i+In_start][0]):
                                    #print(rec[3][i],outedge)
                                    rmList.append( (rec[0],rec[3][i][0],rec[3][i][2]) )
                                    rmList.append( (conjRec[0],rec[3][i][0],rec[3][i][2]) )
                                    
                                    rmList.append( (rec[3][i][0],rec[0],rec[2][i+In_start][2]) )
                                    rmList.append( (rec[3][i][0],conjRec[0],rec[2][i+In_start][2]) )
                                    break
        if(len(rmList) == 0):
            continue

        for edge in rmList:
            # Translate node to key.
            Rec = []
            edgeView = G.get_edge_data(edge[0],edge[1])
            if(edgeView is None):
                continue
            for key1 in edgeView:
                if(edgeView[key1]['label'].strip('\"' ) == str(edge[2])):
                    Rec.append([edge[0],edge[1],key1])
            for rec in Rec:
                G.remove_edge(rec[0],rec[1],rec[2])
    return(G)

G = nx.drawing.nx_pydot.read_dot("./reactionGraph.data")
dic = nx.get_node_attributes(G,'label')


G_t = G
rec = buildBasicInfo(G_t)
Totrec,conjDic = getConjInfo(G_t,rec)
Gout = reaction_filter(G_t,Totrec,conjDic)
write_dot(Gout, "reduce.dot")


