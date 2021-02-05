"""
CPX-MechGen: 
Discover reaction mechanism from complex reaction network.

-Author      : Chen Xin
-Email       : chenxin199261@gmail.com
-Create Date : 2021/2/4 
-Inputs:
    1. Multiple spec-rev*.data  fill their paths in variable 'fnames'.

-Outputs:
    1. recordFile  : step, #of species.

"""

import os

def analy_specs(files):
    totstep = 0
    Rec=[]
    for fname in fnames:
        with  open(fname,'r') as f:
            Lines = f.readlines()
            totstep_file = 0
            for line in Lines:
                rec = list(map(int, line.split() ))  
                if(len(rec)==1):
                    totstep_file = totstep_file + rec[0] 
                if(len(rec)>1):
                    rec[0] = rec[0] + totstep
                    Rec.append(rec)
            totstep = totstep + totstep_file

    for i in Rec:
        print(i)

    print(totstep_file)






if __name__ == "__main__":
    fnames=[  "spec-rev1.data",  
              "spec-rev2.data",  
              "spec-rev3.data",  
              "spec-rev4.data",  
              "spec-rev5.data",  
              "spec-rev6.data",  
              "spec-rev7.data",  
              "spec-rev8.data",  
              "spec-rev9.data",  
              "spec-rev10.data",  
              "spec-rev11.data",  
              "spec-rev12.data",  
              "spec-rev13.data",  
              "spec-rev14.data",  
              "spec-rev15.data",  
              "spec-rev16.data",  
              "spec-rev17.data",  
              "spec-rev18.data",  
              "spec-rev19.data",  
              "spec-rev20.data"] 
    analy_specs(fnames) 
