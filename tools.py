"""
A union-find disjoint set data structure.

"""

# 2to3 sanity
from __future__ import (
    absolute_import, division, print_function, unicode_literals,
)

# Third-party libraries
import numpy as np
import math
class groupSplit(object):
    """Union-find disjoint sets datastructure.

    Union-find is a data structure that maintains disjoint set
    (called connected components or components in short) membership,
    and makes it easier to merge (union) two components, and to find
    if two elements are connected (i.e., belong to the same
    component).

    This implements the "weighted-quick-union-with-path-compression"
    union-find algorithm.  Only works if elements are immutable
    objects.

    Worst case for union and find: :math:`(N + M \log^* N)`, with
    :math:`N` elements and :math:`M` unions. The function
    :math:`\log^*` is the number of times needed to take :math:`\log`
    of a number until reaching 1. In practice, the amortized cost of
    each operation is nearly linear [1]_.

    Terms
    -----
    Component
        Elements belonging to the same disjoint set

    Connected
        Two elements are connected if they belong to the same component.

    Union
        The operation where two components are merged into one.

    Root
        An internal representative of a disjoint set.

    Find
        The operation to find the root of a disjoint set.

    Parameters
    ----------
    elements : NoneType or container, optional, default: None
        The initial list of elements.

    Attributes
    ----------
    n_elts : int
        Number of elements.

    n_comps : int
        Number of distjoint sets or components.

    Implements
    ----------
    __len__
        Calling ``len(uf)`` (where ``uf`` is an instance of ``UnionFind``)
        returns the number of elements.

    __contains__
        For ``uf`` an instance of ``UnionFind`` and ``x`` an immutable object,
        ``x in uf`` returns ``True`` if ``x`` is an element in ``uf``.

    __getitem__
        For ``uf`` an instance of ``UnionFind`` and ``i`` an integer,
        ``res = uf[i]`` returns the element stored in the ``i``-th index.
        If ``i`` is not a valid index an ``IndexError`` is raised.

    __setitem__
        For ``uf`` and instance of ``UnionFind``, ``i`` an integer and ``x``
        an immutable object, ``uf[i] = x`` changes the element stored at the
        ``i``-th index. If ``i`` is not a valid index an ``IndexError`` is
        raised.

    .. [1] http://algs4.cs.princeton.edu/lectures/

    """

    def __init__(self, linkMat):
        self.n_elts = 0  # current num of elements
        self.n_comps = 0  # the number of disjoint sets or components
        self._next = 0  # next available id
        self._elts = []  # the elements
        self._indx = {}  #  dict mapping elt -> index in _elts
        self._par = []  # parent: for the internal tree structure
        self._siz = []  # size of the component - correct only for roots


        dim = len(linkMat)
        for elt in range(dim):
            self.add(elt+1)
        for i in range(dim):
            for j in range(i):
                if linkMat[i][j] ==1 :
                    self.union(i+1,j+1)
				

		# Union from link matrix


    def __repr__(self):
        return  (
            '<UnionFind:\n\telts={},\n\tsiz={},\n\tpar={},\nn_elts={},n_comps={}>'
            .format(
                self._elts,
                self._siz,
                self._par,
                self.n_elts,
                self.n_comps,
            ))

    def __len__(self):
        return self.n_elts

    def __contains__(self, x):
        return x in self._indx

    def __getitem__(self, index):
        if index < 0 or index >= self._next:
            raise IndexError('index {} is out of bound'.format(index))
        return self._elts[index]

    def __setitem__(self, index, x):
        if index < 0 or index >= self._next:
            raise IndexError('index {} is out of bound'.format(index))
        self._elts[index] = x

    def add(self, x):
        """Add a single disjoint element.

        Parameters
        ----------
        x : immutable object

        Returns
        -------
        None

        """
        if x in self:
            return
        self._elts.append(x)
        self._indx[x] = self._next
        self._par.append(self._next)
        self._siz.append(1)
        self._next += 1
        self.n_elts += 1
        self.n_comps += 1

    def find(self, x):
        """Find the root of the disjoint set containing the given element.

        Parameters
        ----------
        x : immutable object

        Returns
        -------
        int
            The (index of the) root.

        Raises
        ------
        ValueError
            If the given element is not found.

        """
        if x not in self._indx:
            raise ValueError('{} is not an element'.format(x))

        p = self._indx[x]
        while p != self._par[p]:
            # path compression
            q = self._par[p]
            self._par[p] = self._par[q]
            p = q
        return p

    def connected(self, x, y):
        """Return whether the two given elements belong to the same component.

        Parameters
        ----------
        x : immutable object
        y : immutable object

        Returns
        -------
        bool
            True if x and y are connected, false otherwise.

        """
        return self.find(x) == self.find(y)

    def union(self, x, y):
        """Merge the components of the two given elements into one.

        Parameters
        ----------
        x : immutable object
        y : immutable object

        Returns
        -------
        None

        """
        # Initialize if they are not already in the collection
        for elt in [x, y]:
            if elt not in self:
                self.add(elt)

        xroot = self.find(x)
        yroot = self.find(y)
        if xroot == yroot:
            return
        if self._siz[xroot] < self._siz[yroot]:
            self._par[xroot] = yroot
            self._siz[yroot] += self._siz[xroot]
        else:
            self._par[yroot] = xroot
            self._siz[xroot] += self._siz[yroot]
        self.n_comps -= 1

    def component(self, x):
        """Find the connected component containing the given element.

        Parameters
        ----------
        x : immutable object

        Returns
        -------
        set

        Raises
        ------
        ValueError
            If the given element is not found.

        """
        if x not in self:
            raise ValueError('{} is not an element'.format(x))
        elts = np.array(self._elts)
        vfind = np.vectorize(self.find)
        roots = vfind(elts)
        return set(elts[roots == self.find(x)])

    def components(self):
        """Return the list of connected components.

        Returns
        -------
        list
            A list of sets.

        """
        elts = np.array(self._elts)
        vfind = np.vectorize(self.find)
        roots = vfind(elts)
        distinct_roots = set(roots)
        return [set(elts[roots == root]) for root in distinct_roots]
        # comps = []
        # for root in distinct_roots:
        #     mask = (roots == root)
        #     comp = set(elts[mask])
        #     comps.append(comp)
        # return comps

    def component_mapping(self):
        """Return a dict mapping elements to their components.

        The returned dict has the following semantics:

            `elt -> component containing elt`

        If x, y belong to the same component, the comp(x) and comp(y)
        are the same objects (i.e., share the same reference). Changing
        comp(x) will reflect in comp(y).  This is done to reduce
        memory.

        But this behaviour should not be relied on.  There may be
        inconsitency arising from such assumptions or lack thereof.

        If you want to do any operation on these sets, use caution.
        For example, instead of

        ::

            s = uf.component_mapping()[item]
            s.add(stuff)
            # This will have side effect in other sets

        do

        ::

            s = set(uf.component_mapping()[item]) # or
            s = uf.component_mapping()[item].copy()
            s.add(stuff)

        or

        ::

            s = uf.component_mapping()[item]
            s = s | {stuff}  # Now s is different

        Returns
        -------
        dict
            A dict with the semantics: `elt -> component contianing elt`.

        """
        elts = np.array(self._elts)
        vfind = np.vectorize(self.find)
        roots = vfind(elts)
        distinct_roots = set(roots)
        comps = {}
        for root in distinct_roots:
            mask = (roots == root)
            comp = set(elts[mask])
            comps.update({x: comp for x in comp})
            # Change ^this^, if you want a different behaviour:
            # If you don't want to share the same set to different keys:
            # comps.update({x: set(comp) for x in comp})
        return comps

ELEMENTS_dict = {
        'GHOST':  0, 'H'    :  1, 'He'   :  2, 'Li'   :  3, 'Be'   :  4,
        'B'    :  5, 'C'    :  6, 'N'    :  7, 'O'    :  8, 'F'    :  9,
        'Ne'   : 10, 'Na'   : 11, 'Mg'   : 12, 'Al'   : 13, 'Si'   : 14,
        'P'    : 15, 'S'    : 16, 'Cl'   : 17, 'Ar'   : 18, 'K'    : 19,
        'Ca'   : 20, 'Sc'   : 21, 'Ti'   : 22, 'V'    : 23, 'Cr'   : 24,
        'Mn'   : 25, 'Fe'   : 26, 'Co'   : 27, 'Ni'   : 28, 'Cu'   : 29,
        'Zn'   : 30, 'Ga'   : 31, 'Ge'   : 32, 'As'   : 33, 'Se'   : 34,
        'Br'   : 35, 'Kr'   : 36, 'Rb'   : 37, 'Sr'   : 38, 'Y'    : 39,
        'Zr'   : 40, 'Nb'   : 41, 'Mo'   : 42, 'Tc'   : 43, 'Ru'   : 44,
        'Rh'   : 45, 'Pd'   : 46, 'Ag'   : 47, 'Cd'   : 48, 'In'   : 49,
        'Sn'   : 50, 'Sb'   : 51, 'Te'   : 52, 'I'    : 53, 'Xe'   : 54,
        'Cs'   : 55, 'Ba'   : 56, 'La'   : 57, 'Ce'   : 58, 'Pr'   : 59,
        'Nd'   : 60, 'Pm'   : 61, 'Sm'   : 62, 'Eu'   : 63, 'Gd'   : 64,
        'Tb'   : 65, 'Dy'   : 66, 'Ho'   : 67, 'Er'   : 68, 'Tm'   : 69,
        'Yb'   : 70, 'Lu'   : 71, 'Hf'   : 72, 'Ta'   : 73, 'W'    : 74,
        'Re'   : 75, 'Os'   : 76, 'Ir'   : 77, 'Pt'   : 78, 'Au'   : 79,
        'Hg'   : 80, 'Tl'   : 81, 'Pb'   : 82, 'Bi'   : 83, 'Po'   : 84,
        'At'   : 85, 'Rn'   : 86, 'Fr'   : 87, 'Ra'   : 88, 'Ac'   : 89,
        'Th'   : 90, 'Pa'   : 91, 'U'    : 92, 'Np'   : 93, 'Pu'   : 94,
        'Am'   : 95, 'Cm'   : 96, 'Bk'   : 97, 'Cf'   : 98, 'Es'   : 99,
        'Fm'   :100, 'Md'   :101, 'No'   :102, 'Lr'   :103, 'Rf'   :104,
        'Db'   :105, 'Sg'   :106, 'Bh'   :107, 'Hs'   :108, 'Mt'   :109,
        'E110' :110, 'E111' :111, 'E112' :112, 'E113' :113, 'E114' :114,
        'E115' :115, 'E116' :116, 'E117' :117, 'E118' :118 }

radii_dict = {
        'H': 0.32,    'C': 0.67,   'N':  0.65,   'O':  0.57
}

mass_dict = {
        'H': 1.008,    'C': 12.011,   'N':  14.007,   'O':  15.999
}

Inter_dict ={"(OOH)2":241.00875,
             "OO+OOH":247.89013,
             "CH4+O2": 46.01147,
             "CH3+O2": 48.57280,
             "(CH3)2":  9.25338}

Trans_dict =    {"methane": 2.88153,"OH."  : 3.88934,"CH3OH" : 11.78743,"MMH"    :38.22148,
                 "oxygen" :15.96772,"H2"   : 0.12674,"CH2OH" : 12.37290, "CH3-N-NH2":39.51493,
                 "CH3NHNH" :39.61882,"CH3NNH": 40.95882,"NO2":59.60995,"HONO":57.95407,
                 "N2":13.97126,"HNO2":57.66979,
                 ".OOH"   :15.52446,"HCO"  :13.29264,"C2H4"  : 10.13715,"O+O"    : 15.99900,
                 ".CH3"   : 3.04194,"O=CH2":12.72717,"CH3OO.": 48.40383,"O3-lin" : 63.74350,
                 "water"  : 3.77359,"H"    : 1.00399,".OOH"  : 15.52446,"O3-tri" : 63.63360,
                 "CO2"    :55.15826,"O"    : 3.99987,"CH3OOH": 47.06011,"CH3CH3" :  9.19653,
                 "CO"     :13.82621,"HCOOH":51.54219,"HOCH"  : 12.92288,"HOOH"   : 15.09337,
                 "CH3ONO"  :191.0259164,  "CH3NO2":180.60540827,  "CH2-NN-NH":41.589125,
                 "CH2=N-NH2":41.478809,
                 "NH3": 3.361201,"CH2-NH" : 11.516598,
                 "CH2-N" :  11.903213,"CH3-O.": 12.125209,
                 "HCN" : 12.432577,"N-NH2" : 13.041992,
                 "NH-NH": 13.080274,"N-NH": 13.518529,
                 "NH2O": 13.943739,"N+N": 13.971258,
                 "ONH": 14.452812,"N+O":14.936465,
                 "CH2-NH-NH2":40.122307,"CH3-NH-N": 40.946319,"CH-NH-NH2":41.907775,
                 "CH2=N-NH2(3)": 41.329115,"NH-CH2-NH": 41.452186,"CH2-N-NH":42.851207,
                 "CH3NN(2)":42.185077,"CH3NN":42.330582,
                 "CH2=N-NH2(2)":42.994458,"CH2-N-N": 44.434385,"CH-N-NH2":43.323556,
                 "CH-N-NH": 44.906605,"CH3-NO":45.255115,"CH-NN":46.410566,
                 "CH2-NO":47.504253,"HN-CO": 49.917573,
                 "HONO-ts": 54.236561,"NNO": 55.757821,"NO2-v1":59.509149,
                 "OH-NH-O":56.067167,"CH3-CH2-NH-NH": 125.805874,
                 "CH3-NN-CH3":128.254585,"CH3-NH-NO":163.412291,
                 "CH3-NO-NH":163.452963,"CH2OH-N-NH": 166.659613,"CH3-NH-NH-OH":153.693835,
                 "CHO-NH-NH2": 167.146396,"CH2-N-NOH": 171.556713,"CH3-NH-NHO":158.087044,
                 "CH2-NO2": 189.581673,"HNO3": 231.286441,".CH2O-NH-NH2":159.979330,"CH2ONO":189.669736,
                 "CH3-NH-NH-CHO": 523.184031,"CH3-N(NH2)-NO": 588.679275,"CH3-NH-NH-NO": 590.122697,
                 "MMH-v":38.07003,"MMH-NO2":2200.18899,"MMH-NO2-v1":2200.605753} 
GroupRec_dict = {"methane": 2.88153,"OH."  : 3.88934,"CH3OH" : 11.78743,"MMH"    :38.22148,
                 "oxygen" :15.96772,"H2"   : 0.12674,"CH2OH" : 12.37290, "CH3-N-NH2":39.51493,
                 "CH3NHNH" :39.61882,"CH3NNH": 40.95882,"NO2":59.60995,"HONO":57.95407,
                 "N2":13.97126,"HNO2":57.66979,
                 ".OOH"   :15.52446,"HCO"  :13.29264,"C2H4"  : 10.13715,"O+O"    : 15.99900,
                 ".CH3"   : 3.04194,"O=CH2":12.72717,"CH3OO.": 48.40383,"O3-lin" : 63.74350,
                 "water"  : 3.77359,"H"    : 1.00399,".OOH"  : 15.52446,"O3-tri" : 63.63360,
                 "CO2"    :55.15826,"O"    : 3.99987,"CH3OOH": 47.06011,"CH3CH3" :  9.19653,
                 "CO"     :13.82621,"HCOOH":51.54219,"HOCH"  : 12.92288,"HOOH"   : 15.09337,
                 "CH3ONO"  :191.0259164,  "CH3NO2":180.60540827,  "CH2-NN-NH":41.589125,
                 "CH2=N-NH2":41.478809,
                 "NH3": 3.361201,"CH2-NH" : 11.516598,
                 "CH2-N" :  11.903213,"CH3-O.": 12.125209,
                 "HCN" : 12.432577,"N-NH2" : 13.041992,
                 "NH-NH": 13.080274,"N-NH": 13.518529,
                 "NH2O": 13.943739,"N+N": 13.971258,
                 "ONH": 14.452812,"N+O":14.936465,
                 "CH2-NH-NH2":40.122307,"CH3-NH-N": 40.946319,"CH-NH-NH2":41.907775,
                 "CH2=N-NH2(3)": 41.329115,"NH-CH2-NH": 41.452186,"CH2-N-NH":42.851207,
                 "CH3NN(2)":42.185077,"CH3NN":42.330582,
                 "CH2=N-NH2(2)":42.994458,"CH2-N-N": 44.434385,"CH-N-NH2":43.323556,
                 "CH-N-NH": 44.906605,"CH3-NO":45.255115,"CH-NN":46.410566,
                 "CH2-NO":47.504253,"HN-CO": 49.917573,
                 "HONO-ts": 54.236561,"NNO": 55.757821,"NO2-v1":59.509149,
                 "OH-NH-O":56.067167,"CH3-CH2-NH-NH": 125.805874,
                 "CH3-NN-CH3":128.254585,"CH3-NH-NO":163.412291,
                 "CH3-NO-NH":163.452963,"CH2OH-N-NH": 166.659613,"CH3-NH-NH-OH":153.693835,
                 "CHO-NH-NH2": 167.146396,"CH2-N-NOH": 171.556713,"CH3-NH-NHO":158.087044,
                 "CH2-NO2": 189.581673,"HNO3": 231.286441,".CH2O-NH-NH2":159.979330,"CH2ONO":189.669736,
                 "CH3-NH-NH-CHO": 523.184031,"CH3-N(NH2)-NO": 588.679275,"CH3-NH-NH-NO": 590.122697,
                 "MMH-v":38.07003,"MMH-NO2":2200.18899,"MMH-NO2-v1":2200.605753} 

Hast_label= {}


grp_dic = dict(zip(GroupRec_dict.values(), GroupRec_dict.keys())) 

def calcDist(atom1,atom2):
    dist = (atom1[1][0]-atom2[1][0])**2+(atom1[1][1]-atom2[1][1])**2+(atom1[1][2]-atom2[1][2])**2
    return dist**0.5 

def MolCenter(atomListSub):
    center=[0,0,0]
    nAtom = len(atomListSub)
    for atom in atomListSub:
        center[0]=center[0]+atom[1][0]/nAtom
        center[1]=center[1]+atom[1][1]/nAtom
        center[2]=center[2]+atom[1][2]/nAtom
    return center
def buildNeigh(atomList,cri):
    dim = len(atomList)
    for i in range(dim):
        for j in range(i):
            dist = calcDist(atomList[i],atomList[j])
            if(dist < cri):
                atomList[i][2].append(j)
                atomList[j][2].append(i)
    return atomList

def buildLinkMat(atomList,cri):
    dim = len(atomList)
    Matrix = [[0]*dim for i in range(dim)]
    for i in range(dim):
        rad1 = radii_dict[atomList[i][0]]
        for j in atomList[i][2]:
            dist = calcDist(atomList[i],atomList[j])
            rad2 = radii_dict[atomList[j][0]]
            if(dist < cri*(rad1+rad2)):
                Matrix[i][j]=Matrix[j][i]=1
        Matrix[i][i]=mass_dict[atomList[i][0]]
    return Matrix 

def buildLinkMatSub(atomList,cri):
    dim = len(atomList)
    Matrix = [[0]*dim for i in range(dim)]
    for i in range(dim):
        rad1 = radii_dict[atomList[i][0]]
        for j in range(i):
            dist = calcDist(atomList[i],atomList[j])
            rad2 = radii_dict[atomList[j][0]]
            if(dist < cri*(rad1+rad2)):
                Matrix[i][j]=Matrix[j][i]=1
        Matrix[i][i]=mass_dict[atomList[i][0]]
    return Matrix 

def groupOp(LinkMat):
    uf = groupSplit(LinkMat)
    MolRec = uf.components()
    nMol = len(MolRec)
    return nMol,MolRec

def BlockInfoUpdate(BlockList,atomList):
    for rec in BlockList:
        atomListSub = [0]*len(rec[1])
        j = 0
        for i in rec[1]:
            atomListSub[j] = atomList[i-1]
            j = j+1
        mat = np.array(buildLinkMatSub(atomListSub,1.6))
        rec[2]=atomListSub 
        rec[3]=abs(np.linalg.det(mat))**0.5
       #if(math.isnan(rec[3])):
       #    print("nananananan")
       #    rec[3]= 777.777
        rec[4]=MolCenter(atomListSub)

def SearchblockbyID(ID,blockList):
    n = len(blockList)
    first = 0
    last = n - 1
    while first <= last:
        mid = (last + first) // 2
        if blockList[mid][0] > ID:
            last = mid - 1
        elif blockList[mid][0] < ID:
            first = mid + 1
        else:
            return blockList[mid]
    return 0

def printUnknowStruc(blockList,atmList):
    printed=[]
    for blk in blockList:
        grpN = blk[3]
        inRec = False
        for rcd in GroupRec_dict:
            if abs(GroupRec_dict[rcd]-grpN)<0.00001:
                inRec = True
                break
        for rcd in Inter_dict:
            if abs(Inter_dict[rcd]-grpN)<0.00001:
                inRec = True
                break
        strGrp=format(grpN,".5f")
        if (not inRec) and ( not strGrp in printed):
            f = open("R"+strGrp+".xyz","w")
            f = open("UnknowRec.txt","w")
            f.write(str(len(blk[2]))+"\n")
            f.write(strGrp+"\n")
            for atom in blk[2]:
                f.write(atom[0]+"  "+str(atom[1][0])+"   "\
                                    +str(atom[1][1])+"   "\
                                    +str(atom[1][2])+"\n")
            f.close()
            printed.append(strGrp)
    return printed


def specCount(blockList,trackList):
    tracknum = [1]*len(trackList)
    Rec = [0]*len(trackList)
    for i in range(len(trackList)):
        tracknum[i] = Trans_dict[trackList[i]]
    for line in blockList:
        for i in range(len(trackList)):
            if(np.abs(line[3]-tracknum[i])<0.001):
                Rec[i] = Rec[i] +1
    return(Rec)



if __name__ == "__main__":
    atomList = [['H',[0,0,0]],['H',[0,0,1]],['H',[5,0,0]],['H',[4,0,0]]]
    level = 2.3
    Matrix = [[0]*dim for i in range(dim)]
    mat =  buildLinkMat(atomList,level)
    nMol,Mol,SubgroupNum = groupOp(mat)
#    print(mat)
#    print(nMol,Mol,SubgroupNum)
