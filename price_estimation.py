import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
data = pd.read_csv("Nat_Gas.csv")
data["Dates"] = pd.to_datetime(data["Dates"])
data = data.sort_values("Dates")
plt.figure(figsize=(10, 5))
plt.plot(data["Dates"], data["Prices"], marker="o")
plt.title("Natural Gas Prices")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid(True)
plt.show()
date_numeric = data["Dates"].map(pd.Timestamp.toordinal)
price_interp = interp1d(
    date_numeric,
    data["Prices"],
    kind="linear",
    fill_value="extrapolate"
)
data["Month"] = data["Dates"].dt.month
monthly_avg = data.groupby("Month")["Prices"].mean()
last_date = data["Dates"].max()
def estimate_price(date_str):
    """
    Estimate natural gas price for any date.
    Uses interpolation within historical range and
    seasonal averages for future dates.
    """
    target_date = pd.to_datetime(date_str)
    if target_date <= last_date:
        return float(
            price_interp(target_date.toordinal())
        )
    month = target_date.month
    yearly_growth = (
        data["Prices"].iloc[-1] -
        data["Prices"].iloc[-13]
    )
    forecast_price = monthly_avg[month] + yearly_growth
    return round(float(forecast_price), 2)
print("2022-06-15:",estimate_price("2022-06-15"))
print("2024-12-31:",estimate_price("2024-12-31"))
print("2025-06-30:", estimate_price("2025-06-30"))