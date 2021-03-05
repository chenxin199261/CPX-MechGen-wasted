
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


def rmIso(G):
    # Remove useless rebundant reactions
    niso = 1
    niso_p = 0
    printTimeStamp("2")
    while(abs(niso_p-niso) != 0):
        niso_p = niso
        recV,niso = removeVib(G)
        print(niso,"   -NISO")
    printTimeStamp("1")
    return G 

def rmParaEdges(G):
    print(G)
    totRec  = getNodeInfo(G)
    conjRec = findConjEdges(totRec)
    print("#####$$$$$$$$$$#####")
    removeConjEdges(G,conjRec)
    return G
    
if __name__ == "__main__":
    fname="reactionGraph.data"   
    #fname="./subgraph/Ori_1.dot"   
    # Read dot File
    G = nx.drawing.nx_pydot.read_dot(fname)
    write_dot(G, "ConvertTotal.dot")
    G = rmParaEdges(G)
    G = rmIso(G) 
    write_dot(G,"./Rev_graph.dot")
