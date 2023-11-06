from math import *
# cu : coût unitaire
# cp : coût passation
# tp : taux de possetion


# Date fixe et Quantité fixe
def S1 (demande):
    return demande

# Date fixe et Quantité variable
def S2(demande , cu , cp , tp):
    Q_EOQ = sqrt((2*demande * cp )/(tp * cu))
    return Q_EOQ

# Date variable et Quantité fixe [ point de commande ]
def S3(demande, delai_livraison , temps_consommation):
    D = demande
    DL = delai_livraison
    T = temps_consommation
    PC = (D)/(T*DL)
    return PC

# Date variable et Quantité variable

def lambda_S4 (demande, horizon):
    D = demande
    HT = horizon
    lamb = D/HT
    return lamb

def S4 (lamb , k):
    P = (((lamb ** k)/(factorial(k)))) * (exp**(-lamb))
    return P
