from tools import *
import json
import pickle
import copy
debug =  True
analy_mode = 3 # 1.raw xyz data to results 
               # 2.raw xyz data to tempRec
               # 3.temRecs to results


def trackBlocks(fnames,trackList):
    Rstep = []
    speRec = []
    tempList=[]    
    istep = 1
    step  = 1
    bnd_cri = 1.6  # Criterion for bond linkage

    # 1. read xyz data in
    for fname in fnames:
        with  open(fname,'r') as f:
            if (istep == 1):
                # First Record:
                Natom = int(f.readline())
                atomList = [0]*Natom # BuildUpAtomListi
                temGrpRec= [[0]*2 for i in range(Natom)] 
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
                #===  Build Templist  ===
                for rec in blockList:
                    for iatm in rec[1]:
                        temGrpRec[iatm-1][0] = rec[0]
                        temGrpRec[iatm-1][1] = rec[3]
                AtmList_temp = copy.deepcopy(temGrpRec)
                tempList.append(AtmList_temp)
                #========================
                p = [istep]
                p.extend(specCount(blockList,trackList))
                print(p)
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
                    #===  Build Templist  ===
                    for rec in blockList:
                        for iatm in rec[1]:
                            temGrpRec[iatm-1][0] = rec[0]
                            temGrpRec[iatm-1][1] = rec[3]
                    AtmList_temp = copy.deepcopy(temGrpRec)
                    tempList.append(AtmList_temp)
                    #========================
                    p = [istep]
                    p.extend(specCount(blockList,trackList))
                    if (debug): print(p)
                    Rstep.append(5*istep*10**(-7))
                    speRec.append(p)
                istep = 1+istep
        f.close()
    # 2. Print species records
    Ft = open("spec-rev.data","w")
    Ft.write(str(istep)+"\n")
    for rec in speRec:
        for ele in rec:
            Ft.write('{0:<6d}'.format(ele))
        Ft.write('\n')
    Ft.close()
    # 3. Save tempList to file
    if(analy_mode != 1):
        Ft = open("file.txt", 'wb')
        pickle.dump(tempList, Ft)
        Ft.close()
        tempList=[]
    return(tempList)

def reactionGen(totRec):
    chgRec_raw = []
    reac_rec_tot = []
    Ft_chk = open("hash_CheckList","w")
    for rec in  range(len(totRec)-1):
        chgRec_rec_stp=[]
        reac_rec = []
        # Build Raw change list
        for atm in range(len(totRec[0])):
            if(abs(totRec[rec+1][atm][1]-1417.40938) < 0.00001):
                print ("warning!P:",rec+1,totRec[rec+1][atm][1],totRec[rec+1][atm][0])
                print ("warning!R:",rec,totRec[rec][atm][1],totRec[rec][atm][0])
            if(abs(totRec[rec][atm][1]-1417.40938) < 0.00001):
                print ("warning!R:",rec+1,totRec[rec][atm][1],totRec[rec][atm][0])
            
            if(abs(totRec[rec+1][atm][1]-totRec[rec][atm][1]) > 0.00001):
                chg = [[totRec[rec][atm][0],totRec[rec+1][atm][0]],\
                       [totRec[rec][atm][1],totRec[rec+1][atm][1]],\
                       atm+1,rec+2]
                chgRec_rec_stp.append(chg)
        chgRec_raw.append(chgRec_rec_stp)
        # Build Rection information
        unique_blk_rec_R=[]
        unique_blk_rec_P=[]
        react_pair=[]
        for chg_rec in chgRec_rec_stp:
        # Unique Block number
            if chg_rec[0][0] not in unique_blk_rec_R:
                unique_blk_rec_R.append(chg_rec[0][0])
            if chg_rec[0][1] not in unique_blk_rec_P:
                unique_blk_rec_P.append(chg_rec[0][1])
            react_tup = tuple(chg_rec[0])
            if react_tup not in react_pair: 
                react_pair.append(react_tup)


        # Print hast checkList
        if (len(unique_blk_rec_R)>0):
            print(str(rec+2)+"  ========== \nchgRec_rec_stp:")
            for Rec_t in chgRec_rec_stp:
                print(Rec_t)
            print( "unique_blk_rec_RP:")
            for Rec_t in unique_blk_rec_R:
                print("R:",Rec_t)
            for Rec_t in unique_blk_rec_P:
                print("P:",Rec_t)
            for Rec_t in react_pair:
                print("react_pair:",Rec_t)

            # Build Hash-dict
            Hashdict_R={}
            Hashdict_P={}
            for iblk in unique_blk_rec_R:
                atmList = []
                grp_num = 0
                for atmrec in chgRec_rec_stp:
                    if atmrec[0][0] == iblk:
                        grp_num = atmrec[1][0]
                        atmList.append(atmrec[2])
                atmList.sort()
                atmList.append(grp_num)
                ls = [str(i) for i in atmList]
                HashT  = abs( hash("".join(ls)) )
                if grp_dic.get(round(grp_num,5)) is None:
                    grp_label=round(grp_num,5)
                else:
                    grp_label=grp_dic[round(grp_num,5)]
                Hashdict_R[iblk] = [HashT,grp_label]
                Ft_chk.write(str(HashT)+": ["+" ".join(ls[0:-1])+"]\n")

            for iblk in unique_blk_rec_P:
                atmList = []
                grp_num = 0
                for atmrec in chgRec_rec_stp:
                    if atmrec[0][1] == iblk:
                        grp_num = atmrec[1][1]
                        atmList.append(atmrec[2])
                atmList.sort()
                atmList.append(grp_num)
                ls = [str(i) for i in atmList]
                HashT  = abs( hash("".join(ls)) )
                if grp_dic.get(round(grp_num,5)) is None:
                    grp_label=round(grp_num,5)
                else:
                    grp_label=grp_dic[round(grp_num,5)]
                Hashdict_P[iblk] = [HashT,grp_label]
                Ft_chk.write(str(HashT)+": ["+" ".join(ls[0:-1])+"]\n")
            
            tup_lst_hash = []
            # Trans form reaction pair
            for i in unique_blk_rec_R:
                T_rec = [tuple([i]),tuple([])\
                         ,(),(),(),(),"F",0,0]
                for j in react_pair:
                    if(j[0] == i):
                        T_rec[1] = T_rec[1] + tuple([j[1]])
                tup_lst_hash.append(T_rec)
            remove_list =[]
            for i in unique_blk_rec_P:
                T_rec = [tuple([]),tuple([i])\
                         ,(),(),(),(),"F",0,0]
                for j in react_pair:
                    if(j[1] == i):
                        T_rec[0] = T_rec[0] + tuple([j[0]])
                        if(len(T_rec[0]) == 2):
                            T_rec[6] ="S" 
                            tup_lst_hash.append(T_rec)
                            remove_list.append(T_rec[0][0])
                            remove_list.append(T_rec[0][1])
                ## Delete redundant.
                remove_tag=[]
            for i in remove_list:
                for rec in tup_lst_hash:
                    if (len(rec[0])==1 and rec[0][0]==i and (rec not in remove_tag)):
                        remove_tag.append(rec)
            for i in remove_tag:
                tup_lst_hash.remove(i)

            # Build reaction type and hash
            for i in tup_lst_hash:
                for r in i[0]:
                    i[2] = tuple([Hashdict_R[r][0]]) + i[2]
                    i[4] = tuple([Hashdict_R[r][1]]) + i[4]
                for p in i[1]:
                    i[3] = tuple([Hashdict_P[p][0]]) + i[3]
                    i[5] = tuple([Hashdict_P[p][1]]) + i[5]
                if(len(i[0]) >=2 ):
                    i[6] = "C"
                    i[7] = chgRec_rec_stp[0][-1]
                    i[8] = i[2][0]+i[2][1]
                if(len(i[1]) >=2 ):
                    i[6] = "S"
                    i[7] = chgRec_rec_stp[0][-1]
                    i[8] = i[3][0]+i[3][1]
                if(len(i[1]) ==1 and len(i[0]) ==1):
                    i[6] = "T"
                    i[7] = chgRec_rec_stp[0][-1]
            reac_rec_tot.append(tup_lst_hash)


          #  for i in tup_lst_hash:
          #      print(i)
    flag = 0

    Ft = open("reactionGraph.data","w")
    Ft.write("digraph G{\n")
    # Print linkage
    for i in reac_rec_tot:
        for rec in i:
            if (rec[6] =="C"):
                for num in range(len(rec[0])):
                    # Add to hash-label:
                    lableStr=' [label="' + str(rec[7]) +'"]'
                    Hast_label[rec[2][num]] = [str(rec[4][num]),rec[7]]
                    Hast_label[rec[3][0]] =   [str(rec[5][0]),  rec[7]]
                    Ft.write("  "+ str(rec[2][num])+" -> "+str(rec[3][0]) +lableStr +" [color=red];\n")
            if (rec[6] =="S"):
                for num in range(len(rec[1])):
                    lableStr=' [label="' + str(rec[7]) +'"]'
                    Hast_label[rec[2][0]] =   [str(rec[4][0]),  rec[7]]
                    Hast_label[rec[3][num]] = [str(rec[5][num]),rec[7]]
                    Ft.write("  "+ str(rec[2][0])+" -> "+str(rec[3][num]) +lableStr +"[color=blue];\n")
            if (rec[6] =="T"):
                Hast_label[rec[2][0]] = [str(rec[4][0]),rec[7]]
                Hast_label[rec[3][0]] = [str(rec[5][0]),rec[7]]
                lableStr=' [label="' + str(rec[7]) +'"]'
                Ft.write("  "+ str(rec[2][0])+" -> "+str(rec[3][0]) +lableStr +" [color=grey];\n")
    # Print node infomation
    for key in Hast_label:
        Ft.write(" " + str(key) +" "+'[label="' + Hast_label[key][0] +'"];\n ')
    Ft.write("}")
    Ft.close()



    reac_rec_tot_dump = copy.deepcopy(reac_rec_tot)
    # Remove junk reactions
   #for i in range(len(reac_rec_tot)):
   #    print(reac_rec_tot[i])

   #for i in reac_rec_tot_dump:
   #    print("=========")
   #    for rec in i:
   #        print(rec)



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
#   fnames = ["./examples/hello5.xyz",
#             "./examples/hello6.xyz"]
    fnames = ["./examples/test-2.xyz"]
    ftempnames=["file1.txt",  
                "file2.txt",  
                "file3.txt",  
                "file4.txt",  
                "file5.txt",  
                "file6.txt",  
                "file7.txt",  
                "file8.txt",  
                "file9.txt",  
                "file10.txt"] 

#    trackList =["MMH","NO2","N2","a","b","c","e","f"]
#    ftempnames=["file1.txt","file2.txt"]
    trackList =["methane","oxygen",".OOH",".CH3"]


# +++++++++++++++++++++++++++++++++++++++++++++++++++
    if (analy_mode == 2 or analy_mode == 1):
        tempList1 = trackBlocks(fnames,trackList)
    if (analy_mode == 3):
        tempList1=[]
        for ftname in ftempnames:
            with open(ftname, 'rb') as f:
                tl = pickle.load(f)
                tempList1.extend(tl)
    if(analy_mode !=2 ):
        reactionGen(tempList1)
