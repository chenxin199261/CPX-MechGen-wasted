import pickle
ftname = "/home/xchen/Downloads/SpecTrac.pk"
f =  open(ftname, 'rb')
Rec2 = pickle.load(f)
print(len(Rec2))
