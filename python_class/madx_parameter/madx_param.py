import sys
import os
import numpy as np

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