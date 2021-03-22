from tools import *
import json
import pickle
import copy

def trackSpec(tempList,trackList):
    List = [["a" for i in range(1)] for i in range(len(trackList))]
    for rec in tempList:
        i = 0
        for itm in trackList:
            # Translate Grp to Name 
            for rcd in GroupRec_dict:
                if abs(GroupRec_dict[rcd]-rec[itm][1])<0.00001 :
                    if (rcd != List[i][-1]):
                        List[i].append(rcd)
            i = i+1
    Ft = open("SpecTrac.txt", 'wb')
    pickle.dump(tempList, Ft)
    Ft.close()

        


if __name__ == "__main__":
    """
    Track-SpeciesFlow
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
    # Track-AtomNumber
    trackList = range(2,17191,9)


    tempList1=[]
    for ftname in ftempnames:
        with open(ftname, 'rb') as f:
            tl = pickle.load(f)
            tempList1.extend(tl)
            
    trackSpec(tempList1,trackList)

