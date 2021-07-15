import networkx as nx

# and the following code block is not needed
# but we want to see which module is used and
# if and why it fails
import pydot
from networkx.drawing.nx_pydot import write_dot
import copy

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
        redTo = []
        for outnode in rec[3]:
            if(outnode[1] == 'red'):
                redTo.append((outnode[0],outnode[2]))
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

##############################
#
#   Remove simple structures. 
#
#   Remove simple grey and red/blue transformation
#
##############################

def reaction_filter2(G,totrec,conjDic):
    rmList=[]
    for rec in totrec:
        if( len(rec[2]) == 0 or len(rec[3])==0):
            continue

        if(rec[0] == "5982426591748898998"):
            print(rec)
        #
        # Remove Grey Transformations
        #
        # In-edge start remove Grey edges.
        if( rec[2][0][2] < rec[3][0][2]):
            nstraight = 0
            nzigzag = 0
            rmList_t = []
            for i in range(min( len(rec[2]),len(rec[3]) )):
                # Go straight
                # Wasted ?
                if (rec[2][i][2]-rec[3][i][2] < 65 and
                    rec[2][i][2]>rec[3][i][2] and
                      rec[3][i][1] == 'grey' and 
                      rec[2][i][1] == 'grey' and
                      rec[3][i][0] == rec[2][i][0]):
                    rmList_t.append( (rec[0],rec[3][i][0],rec[3][i][2],"straight") )
                    rmList_t.append( (rec[3][i][0],rec[0],rec[2][i][2],"straight") )
                    nstraight = nstraight + 1 
                       
                if(i+1 > len(rec[2])-1):
                    break
                # Go zigzag
                # Redifine zigzag walk-path
                if (rec[2][i+1][2]-rec[3][i][2] < 65 and
                    rec[2][i][2] < rec[3][i][2] and
                      rec[3][i][1] == 'grey' and 
                      rec[2][i+1][1] == 'grey' and
                      rec[3][i][0] == rec[2][i+1][0]):
                    nzigzag = nzigzag + 1
                    rmList_t.append( (rec[0],rec[3][i][0],rec[3][i][2],"zigzag" ) )
                    rmList_t.append( (rec[2][i+1][0],rec[0],rec[2][i+1][2],"zigzag" ) )

            # Zigzag or straight.

            '''
            if(nstraight > nzigzag):
                for itm in rmList_t:
                    if(itm[3] == "straight"):
                        rmList.append((itm[0],itm[1],itm[2]))
            else:
                for itm in rmList_t:
                    if(itm[3] == "zigzag"):
                        rmList.append((itm[0],itm[1],itm[2]))
            '''
            if(rec[0] == "5982426591748898998"):
                print(rmList_t)
            for itm in rmList_t:
                    rmList.append((itm[0],itm[1],itm[2]))


        # Out-edge start remove Grey edges.                
        else:
            nstraight = 0
            nzigzag = 0
            rmList_t = []
            for i in range(min( len(rec[2]),len(rec[3]) )):
                 # Go straight
                if (rec[2][i][2]-rec[3][i][2] < 65 and
                    rec[2][i][2]>rec[3][i][2] and
                      rec[2][i][1] == 'grey' and 
                      rec[3][i][1] == 'grey' and
                      rec[3][i][0] == rec[2][i][0]):
                    rmList_t.append( (rec[2][i][0],rec[0],rec[2][i][2],"straight") )
                    rmList_t.append( (rec[0],rec[3][i][0],rec[3][i][2],"straight") )
                    nstraight = nstraight + 1 
                if(i+1 > len(rec[2])-1):
                    break
                 # Go zigzag
                # wasted ? 
                if (rec[2][i+1][2]-rec[3][i][2] < 65 and
                      rec[2][i][2] < rec[3][i][2] and
                      rec[3][i][1] == 'grey' and 
                      rec[2][i+1][1] == 'grey' and
                      rec[3][i][0] == rec[2][i+1][0]):
                    rmList_t.append( (rec[0],rec[3][i][0],rec[3][i][2],"zigzag" ) )
                    rmList_t.append( (rec[2][i+1][0],rec[0],rec[2][i+1][2],"zigzag" ) )
                    nzigzag = nzigzag + 1
            if(rec[0] == "5982426591748898998"):
                print(rmList_t)
            for itm in rmList_t:
                rmList.append((itm[0],itm[1],itm[2]))


            
        #
        # Remove Red-Blue Transformations
        #
        # In-edge start
        if( rec[2][0][2] < rec[3][0][2]):

            nstraight = 0
            nzigzag = 0
            rmList_t = []
            for i in range(min( len(rec[2]),len(rec[3]) )):
                #
                # wasted ?
                if (rec[2][i][2]-rec[3][i][2] < 65 and
                    rec[2][i][2] > rec[3][i][2] and
                      rec[2][i][1] == 'blue' and 
                      rec[3][i][1] == 'red' and
                      rec[3][i][0] == rec[2][i][0]):
                    # remove the refer path 

                    # Remove Conj. path
                    conj_tag1 = '0'
                    conj_tag2 = '0'
                    for rec_conj in rec[5]:
                        # same step out-edge
                        if(rec_conj[1] == rec[3][i][2]):
                            conj_tag1 = rec_conj[0]
                            break
                    inList = G.in_edges(conj_tag1,data=True)
                    remove = False
                    for itm in inList:
                        if(itm[0] == rec[2][i][0] and itm[1] == conj_tag1 and int(itm[2]['label'].strip('\"' )) == rec[3][i][2]):
                            remove = True
                            break
                    if (remove):
                        rmList_t.append( (rec[2][i][0],rec[0],rec[2][i][2],"straight") )
                        rmList_t.append( (rec[0],rec[3][i][0],rec[3][i][2],"straight") )
                        rmList_t.append( (rec[2][i][0],conj_tag1,rec[2][i][2],"straight") )
                        rmList_t.append( (conj_tag1,rec[3][i][0],rec[3][i][2],"straight") )
                    nstraight = nstraight + 1 

                if(i+1 > len(rec[2])-1):
                    break
                    # Go zigzag
                if (rec[2][i+1][2] - rec[3][i][2] < 65 and
                    rec[2][i][2] < rec[3][i][2] and
                      rec[3][i][1] == 'red' and 
                      rec[2][i+1][1] == 'blue' and
                      rec[3][i][0] == rec[2][i+1][0]):
                
                    nzigzag = nzigzag + 1
                    # Remove Conj. path
                    conj_tag1 = '0'
                    conj_tag2 = '0'
                    for rec_conj in rec[5]:
                        # same step out-edge
                        if(rec_conj[1] == rec[3][i][2]):
                            conj_tag1 = rec_conj[0]
                            break
                            
                    # Check if conjNode in edges
                    inList = G.in_edges(conj_tag1,data=True)
                    remove = False
                    for itm in inList:
                        if(itm[0] == rec[2][i+1][0] and itm[1] == conj_tag1 and int(itm[2]['label'].strip('\"' )) == rec[2][i+1][2]):
                            remove = True
                            break

                    if (remove):
                        rmList_t.append( (rec[0],rec[3][i][0],rec[3][i][2],"zigzag" ) )
                        rmList_t.append( (rec[2][i+1][0],rec[0],rec[2][i+1][2],"zigzag" ) )
                        rmList_t.append( (conj_tag1,rec[3][i][0],rec[3][i][2],"zigzag" ) )
                        rmList_t.append( (rec[2][i+1][0],conj_tag1,rec[2][i+1][2],"zigzag" ) )
            if(rec[0] == "5982426591748898998"):
                print(rmList_t)
            for itm in rmList_t:
                rmList.append((itm[0],itm[1],itm[2]))
                            

                        
        # Out-edge start remove Red/nlue edges.                
        else:
            nstraight = 0
            nzigzag = 0
            rmList_t = []
            for i in range(min( len(rec[2]),len(rec[3]) )):
                 # Go straight
                if (rec[2][i][2]-rec[3][i][2] < 65 and
                    rec[2][i][2]>rec[3][i][2] and 
                      rec[2][i][1] == 'blue' and 
                      rec[3][i][1] == 'red' and
                      rec[3][i][0] == rec[2][i][0]):                

                    nstraight = nstraight + 1
                    for rec_conj in rec[5]:
                        # same step out-edge
                        if(rec_conj[1] == rec[3][i][2]):
                            conj_tag1 = rec_conj[0]
                            break
                    inList = G.in_edges(conj_tag1,data=True)
                    remove = False
                    for itm in inList:
                        if(itm[0] == rec[2][i][0] and itm[1] == conj_tag1 and int(itm[2]['label'].strip('\"' )) == rec[2][i][2]):
                            remove = True
                            break
                    if (remove):
                        rmList_t.append( (rec[2][i][0],rec[0],rec[2][i][2],"straight") )
                        rmList_t.append( (rec[0],rec[3][i][0],rec[3][i][2],"straight") )
                        rmList_t.append( (rec[2][i][0],conj_tag1,rec[2][i][2],"straight") )
                        rmList_t.append( (conj_tag1,rec[3][i][0],rec[3][i][2],"straight") )

                if(i+1 > len(rec[2])-1 ):
                    break
                # Go zigzag
                # wasted ?
                if (rec[2][i+1][2]-rec[3][i][2] < 65 and
                      rec[2][i][2] < rec[3][i][2] and
                      rec[3][i][1] == 'red' and 
                      rec[2][i+1][1] == 'blue' and
                      rec[3][i][0] == rec[2][i+1][0]):
                    for rec_conj in rec[5]:
                        # same step out-edge
                        if(rec_conj[1] == rec[3][i][2]):
                            conj_tag1 = rec_conj[0]
                            break
                    inList = G.in_edges(conj_tag1,data=True)

                    remove = False
                    for itm in inList:
                        if(itm[0] == rec[2][i+1][0] and itm[1] == conj_tag1 and int(itm[2]['label'].strip('\"' )) ==rec[2][i+1][2]):
                            remove = True
                            break
                    if (remove):
                        rmList_t.append( (rec[0],rec[3][i][0],rec[3][i][2],"zigzag" ) )
                        rmList_t.append( (rec[2][i+1][0],rec[0],rec[2][i+1][2],"zigzag" ) )
                        rmList_t.append( (conj_tag1,rec[3][i][0],rec[3][i][2],"zigzag" ) )
                        rmList_t.append( (rec[2][i+1][0],conj_tag1,rec[2][i+1][2],"zigzag" ) )

                    nzigzag = nzigzag + 1  
                    
            '''if(nstraight > nzigzag):
                for itm in rmList_t:
                    if(itm[3] == "straight"):
                        rmList.append((itm[0],itm[1],itm[2]))
            else:
                for itm in rmList_t:
                    if(itm[3] == "zigzag"):
                        rmList.append((itm[0],itm[1],itm[2]))
            '''
            if(rec[0] == "5982426591748898998"):
                print(rmList_t)
            for itm in rmList_t:

                rmList.append((itm[0],itm[1],itm[2]))
    return(rmList)


def rmSinglenode(G):                                    
    RawNodeList = G.nodes()
    rmNodeList = []
    for node in RawNodeList:                            
        edgesRawIn = G.in_edges(node,data=True)      
        edgesRawOut = G.out_edges(node,data=True)
        if(len(edgesRawIn)==0 and len(edgesRawOut)==0): 
            rmNodeList.append(node)
    for node in rmNodeList:
        G.remove_node(node)
            
            
def rmEdgeList(G,rmList):
    count = 0
    for itm in rmList:
        count = count +1
        G.remove_edge(itm[0],itm[1],key=itm[3])
    return G
            
    
def addKeyToRMlist(G,rmList):
    rmListUPD = []
    for itm in rmList:
        dicts = G.get_edge_data(itm[0], itm[1])
        for key in dicts:
            if(dicts[key]['label'].strip('\"' ) == str(itm[2])):
                rmListUPD.append((itm[0],itm[1],itm[2],key))
    return(rmListUPD)
                
#=================================
# Program Control
#
#=================================

if __name__ == '__main__':
    print("main")
    G = nx.drawing.nx_pydot.read_dot("/home/xchen/Develop/CPX-MechGen/reactionGraph.data")
    G_t = copy.deepcopy(G)

# 1. simple remove
    
    print("total nodes in original graph: ",G_t.number_of_nodes())
    print("total edges in original graph: ",G_t.number_of_edges())
    for i in range(3):
        # 1.0 Build node information.
        rec = buildBasicInfo(G_t)
        Totrec,conjDic = getConjInfo(G_t,rec)
        # 1.1 Remove redundant edges.
        rmList = reaction_filter2(G_t,Totrec,conjDic)
        rmList_UPD = addKeyToRMlist(G_t,rmList)
        rmList_UPD = list(set(rmList_UPD))
        G_t = rmEdgeList(G_t,rmList_UPD)

    rmSinglenode(G_t)
    print("total nodes in simple reduced graph: ",G_t.number_of_nodes())
    print("total edges in simple reduced graph: ",G_t.number_of_edges())
    print("reduced graph is stored in reduce.dot")
    write_dot(G_t, "reduce.dot")
# End of simple remove 
