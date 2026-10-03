import pandas as pd


def dcf_value(fcf, wacc, terminal_growth, net_debt, shares):
    """
    Calculate implied equity value per share
    using a discounted cash flow model.
    """

    discount_factors = [
        1 / ((1 + wacc) ** year)
        for year in range(1, len(fcf) + 1)
    ]

    pv_fcf = [
        cash_flow * discount_factor
        for cash_flow, discount_factor in zip(
            fcf, discount_factors
        )
    ]

    terminal_fcf = fcf[-1] * (1 + terminal_growth)

    terminal_value = (
        terminal_fcf /
        (wacc - terminal_growth)
    )

    pv_terminal_value = (
        terminal_value * discount_factors[-1]
    )

    enterprise_value = (
        sum(pv_fcf) + pv_terminal_value
    )

    equity_value = (
        enterprise_value - net_debt
    )

    return equity_value / shares


# Example forecast FCF
fcf = [500, 550, 600, 650, 700]

net_debt = 1500
shares = 500

wacc_values = [0.08, 0.09, 0.10, 0.11, 0.12]
growth_values = [0.015, 0.020, 0.025, 0.030, 0.035]

sensitivity = []

for growth in growth_values:

    row = []

    for wacc in wacc_values:

        value = dcf_value(
            fcf,
            wacc,
            growth,
            net_debt,
            shares
        )

        row.append(round(value, 2))

    sensitivity.append(row)


sensitivity_table = pd.DataFrame(
    sensitivity,
    index=[f"{g:.1%}" for g in growth_values],
    columns=[f"{w:.1%}" for w in wacc_values]
)

print("\nDCF Sensitivity Analysis")
print(sensitivity_table)
