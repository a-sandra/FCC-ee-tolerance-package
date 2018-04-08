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
from scipy import linalg
import madx_param
from class_twiss_table import TwissTable

#------------- Get the cut-off for the svd --------------------

nb_sg=float(sys.argv[1])
print nb_sg

#------------- Functions -------------------------------------
def make_name(a,b):
    return a+"="+str(b)+";"

#------------- Check wether there is already a str file for skew from a previous step -------------
try:
    with open('temp_multipole.str') as file:
        str_temp=np.genfromtxt("temp_multipole.str")
except IOError as e:
    str_temp=np.zeros(1176)

#-------------------------- Get the relative phase advances from twiss file ------------------------------------------
bare=TwissTable("/afs/cern.ch/user/s/saumon/FCCee/TLEP_lattice_version/ko_175_t_85/lattice/twiss_bare_bpm.twiss")
#muy0=bare.get_muy()
#mux0=bare.get_mux()
dx0=bare.get_dx()

pert_optics=TwissTable("beat.twiss")

#muy=pert_optics.get_muy()
#mux=pert_optics.get_mux()
dx=pert_optics.get_dx()

#phase_advance=np.concatenate((muy-muy0,mux-mux0,dx-dx0),axis=0)
phase_advance=np.concatenate(dx-dx0,axis=0)

print phase_advance.shape
print phase_advance
print "read data phase advance ok"

print "load response matrix"

#-------------------------- Solve the system ------------------------------------------
path="/afs/cern.ch/user/s/saumon/FCCee/correction_scheme/correction_scheme_ko/beta_beat_correction/response_matrix_w_sextupole/build/"
file_resp="respmat_dx.txt"

resp_mat=np.genfromtxt(path+file_resp, delimiter=",", dtype='float')

print "load response matrix ok"
print "solve the system"

x=np.linalg.lstsq(resp_mat, -phase_advance, rcond=nb_sg)

print "solve the system ok"
print x[0]

k1_str=x[0]/2.0+str_temp

ku_name=["KQU"+str(i) for i in np.arange(1,1169)]
ksy_name=["KSYQU"+str(i) for i in np.arange(1,9)]
k1name=np.concatenate((ku_name,ksy_name), axis=0)

correction=[make_name(ai,bi) for ai,bi in zip(k1name,k1_str)]

strfile = open('quad_multipole.str','wr')
for line in correction:
    strfile.write(line+"\n")
strfile.close()

np.savetxt("temp_multipole.str", k1_str, fmt='%.18e', delimiter=',')

print "PRAISE THE SUN \[T]/"

sys.exit()