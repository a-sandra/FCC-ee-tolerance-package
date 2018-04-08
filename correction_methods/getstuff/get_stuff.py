#!/usr/bin/env python

__author__ = 'sandra'

# Python packages
import sys, os
import numpy as np
sys.path.append('/afs/cern.ch/user/s/saumon/FCCee/packages/python/madx_parameter/')
sys.path.append('/afs/cern.ch/user/s/saumon/FCCee/packages/python/metaclass/')
sys.path.append('/afs/cern.ch/user/s/saumon/FCCee/packages/python/classtwisstable/')
from metaclass import twiss
import madx_param
from class_twiss_table import TwissTable

filename=sys.argv[1]
print filename
stat=sys.argv[2]
print stat
# Read the twiss file

class madxParams:
    def __init__(self,filename):
        self.settings={}
        self.read_header(filename)
    def read_header(self, filename):
        myFile=open(filename,"r")
        for line in myFile.readlines():
            lineList=line.split()
            if lineList[0]=="@":
                if lineList[2]=='%le':
                    self.settings[lineList[1]]=float(lineList[3])
                else:
                    self.settings[lineList[1]]=lineList[3]
    def get_value(self, paramName):
        if paramName in self.settings.keys():
            return self.settings[paramName]
        else:
            raise KeyError('undefined config parameter %s' % paramName)

def return_header_value(filename, label):
    thing=madxParams(filename)
    return thing.get_value(label)

dy_rms=return_header_value(filename, "DYRMS")
print dy_rms
f=file("dyrms_"+stat+".txt",'a')
#np.savetxt(f,dy_rms)
f.write("%.10f\n"%dy_rms)
f.close()

y_rms=return_header_value(filename, "YCORMS")
print y_rms
g=file("yrms_"+stat+".txt",'a')
#np.savetxt(f,dy_rms)
g.write("%.10f\n"%y_rms)
g.close()

x_rms=return_header_value(filename, "XCORMS")
print x_rms
xf=file("xrms_"+stat+".txt",'a')
#np.savetxt(f,dy_rms)
xf.write("%.10f\n"%x_rms)
xf.close()

tune1=return_header_value(filename, "Q1")
print tune1
q1=file("q1_"+stat+".txt",'a')
#np.savetxt(f,dy_rms)
q1.write("%.10f\n"%tune1)
q1.close()

tune2=return_header_value(filename, "Q2")
print tune2
q2=file("q2_"+stat+".txt",'a')
#np.savetxt(f,dy_rms)
q2.write("%.10f\n"%tune2)
q2.close()

sys.exit()