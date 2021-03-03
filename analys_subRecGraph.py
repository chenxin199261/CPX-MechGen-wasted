
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
import pydot
from networkx.drawing.nx_pydot import write_dot
from tools_graph import *

#def rmRedEdgNodes(fname):


def anaSubgraph(fname):
    G = nx.drawing.nx_pydot.read_dot("reactionGraph.data")
    write_dot(G, "ConvertTotal.dot")
    ## 1. Divide graph into subgraph
    sub_set = nx.weakly_connected_components(G)
    subG = []
    for nset in sub_set:
        subG.append(G.subgraph(list(nset)))
     # 1.1 save subgraph into file
    Num = 0
    for rec in subG:
        name = "./subgraph/Ori_"+str(Num)+".dot"
        write_dot(rec,name)
        Num = Num+1
    Num = 0
    for coun in range(0,len(subG)-1):
        printTimeStamp("1")
        name = "./subgraph/Ori_"+str(Num)+".dot"
        print(name+"  :1")
        name2 = "./subgraph/Rev_"+str(Num)+".dot"
        rec = nx.drawing.nx_pydot.read_dot(name)
        printTimeStamp("2")
        # Remove useless rebundant reactions
        niso = 1
        niso_p = 0
        while(abs(niso_p-niso) != 0):
            print("niso_p,niso111",niso_p,niso)
            niso_p = niso
            recV,niso = removeVib(rec)
            print(niso,"   -NISO")
            print("niso_p,niso222",niso_p,niso)

        printTimeStamp("3")
        write_dot(recV,name2)
        Num = Num+1
        return subG 

def rmParaEdges(G):
    totRec  = getNodeInfo(G)
    conjRec = findConjEdges(totRec)
    print("#####$$$$$$$$$$#####")
    removeConjEdges(G,conjRec)
    
if __name__ == "__main__":
    fname="reactionGraph.data"   
    #subG = anaSubgraph(fname) 
    #print(len(subG))
    G = nx.drawing.nx_pydot.read_dot("./subgraph/Rev_0.dot")
    rmParaEdges(G)
