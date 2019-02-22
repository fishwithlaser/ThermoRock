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

def minerals(mins, minerals):
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
            "endmember"  : [mins[i]],
            "endnum"     : 2,
            "variables"  : [],
            "vari_lower" : [],
            "vari_upper" : [],
            "p"          : "@(X)X(1)",
            "SiO2toCO2"  : minerals.loc[mins[i],"SiO2":"CO2"]
            }
    # Add water
        d["Mineral_{0}".format((minNum))] = {
        "minrl"      : "liq",
        "name"       : "water",
        "min_name"   : "Water",
        "sys"        : "CHO",
        "endmember"  : [151],
        "endnum"     : 2,
        "variables"  : {'x(liq)'},
        "vari_lower" : [0],
        "vari_upper" : [1],
        "p"          : "@(X)X(1)",
        "SiO2toCO2"  : minerals.loc[150,"SiO2":"CO2"]
    }
    # Add CO2
    d["Mineral_{0}".format((minNum+1))] = {
        "minrl"      : "liq",
        "min_name"   : "carbonDioxide",
        "name"       : "CO2",
        "sys"        : "CHO",
        "endmember"  : [152],
        "endnum"     : 2,
        "variables"  : {'x(liq)'},
        "vari_lower" : [0],
        "vari_upper" : [1],
        "p"          : "@(X)X(1)",
        "SiO2toCO2"  : minerals.loc[151,"SiO2":"CO2"]
    }
    return d

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





