from tools import *


debug =  True 



def trackBlocks(fnames,trackList):
    Rstep = []
    istep = 1
    step  = 1
    bnd_cri = 1.6  # Criterion for bond linkage
    for fname in fnames:
        with  open(fname,'r') as f:
            if (istep == 1):
                # First Record:
                Natom = int(f.readline())
                atomList = [0]*Natom # BuildUpAtomList
                f.readline()
                for i in range(Natom):
                    line = f.readline().split()
                    line[2] = float(line[2])
                    line[3] = float(line[3])
                    atomList[i] = \
                    [line[0],[float(line[1]),float(line[2]),float(line[3])],[]]
                   #   ^                 ^                                  ^
                   #  ele.Name,  element coordinate,                  neighbor    
                atomList = buildNeigh(atomList,20) # 20 anstrom into neighbour

                # Divide system into fragments.
                mat = buildLinkMat(atomList,bnd_cri)
                nMol,MolRec = groupOp(mat)
                if (debug): print(nMol)
                blockList = [[0]*5 for i in range(nMol)] # BuildUpBlockList
                Molid = 1
                for rec in MolRec:
                    blockList[Molid-1][0] = Molid
                    blockList[Molid-1][1] = list(rec)
                    Molid = Molid+1
                BlockInfoUpdate(blockList,atomList)
                speRec = []
                p = specCount(blockList,trackList)
                speRec.append(p)
                Rstep.append(5*istep*10**(-7))
            while True:
                if (debug): print(istep,step,len(blockList))
                line = f.readline()
                if not line:break
                Natom =int(line)
                f.readline()
                for i in range(Natom):
                    line = f.readline().split()
                    line[2] = float(line[2])
                    line[3] = float(line[3])
                    atomList[i][0] = line[0]
                    atomList[i][1] = [float(line[1]),float(line[2]),float(line[3])]
                if(istep%200 == 0):
                    atomList=buildNeigh(atomList,20)
                if(istep%10 == 0):
                    mat =  buildLinkMat(atomList,bnd_cri)
                    nMol,MolRec = groupOp(mat)
                    blockList = [[0]*5 for i in range(nMol)] # BuildUpBlockList
                    Molid = 1
                    for rec in MolRec:
                        blockList[Molid-1][0] =Molid
                        blockList[Molid-1][1] =list(rec)
                        Molid = Molid+1
                    BlockInfoUpdate(blockList,atomList)
                    p=specCount(blockList,trackList)
                    if (debug): print(p)
                    Rstep.append(5*istep*10**(-7))
                    speRec.append(p)
                istep = 1+istep
    return([])




if __name__ == "__main__":
    """
    CPX-MechGen: 
    Discover reaction mechanism from complex reaction network.

    -Author      : Chen Xin
    -Email       : chenxin199261@gmail.com
    -Create Date : 2021/1/19 
    -Inputs:
        1. Multiple xyz trajectory files. fill their paths in variable 'fname'.

    -Outputs:
        1. blk_evo  : The evolution of monitoring fragments. 
        2. graph.dat: Graph metaData 

    -Data structure:
        tempList1: atoms belonging to which group and group id
                   tempList1 = [atomRec*nstep]
                   atomRec[i] for atom i is [blknum,grp_id]

    """
    fnames = ["./examples/hello5.xyz",
              "./examples/hello6.xyz"]
    trackList =["MMH","NO2","N2","a","b","c","e","f"]
    tempList1 = trackBlocks(fnames,trackList)
