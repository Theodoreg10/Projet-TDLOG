# cu : unit cost
# cp : cost of making an order
# tp : possession rate

from math import sqrt, exp, factorial
from scipy.stats import norm

# Date fixe et Quantité fixe


def S1(demande):
    return demande


# Date fixe et Quantité variable


def S2(demande, cu, cp, tp):
    Q_EOQ = sqrt((2 * demande * cp) / (tp * cu))
    return Q_EOQ
 

# Date variable et Quantité fixe [ point de commande ]


def S3(demande, delai_livraison, temps_consommation):
    D = demande
    DL = delai_livraison
    T = temps_consommation
    PC = ((D) / (T)) * DL
    return PC


# Date variable et Quantité variable


def lambda_S4(demande, horizon):
    D = demande
    HT = horizon
    lamb = D / HT
    return lamb

# k - peut être numero des ventes
def S4(lamb, k):
    P = (((lamb**k) / (factorial(k)))) * (exp ** (-lamb))
    return P


# Stock de sécurité


def StockSec1(demande_moy, delai_livraison):
    DL = delai_livraison
    DM = demande_moy
    SS1 = DL * DM
    return SS1


def StockSec2(niveau_service, ecart_type_demande):
    ETD = ecart_type_demande
    NS = niveau_service
    z = norm.ppf(NS)
    SS2 = z * ETD
    return SS2


# Vrai stock


def stock_final(stock, stock_securité):
    return stock + stock_securité


def stock_alerte(stock_min, stock_securité):
    return stock_min + stock_securité
