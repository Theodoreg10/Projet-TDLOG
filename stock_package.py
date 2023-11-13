# cu : coût unitaire
# cp : coût passation
# tp : taux de possetion

from math import sqrt, exp, factorial
from scipy.stats import norm

# Date fixe et Quantité fixe


def Scenario1(demande: float):
    return demande


# Date fixe et Quantité variable


def Scenario2(demande: float, cout_unitaire: float, cout_passation: float,
              taux_possession: float):
    Quantite_eco_commandee = sqrt(
        (2 * demande * cout_passation) / (taux_possession * cout_unitaire))
    return Quantite_eco_commandee


# Date variable et Quantité fixe [ point de commande ]


def Scenario3(demande: float, delai_livraison: int, temps_consommation: int):
    Point_Commande = ((demande) / (temps_consommation)) * delai_livraison
    return Point_Commande


# Date variable et Quantité variable


def lambda_Scenario4(demande: float, horizon: int):
    return demande / horizon


def Scenario4(lamb: float, k: float):
    Probabilite = (((lamb**k) / (factorial(k)))) * (exp ** (-lamb))
    return Probabilite


# Stock de sécurité


def StockSecurite1(demande_moy: float, delai_livraison: int):
    Stock_Sec1 = delai_livraison * demande_moy
    return Stock_Sec1


def StockSecurite2(niveau_service: float, ecart_type_demande: float):
    Stock_Sec2 = norm.ppf(niveau_service) * ecart_type_demande
    return Stock_Sec2


# Vrai stock


def stock_final(stock: float, stock_securité: float):
    return stock + stock_securité


def stock_alerte(stock_min: float, stock_securite: float):
    return stock_min + stock_securite
