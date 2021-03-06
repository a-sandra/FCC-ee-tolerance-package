#!/usr/bin/env python

__author__ = 'sandra'

# Python packages
import os
import sys
sys.path.append('/afs/cern.ch/user/s/saumon/FCCee/packages/python/madx_parameter/')
sys.path.append('/afs/cern.ch/user/s/saumon/FCCee/packages/python/metaclass/')
sys.path.append('/afs/cern.ch/user/s/saumon/FCCee/packages/python/classtwisstable/')
import numpy as np
import io
import re
from metaclass import twiss
#from scipy import linalg

#------------- Get the cut-off for the svd --------------------

nb_sg=float(sys.argv[1])
print nb_sg

#------------- Functions -------------------------------------
def make_name(a,b):
    return "KQTS"+str(a)+"="+str(b)+";"

#------------- Check wether there is already a str file for skew from a previous step -------------
try:
    with open('temp.str') as file:
        str_temp=np.genfromtxt("temp.str")
except IOError as e:
    str_temp=np.zeros(1184)

#-------------------------- Get the RDT from twiss file ------------------------------------------

tab=twiss("twiss_coupling.twiss")
tab.Cmatrix()

#-------------------------- Assemble the rdt list to correct -------------------------------------

difference=np.array([tab.F1001R,tab.F1001I])
addit=np.array([tab.F1010R,tab.F1010I])
#optics=np.genfromtxt("twiss_coupling.twiss",dtype=None,skip_header=47)
#dy_tab=optics['f12']

sol=np.concatenate((difference.flatten(),addit.flatten()),axis=0)
#sol=np.concatenate((difference.flatten(),addit.flatten(),dy_tab.flatten()),axis=0)
#print dy_tab
#print sol
#----------------------------- Compute the solution --------------------------------------------
print "sol sys"
matrdt=np.genfromtxt("/afs/cern.ch/user/s/saumon/FCCee/correction_scheme/correction_scheme_ko/batch_rm_rdt/1176_skews/rdt_respmat_skewonallsext_ip.txt", delimiter=",", dtype='float')
print "load matrix"
resulting_solution=np.linalg.lstsq(matrdt, -sol, rcond=nb_sg)
print resulting_solution[0]

#----- Tricky part, the strength of the skew from the correction should be, in principle added to the previous correction step. -----

 # strength from the previous iteration of coupling correction. just the number, without the name of the strength.
#skew_str=resulting_solution[0] #str_temp # I add then to my solution.
#skew_str=resulting_solution[0]+str_temp # I add then to my solution.

if str_temp.shape[0]==1184:
  skew_str=resulting_solution[0]+str_temp
else:
  skew_str=resulting_solution[0]+np.concatenate((str_temp, np.zeros(8)), axis=0)

liste=np.arange(1,1185)
correction=[make_name(ai,bi) for ai,bi in zip(liste,skew_str)]

strfile = open('skew.str','wr')
for line in correction:
    strfile.write(line+"\n")
strfile.close()

#np.savetxt("temp.str", resulting_solution[0], fmt='%.18e', delimiter=',')
np.savetxt("temp.str", skew_str, fmt='%.18e', delimiter=',')

print "PRAISE THE SUN"

sys.exit()