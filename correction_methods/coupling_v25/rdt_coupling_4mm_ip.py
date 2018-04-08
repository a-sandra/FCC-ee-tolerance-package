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
from numpy.linalg import inv

#------------- Get the cut-off for the svd --------------------

nb_sg=float(sys.argv[1])
#print nb_sg

#------------- Functions -------------------------------------
def make_name(a,b):
    return "KQTS"+str(a)+"="+str(b)+";"

def make_name_sy(a,b):
    return "KQTSY"+str(a)+"="+str(b)+";"

def make_name_ip(a,b):
    return "KIPQTS"+str(a)+"="+str(b)+";"
  
#------------- Check wether there is already a str file for skew from a previous step -------------
try:
    with open('temp.str') as file:
        str_temp=np.genfromtxt("temp.str")  
except IOError as e:
    str_temp=np.zeros(1203) #str_temp=np.zeros(1184)

print str_temp, str_temp.shape

#----------------------------------------- IP -----------------------------------------------------

zero_for_conc = np.zeros(19)
if str_temp.shape[0] != 1203:
  tt=np.concatenate((str_temp,zero_for_conc), axis=0)
  print "tt"
  str_temp=tt
  print str_temp

#np.savetxt("file.txt",str_tempo, fmt='%.18e')

#-------------------------- Get the RDT from twiss file ------------------------------------------

tab=twiss("twiss_coupling.twiss")
tab.Cmatrix()

#-------------------------- Assemble the rdt list to correct -------------------------------------

difference=np.array([tab.F1001R,tab.F1001I])
addit=np.array([tab.F1010R,tab.F1010I])

sol=np.concatenate((difference.flatten(),addit.flatten()),axis=0)
print sol

#----------------------------- Compute the solution --------------------------------------------
print "solve system"
matrdt=np.genfromtxt("/afs/cern.ch/work/s/saumon/__response_matrix/coupling_v205_4mm/rdt_arc_sy_ip_response_matrix_v205_4mm.txt", delimiter=",", dtype='float')

print "load response matrix"
resulting_solution=np.linalg.lstsq(matrdt, -sol, rcond=nb_sg)
print resulting_solution[0]

#----- Tricky part, the strength of the skew from the correction should be, in principle added to the previous correction step. -----
 # strength from the previous iteration of coupling correction. just the number, without the name of the strength.
#skew_str=resulting_solution[0] #str_temp # I add then to my solution.
# 21 august 2017

print resulting_solution[0].shape, str_temp.shape
skew_str=resulting_solution[0]+str_temp # I add then to my solution.

#----------------------------- Assign skew strength --------------------------------------------

skew_exc_ip=skew_str[:-19]
skew_arc=skew_exc_ip[:-8]
skew_sy=skew_exc_ip[-8:]
skew_ip = skew_str[-19:]

liste=np.arange(1,1177)
correction=[make_name(ai,bi) for ai,bi in zip(liste, skew_arc)]
correction_sy=[make_name_sy(ai,bi) for ai,bi in zip(np.arange(1,9), skew_sy)]
correction_ip=[make_name_ip(ai,bi) for ai,bi in zip(np.arange(1,20), skew_ip)]

print len(correction), len(correction_sy), len(correction_ip)

#----------------------------- Export strength  -----------------------------------------------

strfile = open('skew.str','wr')
for line in correction:
    strfile.write(line+"\n")

for line in correction_sy:
    strfile.write(line+"\n")

for line in correction_ip:
    strfile.write(line+"\n")
strfile.close()

np.savetxt("temp.str", skew_str, fmt='%.18e', delimiter=',')

print "PRAISE THE SUN"

sys.exit()