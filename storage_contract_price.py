import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
data = pd.read_csv("Nat_Gas.csv")
data["Dates"] = pd.to_datetime(data["Dates"])
data = data.sort_values("Dates")
date_nums = data["Dates"].map(pd.Timestamp.toordinal)
price_function = interp1d(
    date_nums,
    data["Prices"],
    kind="linear",
    fill_value="extrapolate"
)
def get_price(date):
    """
    Estimate gas price on any date.
    """
    date = pd.to_datetime(date)
    return float(price_function(date.toordinal()))
def price_storage_contract(
    injection_dates,
    withdrawal_dates,
    injection_rate,
    withdrawal_rate,
    max_volume,
    storage_cost_per_month
):
    """
    Calculate storage contract value.
    """
    total_purchase_cost = 0
    total_sale_revenue = 0
    current_volume = 0
    for d in injection_dates:
        volume = min(
            injection_rate,
            max_volume - current_volume
        )
        current_volume += volume
        purchase_price = get_price(d)
        total_purchase_cost += (
            volume * purchase_price
        )
    for d in withdrawal_dates:
        volume = min(
            withdrawal_rate,
            current_volume
        )
        current_volume -= volume
        sale_price = get_price(d)
        total_sale_revenue += (
            volume * sale_price
        )
    start_date = pd.to_datetime(min(injection_dates))
    end_date = pd.to_datetime(max(withdrawal_dates))
    months_stored = (
        (end_date - start_date).days / 30
    )
    storage_cost = (
        months_stored *
        storage_cost_per_month
    )
    contract_value = (
        total_sale_revenue
        - total_purchase_cost
        - storage_cost
    )
    return round(contract_value, 2)
value = price_storage_contract(
    injection_dates=[
        "2023-06-30",
        "2023-07-31"
    ],
    withdrawal_dates=[
        "2023-12-31",
        "2024-01-31"
    ],
    injection_rate=100000,
    withdrawal_rate=100000,
    max_volume=200000,
    storage_cost_per_month=10000
)
print("Contract Value =", value)