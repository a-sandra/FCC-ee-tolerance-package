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
from time import sleep
from numpy.linalg import inv

nb_sg=float(sys.argv[1])
print nb_sg

weight=1.0

# Read the twiss file

def select_a_pattern(pattern, table, column2use):
    label_name=table['f'+str(column2use)]
    regexpr = re.compile(pattern)
    vmatch = np.vectorize(lambda x:bool(regexpr.match(x)))
    selection = vmatch(label_name)
    return table[selection]

sleep(0.05)
optics=np.genfromtxt("twiss_2_correct.twiss", dtype=None, skip_header=47)
matrdy=np.genfromtxt("/afs/cern.ch/user/s/saumon/FCCee/correction_scheme/correction_scheme_ko_205/response_matrix/no_sextupole/build_response_matrix_no_sextupole/resp_mat_dy_nosextupole_v205.out", delimiter=",", dtype='float')

matdy=matrdy
#maty=matry*(1-weight)

#try:
#    with open('kick.str') as file:
#        kicker_2_export=np.genfromtxt("kick.str", dtype='float')
#except IOError as e:
#    kicker_2_export=np.zeros(2006)

vert_corr_table=select_a_pattern('"MCV_*', optics, 0)
corrector_name=vert_corr_table['f0']
corr_name=[item[1:][:-1] for item in corrector_name ]
vert_bpm_table=select_a_pattern('"BPMV_*', optics, 0)
#y_co=vert_bpm_table['f2']*(1-0)
dy=vert_bpm_table['f3']
#Value of the kick from local disp correct.
vkick_value=vert_corr_table['f4']

#matrice2correct=np.concatenate((y_co,dy), axis=0) 
matrice2correct=dy
mat=matdy
#mat=np.concatenate((maty,matdy), axis=0) 

kicker_str_1=np.linalg.lstsq(mat, -matrice2correct, rcond=nb_sg)
kicker_strb=kicker_str_1[0]/1.0 # 5 was added because roll+transv. quad did not work 23oct 2017 # put it back to 1 after reducing the number of sg.
kicker_str=np.asarray(kicker_strb)

#kicker_str2_export=map(lambda i: corr_name[i]+"->KICK="+str(kicker_str[i]+kicker_2_export[i])+";", np.arange(2006))
kicker_str2_export=map(lambda i: corr_name[i]+"->KICK="+str(kicker_str[i]+vkick_value[i])+";", np.arange(1600))
#kicker_temp=map(lambda i: kicker_str[i]+kicker_2_export[i], np.arange(2006))

print kicker_str
print "GO THERE!"

strfile = open('kicker.str','wr')
for line in kicker_str2_export:
    strfile.write(line+"\n")
strfile.close()

sys.exit()