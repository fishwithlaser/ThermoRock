"""
Python 3.7 code to calculate rock-thermodynamic interactions

Written by:   thomas.kosciuch@mail.utoronto.ca
Adapted from: xu.chu@utoronto.ca
Metamorphic Petrology Lab @ the University of Toronto

Last updated: 02/25/2019
"""

#Directory Structure
#
#   python code
#           /XSLX/
#               xlsx files
# 

import sympy
import numpy as np         # dtypes
import os as os            # directory opperations
import sys                 # directory opperations
from numpy import linalg   # math
                           # Custom packages 
sys.path.append(os.path.join(sys.path[0],'mods'))
import metamathicCalc as calc #
import loader as loader    # loads data
import matrixOps as Ops    # matrix opperations

#loads inputs / database 
notKnown, minerals, thermody = loader.load()

CC=['  SiO2   ','  TiO2   ',' Al2O3   ','   FeO   ','   MgO   ','   MnO   ','   CaO   ','  Na2O   ','   K2O   ','     O   ','   H2O   ','   CO2   ',' Supl1   ',' Supl2   ']

def Rx(mins,CC=CC):
    """
    We check which minerals will react using a list of minerals inserted
    individually
    """
    # Loads datadrame
    notKnown, minerals, thermody = loader.load() 
    d = loader.minerals(mins, minerals, thermody)
    minNum        = len(mins)
    PHASE         = d
    endnum        = np.zeros(minNum+2)
    for i in range(0, minNum+2):
        target    = 'Mineral_' +  str(i)
        temp      = d.get(target)
        endnum[i] = len(temp.get('endmember'))
 
    minNum = len(mins)
    d = loader.minerals(mins, minerals, thermody)
    PHASE         = d
    endnum        = np.zeros(minNum+2)
    for i in range(0, minNum+2):
        target    = 'Mineral_' +  str(i)
        temp      = d.get(target)
        endnum[i] = len(temp.get('endmember'))


    A = Ops.compress(d, PHASE, CC)
    #sheinmark check
    C = len(np.transpose(A))
    A0 = np.transpose(A)                     # this is required for return
    P = len(A)
    # F = C - P + 2
    """ this needs to be 1 in order to plot univariant lines"""
    F = C - P + 2
    if F == 1:
        print ("did react: ", mins)
        A = np.transpose(A)
        A = sympy.Matrix(A).rref()
        index = list(range(0, minNum+1))
        react = A[0][index,5]
    return react, A0


