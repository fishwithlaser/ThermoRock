"""
Code to support thermodynamics-mineral interactions
Adapted from code written by: Dr. Xu Chu
Written by: Thomas Kosciuch
Winter 2019, University of Toronto

   thomas@kosciuch.ca 
or thomas.kosciuch@mail.utoronto.ca 
or xu.chu@utoronto.ca

_________M E T A (-morphic) M A T H (-ematic) C A L C (-ulations) _____________

This package is responsible for 
    calculating gibbs free energy and activity models
"""

def CalcG_f(P, T):   #says P is required but not used
    R = 8.314472e-3
    T = T+273
    a = 0

    if 1 == 1:
        a0= 1113.4
        a1=-0.88517
        a2= 4.53e-3
        a3=-1.3183e-5
        a4=-0.22291
        a5=-3.8022e-4
        a6= 1.7791e-7
        a7= 5.8487
        a8=-2.1370e-2
        a9= 6.8133e-5
        b = 1.465
        c = 1.9853e-3
        d =-8.9090e-2
        e = 8.0331e-2
        Tc= 673
        P0= 2
        Psat= (-13.627*(10**-3)
               +7.29395*(10**-7)* T ** 2 - 
               2.34622*(10**-9)*  T **3 + 
               4.83607*(10**-15)* T ** 5)
        if T < Tc:
            a     = a0 + a1 * (Tc-T) + a2 * (Tc-T) ** 2 + a3 * (Tc-T)**3
            a_gas = a0 + a7 * (Tc-T) + a8 * (Tc-T) ** 2 + a9 * (Tc-T)**3
        else:
            a     = a0 + a4 * (T-Tc) + a5 * (T-Tc) ** 2 + a6 * (T-Tc)**3
            
    else:
        a0=741.2
        a1=-0.10891
        a2=-3.903e-4
        Tc=304.2
        P0=5
        a = a0 + a1 * T + a2 * T ** 2
        b = 3.057
        c = 5.40776e-3 - 1.59046e-6 *T
        d =-1.78198e-1 + 2.45317e-5 *T
        e = 0
        if T <= Tc:
            Vinit = R * T / P + b
            lngamma_MRK, V_MRK  =  Calclngamma(a,b,P,T,Vinit)
        else:
            Vinit  = R * T / P + 10 * b 
            lngamma1,V_MRK      = Calclngamma(a_gas,b,Psat,T,Vinit)
    
            Vinit  = b / 2
            lngamma2,V_MRK = Calclngamma(a,b,Psat,T,Vinit)

            Vinit  = R * T / P + b
            lngamma3,V_MRK = Calclngamma(a,b,P,T,Vinit)
        
            lngamma_MRK = lngamma1-lngamma2+lngamma3
    
    return Psat, a, b, P, T, Vinit

def Calclngamma(a,b,P,T,Vinit): 
    R=8.314472*10**(-3)
    temp = (b*R*T+b ** 2*P-a/sqrt(T))
    F1   =  P*V**3 - R*T*V**2  - temp * V-a * b/sqrt(T) # this used to have @(V) at start
    F2   = 3*P*V**2 - 2*R*T*V   - temp                  # this used to have @(V) at start
    V_MRK = Vinit
    f1   = 1
    
    while abs(f1)>1e-5:
        f1=F1 [V_MRK];
        f2=F2 [V_MRK];
        V_MRK = V_MRK - f1/f2;    
    z=P*V_MRK/R/T;
    B=b*P/R/T;
    A=a/b/R/T^1.5;
    lngamma=z-1-log(z-B)-A*log(1+B/z);
    return lngamma,V_MRK
