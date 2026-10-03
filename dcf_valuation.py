import numpy as np
import pandas as pd


# -----------------------------
# Company assumptions
# -----------------------------

company = "Example Company"

revenue_2025 = 10_000
ebitda_margin = 0.25
depreciation = 300
capex = 400
tax_rate = 0.25
change_nwc = 100

revenue_growth = [0.08, 0.07, 0.06, 0.05, 0.04]

wacc = 0.09
terminal_growth = 0.025

net_debt = 1_500
shares_outstanding = 500


# -----------------------------
# Revenue forecast
# -----------------------------

years = [2026, 2027, 2028, 2029, 2030]

revenues = []
revenue = revenue_2025

for growth in revenue_growth:
    revenue = revenue * (1 + growth)
    revenues.append(revenue)


# -----------------------------
# EBITDA and EBIT
# -----------------------------

ebitda = [revenue * ebitda_margin for revenue in revenues]

ebit = [
    EBITDA - depreciation
    for EBITDA in ebitda
]


# -----------------------------
# NOPAT
# -----------------------------

tax = [
    EBIT * tax_rate
    for EBIT in ebit
]

nopat = [
    EBIT - tax
    for EBIT, tax in zip(ebit, tax)
]


# -----------------------------
# Free Cash Flow
# -----------------------------

fcf = [
    NOPAT + depreciation - capex - change_nwc
    for NOPAT in nopat
]


# -----------------------------
# Discount Free Cash Flow
# -----------------------------

discount_factors = [
    1 / ((1 + wacc) ** year)
    for year in range(1, len(years) + 1)
]

pv_fcf = [
    cash_flow * discount_factor
    for cash_flow, discount_factor in zip(fcf, discount_factors)
]


# -----------------------------
# Terminal Value
# -----------------------------

terminal_fcf = fcf[-1] * (1 + terminal_growth)

terminal_value = (
    terminal_fcf /
    (wacc - terminal_growth)
)

pv_terminal_value = (
    terminal_value * discount_factors[-1]
)


# -----------------------------
# Enterprise Value
# -----------------------------

enterprise_value = (
    sum(pv_fcf) + pv_terminal_value
)


# -----------------------------
# Equity Value
# -----------------------------

equity_value = (
    enterprise_value - net_debt
)

value_per_share = (
    equity_value / shares_outstanding
)


# -----------------------------
# Output
# -----------------------------

forecast = pd.DataFrame({
    "Year": years,
    "Revenue": revenues,
    "EBITDA": ebitda,
    "EBIT": ebit,
    "NOPAT": nopat,
    "Free Cash Flow": fcf,
    "PV of FCF": pv_fcf
})

print("\nDCF Forecast")
print(forecast.round(2))

print("\nValuation")
print(f"Enterprise Value: ${enterprise_value:,.2f}")
print(f"Equity Value: ${equity_value:,.2f}")
print(f"Implied Value Per Share: ${value_per_share:,.2f}")
