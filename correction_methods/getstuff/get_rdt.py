#!/usr/bin/env python

__author__ = 'sandra'

# Python packages
import sys, os
import numpy as np
sys.path.append('/afs/cern.ch/user/s/saumon/FCCee/packages/python/madx_parameter/')
sys.path.append('/afs/cern.ch/user/s/saumon/FCCee/packages/python/metaclass/')
sys.path.append('/afs/cern.ch/user/s/saumon/FCCee/packages/python/classtwisstable/')
from metaclass import twiss
from madx_param import madxParams
from class_twiss_table import TwissTable

# Functions
def Cminus(f):
    a=twiss(f)
    a.Cmatrix()
    abs_f1001=np.sqrt((a.F1001R)*(a.F1001R)+(a.F1001I)*(a.F1001I))
    abs_f1010=np.sqrt((a.F1010R)*(a.F1010R)+(a.F1010I)*(a.F1010I))
    Cm=1-1/(1+4*((abs_f1001)*(abs_f1001)-(abs_f1010)*(abs_f1010)))
    return Cm

# Some initializations
filename=sys.argv[1]
stat=sys.argv[2]
print stat

# Read the twiss file - Extract the data
##Compute coupling
xf=twiss("twiss_coupling.twiss")
xf.Cmatrix()
## Compute the coupling strength C-
Cm=np.std(Cminus("twiss_coupling.twiss"))
# Retrieve the vertical dispersion RMS
y=madxParams('twiss_coupling.twiss')
dy_rms=y.get_value("DYRMS")

# Write to files
ff=file("dyrms_"+stat+".txt",'a')
ff.write("%.10f\n"%dy_rms)
ff.close()

f=file("re_f1001_"+stat+".txt",'a')
f.write("%.10f\n"%np.std(xf.F1001R))
f.close()

g=file("im_f1001_"+stat+".txt",'a')
#np.savetxt(f,dy_rms)
g.write("%.10f\n"%np.std(xf.F1001I))
g.close()

j=file("re_f1010_"+stat+".txt",'a')
#np.savetxt(f,dy_rms)
j.write("%.10f\n"%np.std(xf.F1010R))
j.close()

q1=file("im_f1010_"+stat+".txt",'a')
#np.savetxt(f,dy_rms)
q1.write("%.10f\n"%np.std(xf.F1010I))
q1.close()

h=file("cm_"+stat+".txt",'a')
#np.savetxt(f,dy_rms)
h.write("%.10f\n"%Cm)
h.close()

sys.exit()