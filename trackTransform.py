from tools import *
import json
import pickle
import copy

def trackSpec(ftempnames,trackList):
    List = [["a" for i in range(1)] for i in range(len(trackList))]
    LastFrame = []
    # Open different files
    for ftname in ftempnames:
        tempList = []
        print(ftname)
        with open(ftname, 'rb') as f:
            tl = pickle.load(f)
            tempList.extend(tl)
        for rec in tempList:
            i = 0
            for itm in trackList:
                for rcd in GroupRec_dict:
                    if abs(GroupRec_dict[rcd]-rec[itm][1])<0.00001 :
                        if (rcd != List[i][-1]):
                            List[i].append(rcd)
                i = i+1
            LastFrame = rec
                



#   for rec in tempList:
#       i = 0
#       for itm in trackList:
#           # Translate Grp to Name 
#           for rcd in GroupRec_dict:
#               if abs(GroupRec_dict[rcd]-rec[itm][1])<0.00001 :
#                   if (rcd != List[i][-1]):
#                       List[i].append(rcd)
#           i = i+1
    Ft = open("SpecTrac.txt", 'wb')
    pickle.dump(List, Ft)
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


#   for ftname in ftempnames:
#       with open(ftname, 'rb') as f:
#           tl = pickle.load(f)
#           tempList1.extend(tl)
            
    trackSpec(ftempnames,trackList)

