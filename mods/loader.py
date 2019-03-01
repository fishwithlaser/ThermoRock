from os import listdir
import csv
# required to load database file
import scipy                          #dtypes
import numpy as np                    #dtypes
import pandas as pd
import os as os                       # checks if exist for file writing
import mysql.connector

from numpy import linalg
import sys
from tqdm import tqdm                 # timing for large-calcs

#converts to CSV
import xlrd
import csv

### Converts XLSX sheets to CSV  ###
def change(folder = "XLSX", destination_folder = "csv"):
    ####################################
    ##  finds files in source folder  ##
    files = listdir(folder)            #
    path = folder + "/" + files[0]     #
    file = pd.ExcelFile(path)          #
    sheets = file.sheet_names          #
                                      ## 
    # loading:                     #####
    # checks for directory
    if os.path.isdir(destination_folder) == False:
        mkdir(destination_folder)
    # sheet 1
    notKnown = pd.read_excel(file,sheets[0], header=None, keep_default_na=True)
    csvName = destination_folder + '/' + sheets[0] +'.csv'
    notKnown.to_csv(csvName, encoding='utf-8')
    # sheet 2
    minerals = pd.read_excel(file,sheets[1],  keep_default_na=True)
    csvName = destination_folder + '/' + sheets[1] +'.csv'
    minerals.to_csv(csvName, encoding='utf-8')
    # sheet 3
    thermody = pd.read_excel(file,sheets[2], header=None, keep_default_na=True)
    csvName = destination_folder + '/' + sheets[2] +'.csv'
    thermody.to_csv(csvName, encoding='utf-8')

def load(folder="XLSX", destination_folder = "csv"):
    ####################################
    ##  finds files in source folder  ##
    files = listdir(folder)            #
    path = folder + "/" + files[0]     #
    file = pd.ExcelFile(path)          #
    sheets = file.sheet_names          #
                                      ## 
    # loading:                     #####
    # sheet 1
    notKnown = pd.read_excel(file,sheets[0], header=None, keep_default_na=True)
    csvName = destination_folder + '/' + sheets[0] +'.csv'
    notKnown = pd.read_csv(csvName, na_values="NaN")
    # sheet 2
    minerals = pd.read_excel(file,sheets[1],  keep_default_na=True)
    csvName = destination_folder + '/' + sheets[1] +'.csv'
    minerals = pd.read_csv(csvName, na_values="NaN")
    # sheet 3
    thermody = pd.read_excel(file,sheets[2], header=None, keep_default_na=True)
    csvName = destination_folder + '/' + sheets[2] +'.csv'
    thermody = pd.read_csv(csvName, na_values="NaN")

    return notKnown, minerals, thermody 

def minerals(mins, minerals, thermody):
    ########### Creates definition that uploads relevant minerals
    d={} # set up empty dictionary
    minNum = len(mins)
    mins = [x-1 for x in mins]            # - 1 b/c csv index offset
  
    endmember = [0] * ( minNum + 2)      
    endmember[minNum]   = 151
    endmember[minNum+1] = 152
    #loop to populate minerals into dictionary
    for i in range(minNum):
        endmember[i]     = mins[i]
        d["Mineral_{0}".format(i)] = {
            "minrl"      : str(minerals.loc[mins[i],"min_sym"]),
            "min_name"   : str(minerals.loc[mins[i],"mineral_name"]),
            "sys"        : "",
            "sg"         : [],
            "endmember"  : [mins[i]],
            "endnum"     : 2,
            "variables"  : [],
            "vari_lower" : [],
            "vari_upper" : [],
            "p"          : "@(X)X(1)",
            "SiO2toCO2"  : minerals.loc[mins[i],"SiO2":"CO2"],
            "H"          : thermody.loc[mins[i],"1"],
            "S"          : thermody.loc[mins[i],"2"], 
            "V"          : thermody.loc[mins[i],"3"], 
            "a"          : thermody.loc[mins[i],"4"], 
            "b"          : thermody.loc[mins[i],"5"], 
            "c"          : thermody.loc[mins[i],"6"], 
            "d"          : thermody.loc[mins[i],"7"], 
            "alpha0"     : thermody.loc[mins[i],"8"], 
            "alpha1"     : thermody.loc[mins[i],"9"], 
            "K"          : thermody.loc[mins[i],"10"], 
            "dKdp"       : thermody.loc[mins[i],"11"], 
            "dKdT"       : thermody.loc[mins[i],"12"], 
            "Tc"         : thermody.loc[mins[i],"13"], 
            "Smax"       : thermody.loc[mins[i],"14"], 
            "Vmax"       : thermody.loc[mins[i],"15"], 
            "Comp"       : []
            }
    # Add water
        d["Mineral_{0}".format((minNum))] = {
        "minrl"      : "liq",
        "name"       : "water",
        "min_name"   : "Water",
        "sys"        : "CHO",
        "sg"         : [],
        "endmember"  : [151],
        "endnum"     : 2,
        "variables"  : {'x(liq)'},
        "vari_lower" : [0],
        "vari_upper" : [1],
        "p"          : "@(X)X(1)",
        "SiO2toCO2"  : minerals.loc[150,"SiO2":"CO2"],
        "H"          : thermody.loc[150,"1"],
        "S"          : thermody.loc[150,"2"], 
        "V"          : thermody.loc[150,"3"], 
        "a"          : thermody.loc[150,"4"], 
        "b"          : thermody.loc[150,"5"], 
        "c"          : thermody.loc[150,"6"], 
        "d"          : thermody.loc[150,"7"], 
        "alpha0"     : thermody.loc[150,"8"], 
        "alpha1"     : thermody.loc[150,"9"], 
        "K"          : thermody.loc[150,"10"], 
        "dKdp"       : thermody.loc[150,"11"], 
        "dKdT"       : thermody.loc[150,"12"], 
        "Tc"         : thermody.loc[150,"13"], 
        "Smax"       : thermody.loc[150,"14"], 
        "Vmax"       : thermody.loc[150,"15"], 
        "Comp"       : []    }
# Add CO2
    d["Mineral_{0}".format((minNum+1))] = {
        "minrl"      : "liq",
        "min_name"   : "carbonDioxide",
        "name"       : "CO2",
        "sys"        : "CHO",
        "sg"         : [],
        "endmember"  : [152],
        "endnum"     : 2,
        "variables"  : {'x(liq)'},
        "vari_lower" : [0],
        "vari_upper" : [1],
        "p"          : "@(X)X(1)",
        "SiO2toCO2"  : minerals.loc[151,"SiO2":"CO2"],
        "H"          : thermody.loc[151,"1"],
        "S"          : thermody.loc[151,"2"], 
        "V"          : thermody.loc[151,"3"], 
        "a"          : thermody.loc[151,"4"], 
        "b"          : thermody.loc[151,"5"], 
        "c"          : thermody.loc[151,"6"], 
        "d"          : thermody.loc[151,"7"], 
        "alpha0"     : thermody.loc[151,"8"], 
        "alpha1"     : thermody.loc[151,"9"], 
        "K"          : thermody.loc[151,"10"], 
        "dKdp"       : thermody.loc[151,"11"], 
        "dKdT"       : thermody.loc[151,"12"], 
        "Tc"         : thermody.loc[151,"13"], 
        "Smax"       : thermody.loc[151,"14"], 
        "Vmax"       : thermody.loc[151,"15"], 
        "Comp"       : []    }
    return d


#### LOADS VALUES WITHIN ACTIVITY FUNCTION
def actMod(mins):
"""
Loads activity function for gibbs free energy calculations. Also, i feel there must be a better way of doing this
"""
    d = minerals(mins, minerals, thermody)                                      
    #def calcG(P,T,A, flag):                    i
	pd.DataFrame(d, index = ['H'])                                                     
	T_G = [300, 800]                                                                   
	T = T_G[0]/2 + T_G[1]/2                                                            
	minrl = pd.DataFrame(d, index = ['minrl']).values                                  
	H0=pd.DataFrame(d, index = ['H']).values                                           
	S0=pd.DataFrame(d, index = ['S']).values                                           
	V0=pd.DataFrame(d, index = ['V']).values             # H in KJ, S in KJ/K, V in J/bar
	a0=pd.DataFrame(d, index = ['a']).values                                           
	b0=pd.DataFrame(d, index = ['b']).values                                           
	c0=pd.DataFrame(d, index = ['c']).values                                           
	d0=pd.DataFrame(d, index = ['s']).values                                           
	alpha00=pd.DataFrame(d, index = ['alpha0']).values                                 
	alpha10=pd.DataFrame(d, index = ['alpha1']).values                                 
	Tc00=pd.DataFrame(d, index = ['Tc0']).values                                       
	Smax0=pd.DataFrame(d, index = ['Smax']).values                                     
	Vmax0=pd.DataFrame(d, index = ['Vmax']).values                                     
	K0=pd.DataFrame(d, index = ['K']).values                                           
	dKdT0=pd.DataFrame(d, index = ['dKdT']).values                                     
	dKdp0=pd.DataFrame(d, index = ['dKdp']).values   
    return minrl, H0, S0, V0, a0, b0, c0, d0, alpha00, alpha10, Tc00, Smax0, Vmax0, K0, dKdT0, dKdp0




def iter4(minlen):
    """ Package will calculate all combonations within a 4-series of len-numbers
    This creates duplicate entries of un-ordered list b/c checks take more time
    than calculations"""
    combo = []
    pbar = tqdm(range(0,minlen))
    for i in range(0,minlen):
        tests = []
        pbar.update(1)
        a = i
        for j in range(0,(minlen - 1)):
            b = j
            if b is not a:
                for k in range(0,(minlen - 2)):
                    c = k
                    if c is not a and c is not b:
                        for l in range(0,(minlen - 3)):
                            d = l
                            temp = [a,b,c]
                            if d not in temp:
                                test = [a, b, c, d]
                                tests.append(test)
        outF = open("runs.txt", "a")
        outF.write(str(tests))
        outF.write("\n")
        outF.close()
    return combo




