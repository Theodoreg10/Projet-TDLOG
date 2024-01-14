# uc : unit cost
# fc : fixed cost, cost of making an order
# hr : holding rate

from math import sqrt, exp, factorial
import pandas as pd


def scenario1(demand: float):
    """
    Function for the scenario where the date for ordering and the
    quantity ordered are fixed.
    """
    return demand


def scenario2(demand: float,
              unit_cost: float,
              fixed_cost: float,
              holding_rate: float):
    """
    Function for the scenario where the date for ordering is fixed
    and the quantity ordered is variable.
    """
    if holding_rate == 0:
        raise ("The holding rate mustn't be null")
    if unit_cost == 0:
        raise ("The unit cost mustn't be null")
    return sqrt((2 * demand * fixed_cost) / (holding_rate * unit_cost))


def scenario3(demand: float, lead_time: int, consumption_time: int):
    """
    Function for the scenario where the date for ordering is variable
    and the quantity ordered is fixed.
    This is called "point of command"
    """
    if consumption_time == 0:
        raise ("the consumption time mustn't be null")
    return ((demand) / (consumption_time)) * lead_time


def scenario4(demand, horizon, k):
    """
    Function for the scenario where the date and the quantity ordered
    are variables.
    """
    lambd = demand / horizon
    if k <= 0:
        raise ("the number of events k must be positive")
    return (((lambd**k) / (factorial(k)))) * (exp(-lambd))


def security_stock_simple(average_demand: float, lead_time: int):
    """
    Function of one of the possible methods to calculate the security stock.
    This method is simpler and does not take probabilistics into consideration.
    """
    return lead_time * average_demand


def security_stock_probabilistic(service_level: float,
                                 std_deviation_demand: float):
    """
    Function of one other possible method to calculate the security stock.
    This method takes probabilistics into consideration.
    """
    if service_level > 1:
        raise ("the service level cannot exceed 100%")
    return service_level * std_deviation_demand


def stock_final(stock: float, security_stock: float):
    """ "
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


def django_to_df(model, user, product=None, is_product=True):
    """
    Function that transforms the model given in Django into Pandas
    """
    if product is not None:
        if is_product:
            product_exists = (
                model.objects.filter(product_name=product, user=user)
                .exists()
            )
            if product_exists:
                django_data = (
                    model.objects.filter(product_name=product, user=user)
                    .values()
                )
            else:
                return None
        else:
            sale_exists = (
                model.objects.filter(ref__product_name=product, user=user)
                .exists()
            )
            if sale_exists:
                django_data = (
                    model.objects.filter(ref__product_name=product, user=user)
                    .values()
                )
            else:
                return None
    else:
        django_data = model.objects.filter(user=user).values()
    df = pd.DataFrame.from_records(django_data)
    return df


if __name__ == "__main__":
    from models import Product

    products = Product.Objects
    print(django_to_df(products))
