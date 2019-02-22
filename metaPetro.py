"""
Python 3.7 code to calculate rock-thermodynamic interactions

Written by:   thomas.kosciuch@mail.utoronto.ca
Adapted from: xu.chu@utoronto.ca
Metamorphic Petrology Lab @ the University of Toronto

Last updated: 02/11/2019
"""

#Directory Structure
#
#   python code
#           /XSLX/
#               xlsx files
# 

import scipy               # dtypes
import numpy as np         # dtypes
import pandas as pd        # dtypes n dataframes
import os as os            # directory opperations
import sys                 # directory opperations
import mysql.connector     # mySQL opperations
from numpy import linalg   # math
import xlrd                # xlsx opperations
import csv                 # csv opperations
                           # Custom packages 
sys.path.append(os.path.join(sys.path[0],'mods'))
import metamathicCalc as calc #
import loader as loader    # loads data
import matrixOps as Ops    # matrix opperations

#loads inputs / database 
notKnown, minerals, thermody = loader.load()

mins = [57, 138, 143, 105]
minNum = len(mins)

d = loader.minerals(mins, minerals) # loads populates database

# Initial Conditions
T_min   = 200
T_max   = 1000
P       = 2                         # [kbar]
res     = 101                       # resolution
TRange  = [T_min, T_max]
XCO2    = np.linspace(0,0.5, res)   # sets up plotting 
XCO2    = XCO2[1:res]               # removes final CO2 point
Phase   = mins                      # Sets up "Phase" variable to mimic MatLab
T       = [0] * res                 # creates empty matrix
# First guess for temperature
T_guess = (TRange[0]+TRange[1])/2   # guesses halfway between range
Xs      = [] 
CC=['  SiO2   ','  TiO2   ',' Al2O3   ','   FeO   ','   MgO   ','   MnO   ','   CaO   ','  Na2O   ','   K2O   ','     O   ','   H2O   ','   CO2   ',' Supl1   ',' Supl2   ']


PHASE         = d
endnum        = np.zeros(minNum+2)
for i in range(0, minNum+2):
    target    = 'Mineral_' +  str(i)
    temp      = d.get(target)
    endnum[i] = len(temp.get('endmember'))


A = Ops.compress(d, PHASE, CC)
A = np.transpose(A)
print(A)

# here I will try to copy line for lin whatever Xu does....
m = len(mins+1)
i = 1
j = 1
l = np.zeros( 1, m)

while i <= m:
    # partial pivot
    if j > n:
        React = 0
        A0 = A0*0
    p = abs(A([i,j]))
    q = i
    for k in range(i+1,m):
        if abs(A[k,j])>p:
            p    = abs(A[k,j]
            q    = k
    if abs(p)>1e-14:
        A_temp   = A[q,j:n]
        A[q,j:n] = A[i,j:n]
        A[i,j:n] = A_temp/A_temp[1] #?[1]? wtf
    #Gaussian Elimination?
        for k in range(i+1,m):
            A[k,:] = A[i,:] - A[i,:] * A[k,j]
        for k in range(1,i-1):
            A[k,:] = A[k,:] - A[i,:] * A[k,j]
        l[i] = j
    else: 
        A[i:m,j] = 0

    l[i] = j
    j = j + 1

l(m+1)=n+1;
