"""
Python code to calculate rock-thermodynamic interactions
Written by:   thomas.kosciuch@mail.utoronto.ca
Adapted from: xu.chu@utoronto.ca

Last updated: 02/11/2019
"""

import numpy as np                                 # matrix ops

def compress(d, PHASE, CC):
    """
    compress will compose the A-matrix of the minerals selected, then compress it.
    """
    A                       = np.zeros(((len(PHASE)), len(CC)))
    minPres                 = []                    # min names
    # Compositional matrix
    # Col 1: 15 = CC
    for i in range((len(PHASE))):
        for j in range(len(CC)-2):                  # -2 b/c of H2O+CO2
            target          = 'Mineral_' +  str(i)
            temp            = d.get(target)
            temp            = temp.get('SiO2toCO2')
            A[i][j]         = int(temp[j])
            temp            = d.get(target)
            temp            = temp.get('min_name')
        minPres.append(temp)                        # tracking mins
    # Deletes zero columns
    components = []
    for i in range(len(CC)-1):
        target = len(CC) - 1 - i
        if sum(A[:,target]) > 0:                    # Preserves components
            components.insert(0,(CC[target]))    
        if sum(A[:,target]) == 0:
            A = np.delete(A,target,1)

    return A


