# uc : unit cost
# fc : fixed cost, cost of making an order
# hr : holding rate

from math import sqrt, exp, factorial
from scipy.stats import norm
import pandas as pd


def scenario1(demand: float):
    """
    Function for the scenario where the date for ordering and the
    quantity ordered are fixed.
    """
    return demand


def scenario2(demand: float, uc: float, fc: float, hr: float):
    """
    Function for the scenario where the date for ordering is fixed
    and the quantity ordered is variable.
    """
    return sqrt((2 * demand * fc) / (hr * uc))


def scenario3(demand: float, lead_time: int, consumption_time: int):
    """
    Function for the scenario where the date for ordering is variable
    and the quantity ordered is fixed.
    This is called "point of command"
    """
    return ((demand) / (consumption_time)) * lead_time


def lambda_scenario4(demand: float, horizon: int):
    """
    Function that calculates the average rate of demand.
    """
    return demand / horizon


def scenario4(lamb, k):
    """
    Function for the scenario where the date and the quantity ordered
    is are variables.
    """
    return (((lamb**k) / (factorial(k)))) * (exp ** (-lamb))


def security_stock_simple(avg_demand: float, lead_time: int):
    """
    Function of one of the possible methods to calculate the security stock.
    This method is simpler and does not take probabilistic into consideration.
    """
    return lead_time * avg_demand


def security_stock_probabilistic(service_level: float,
                                 std_deviation_demand: float):
    """
    Function of one other possible method to calculate the security stock.
    This method takes probabilistic into consideration.
    """
    return norm.ppf(service_level) * std_deviation_demand


def stock_final(stock: float, security_stock: float):
    """"
    Function that calculates the total stock level taking into account the
    security stock.
    """
    return stock + security_stock


def stock_alert(stock_min: float, security_stock: float):
    """
    Function that sets the stock level that triggers an alert that
    the level is low.
    """
    return stock_min + security_stock


def django_to_df(model):
    """
    Function that transforms the model given in Django into Pandas
    """
    django_data = model.objects.values()
    df = pd.DataFrame.from_records(django_data)
    return df


if __name__ == "__main__":
    from principal.models import Product
    products = Product.Objects()
    print(django_to_df(products))
