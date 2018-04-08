import sys
import os
import numpy as np

class TwissTable:
    def __init__(self,filename):
        self.optics={}
        self.rows={}
        self.column=[]
        myFile=open(filename,"r")
        proceed = False
        row = 0
        for line in myFile.readlines():
            lineList=line.split()
            if proceed:
                if not lineList[0] == "$":
                    self.rows[lineList[0]] = row
                    for i in range(len( self.column )):
                        try :
                            #print self.column[i], lineList[0], lineList[i]
                            self.optics[self.column[i]][row] = float(lineList[i])
                        except ValueError:
                            pass
                    row += 1
            
            if lineList[0]=="*":
                for name in lineList[1:]:
                    self.optics[name] = {}
                    #print name
                self.column = lineList[1:]
                proceed = True
    def get_s(self):
        return np.array(self.optics["S"].values())
    def get_betx(self):
        return np.array(self.optics["BETX"].values())
    def get_bety(self):
        return np.array(self.optics["BETY"].values())
    def get_dx(self):
        return np.array(self.optics["DX"].values())
    def get_dy(self):
        return np.array(self.optics["DY"].values())
    def get_y(self):
        return np.array(self.optics["Y"].values())
    def get_x(self):
        return np.array(self.optics["X"].values())
    def get_r11(self):
        return np.array(self.optics["R11"].values())
    def get_r12(self):
        return np.array(self.optics["R12"].values())
    def get_r21(self):
        return np.array(self.optics["R21"].values())
    def get_r22(self):
        return np.array(self.optics["R22"].values())
    def get_mux(self):
        return np.array(self.optics["MUX"].values())
    def get_muy(self):
        return np.array(self.optics["MUY"].values())
    def get_k1l(self):
        return np.array(self.optics["K1L"].values())
    def get_l(self):
        return np.array(self.optics["L"].values())
    def get_pt(self):
        return np.array(self.optics["PT"].values())
    def get_name(self):
        return np.array(self.optics["NAME"].values())