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

def make_name_sy(a,b):
    return "KQTSY"+str(a)+"="+str(b)+";"

#------------- Check wether there is already a str file for skew from a previous step -------------
try:
    with open('temp.str') as file:
        str_temp=np.genfromtxt("temp.str")
except IOError as e:
    str_temp=np.zeros(1184)

if str_temp.shape[0] == 1203:
  str_temp=str_temp[:-19]
  print "tt"
  print str_temp

#-------------------------- Get the RDT from twiss file ------------------------------------------

tab=twiss("twiss_coupling.twiss")
tab.Cmatrix()

#-------------------------- Assemble the rdt list to correct -------------------------------------

difference=np.array([tab.F1001R,tab.F1001I])
addit=np.array([tab.F1010R,tab.F1010I])
optics=np.genfromtxt("twiss_coupling.twiss",dtype=None,skip_header=47)
dy_tab=optics['f12']

sol=np.concatenate((difference.flatten(),addit.flatten(),dy_tab.flatten()),axis=0)
print dy_tab
#print sol
#----------------------------- Compute the solution --------------------------------------------
print "sol sys"
matrdt=np.genfromtxt("/afs/cern.ch/work/s/saumon/__response_matrix/coupling_v205_4mm/rdt_dy_respmat_arc_sy_v205_4mm.txt", delimiter=",", dtype='float')
print "load matrix"
resulting_solution=np.linalg.lstsq(matrdt, -sol, rcond=nb_sg)
print resulting_solution[0]

#----- Tricky part, the strength of the skew from the correction should be, in principle added to the previous correction step. -----

#if str_temp.shape[0]==1184:
#  skew_str=resulting_solution[0]+str_temp[:-8]
#else:
#  skew_str=resulting_solution[0]+str_temp

 # strength from the previous iteration of coupling correction. just the number, without the name of the strength.
skew_str=resulting_solution[0]+str_temp # I add then to my solution.
#skew_str=resulting_solution[0]+str_temp[:-8] # I add then to my solution.

liste=np.arange(1,1177)
correction=[make_name(ai,bi) for ai,bi in zip(liste,skew_str[:-8])]

correction_sy=[make_name_sy(ai,bi) for ai,bi in zip(np.arange(1,9),skew_str[-8:])]

strfile = open('skew.str','wr')
for line in correction:
    strfile.write(line+"\n")
    
for line in correction_sy:
    strfile.write(line+"\n")
strfile.close()

#np.savetxt("temp.str", resulting_solution[0], fmt='%.18e', delimiter=',')
np.savetxt("temp.str", skew_str, fmt='%.18e', delimiter=',')

print "PRAISE THE SUN"

sys.exit()