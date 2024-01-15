"""
Inventory management module.

This module provides functions for inventory management, including order scenarios,
calculation of safety stock, and utilities for handling Django data with Pandas.
"""

from math import sqrt, exp, factorial
from scipy.stats import norm
import pandas as pd

def scenario1(demand: float):
    """
    Scenario 1: Function for the case where the order date and the ordered quantity are fixed.
    
    Args:
        demand (float): The demand.

    Returns:
        float: The demand.
    """
    return demand

def scenario2(demand: float, unit_cost: float, fixed_cost: float, holding_rate: float):
    """
    Scenario 2: Function for the case where the order date is fixed and the ordered quantity is variable.

    Args:
        demand (float): The demand.
        unit_cost (float): The unit cost.
        fixed_cost (float): The fixed cost, cost of making an order.
        holding_rate (float): The holding rate.

    Returns:
        float: The optimal quantity to order.
    """
    if holding_rate == 0:
        raise ValueError("The holding rate mustn't be null")
    if unit_cost == 0:
        raise ValueError("The unit cost mustn't be null")
    
    return sqrt((2 * demand * fixed_cost) / (holding_rate * unit_cost))

def scenario3(demand: float, lead_time: int, consumption_time: int):
    """
    Scenario 3: Function for the case where the order date is variable and the ordered quantity is fixed.
    This is called "point of command".

    Args:
        demand (float): The demand.
        lead_time (int): The lead time.
        consumption_time (int): The consumption time.

    Returns:
        float: The point of command.
    """
    if consumption_time == 0:
        raise ValueError("The consumption time mustn't be null")
    
    return ((demand) / (consumption_time)) * lead_time

def scenario4(demand, horizon, k):
    """
    Scenario 4: Function for the case where the order date and the ordered quantity are variable.

    Args:
        demand: The demand.
        horizon: The time horizon.
        k: The number of events.

    Returns:
        float: The result of the calculation for scenario 4.
    """
    lambd = demand / horizon
    if k <= 0:
        raise ValueError("The number of events k must be positive")
    return (((lambd**k) / (factorial(k)))) * (exp(-lambd))

def security_stock_simple(average_demand: float, lead_time: int):
    """
    Function of one of the possible methods to calculate the safety stock.
    This method is simpler and does not take probabilistics into consideration.

    Args:
        average_demand (float): The average demand.
        lead_time (int): The lead time.

    Returns:
        float: The safety stock.
    """
    return lead_time * average_demand

def security_stock_probabilistic(service_level: float, std_deviation_demand: float):
    """
    Function of one other possible method to calculate the safety stock.
    This method takes probabilistics into consideration.

    Args:
        service_level (float): The target service level.
        std_deviation_demand (float): The standard deviation of demand.

    Returns:
        float: The calculated safety stock.
    """
    if service_level > 1:
        raise ValueError("The service level cannot exceed 100%")
    return service_level * std_deviation_demand

def stock_final(stock: float, security_stock: float):
    """"
    Function that calculates the total stock level taking into account the
    safety stock.

    Args:
        stock (float): The current stock level.
        security_stock (float): The safety stock.

    Returns:
        float: The final stock level.
    """
    return stock + security_stock

def stock_alert(stock_min: float, security_stock: float):
    """
    Function that sets the stock level that triggers an alert that
    the level is low.

    Args:
        stock_min (float): The minimum desired stock level.
        security_stock (float): The safety stock.

    Returns:
        float: The alert stock level.
    """
    return stock_min + security_stock

def django_to_df(model, product=None, is_product=True):
    """
    Function that transforms the model given in Django into Pandas.

    Args:
        model: The Django model.
        product (str): The name or reference of the product (optional).
        is_product (bool): Indicates whether the filter should be applied on the product name or reference.

    Returns:
        pandas.DataFrame: The resulting Pandas DataFrame.
    """
    if product is not None:
        if is_product:
            django_data = model.filter(product_name=product)
        else:
            django_data = model.filter(ref=product)
    else:    
        django_data = model.objects.values()
    
    df = pd.DataFrame.from_records(django_data)
    return df

def test_django_to_df():
    """
    Test function for converting Django data to Pandas DataFrame.
    """
    from models import Product
    products = Product.objects
    print(django_to_df(products))

if __name__ == "__main__":
    test_django_to_df()
