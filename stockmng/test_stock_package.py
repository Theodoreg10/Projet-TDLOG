from stock_package import (
    scenario2, scenario3, scenario4, security_stock_simple,
    security_stock_probabilistic, stock_final, stock_alert)


def test_scenario2():
    """Test the scenario2 function with specific inputs
    """
    demand = 100
    uc = 2
    fc = 500
    hr = 8
    result = scenario2(demand, uc, fc, hr)
    expected_result = 79.056
    """Verify that the result is as expected
    """
    assert (result - expected_result < 1e-3)


def test_scenario3():
    """Test the scenario3 function with specific inputs
    """
    demand = 100
    lead_time = 2
    consumption_time = 4
    result = scenario3(demand, lead_time, consumption_time)
    expected_result = 50
    """Verify that the result is as expected
    """
    assert (result - expected_result < 1e-3)


def test_scenario4():
    """Test the scenario4 function with specific inputs
    """
    demand = 100
    horizon = 5
    k = 12
    result = scenario4(demand, horizon, k)
    expected_result = 0.01762
    """Verify that the result is as expected
    """
    assert (result - expected_result < 1e-3)


def test_security_stock_simple():
    """Test the security_stock_simple function with specific inputs
    """
    average_demand = 100
    lead_time = 5
    result = security_stock_simple(average_demand, lead_time)
    """Verify that the result is as expected
    """
    expected_result = 500
    assert (result - expected_result < 1e-3)


def test_security_stock_probabilistic():
    """Test the security_stock_probabilistic function with specific inputs
    """
    std_deviation_demand = 100
    service_level = 0.85
    result = security_stock_probabilistic(service_level, std_deviation_demand)
    """Verify that the result is as expected
    """
    expected_result = 85
    assert (result - expected_result < 1e-3)


def test_stock_final():
    """Test the stock_final function with specific inputs
    """
    stock = 100
    security_stock = 200
    result = stock_final(stock, security_stock)
    expected_result = 300
    """Verify that the result is as expected
    """
    assert (result - expected_result < 1e-3)


def test_stock_alert():
    """Test the stock_final function with specific inputs
    """
    stock_min = 100
    security_stock = 200
    result = stock_alert(stock_min, security_stock)
    expected_result = 300
    """Verify that the result is as expected
    """
    assert (result - expected_result < 1e-3)
