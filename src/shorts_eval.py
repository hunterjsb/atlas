import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ATLAS_COLOR = '#e64417'
ATLAS_COLOR_ALT = '#f09859'

plt.style.use('dark_background')
with open('./dat/atlasshorts.csv') as f:
    shorts = pd.read_csv(f)


def dollars_to_numeric(_df: pd.DataFrame, col_name: str) -> None:
    _df[col_name] = _df[col_name].replace('\$|,', '', regex=True)
    _df[col_name] = pd.to_numeric(shorts[col_name])


dollars_to_numeric(shorts, 'Amount')
dollars_to_numeric(shorts, 'Price')
dollars_to_numeric(shorts, 'Fees')


def smooth(scalars: list[float], weight: float) -> list[float]:  # Weight between 0 and 1
    """smoothed_profits = smooth(shorts['Profits'], .4)"""
    last = scalars[0]  # First value in the plot (first timestep)
    smoothed = list()
    for point in scalars:
        smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
        smoothed.append(smoothed_val)                        # Save it
        last = smoothed_val                                  # Anchor the last smoothed value

    return smoothed

# MATH
shorts['Profits'] = shorts['Amount'].cumsum()
buys = {}
sells = {}
for i, row in shorts.iterrows():
    ticker = row['Symbol']
    amount = row['Amount']
    fee = row['Fees'] if row['Fees'] == row['Fees'] else 0

    if row['Action'] == 'Buy':
        if ticker not in buys:
            buys[ticker] = abs(amount) + fee
        else:
            buys[ticker] += abs(amount) + fee
    
    if row['Action'] == 'Sell Short':
        if ticker not in sells:
            sells[ticker] = amount - fee
        else:
            sells[ticker] += amount - fee

abs_profits = []
pct_profits = []
for ticker in buys.keys():
    abs_profits.append((sells[ticker] - buys[ticker]))
    pct_profits.append(round((sells[ticker] - buys[ticker])/buys[ticker] * 100))

# PLOT
fig, ax = plt.subplots(1, 2)
rects1 = ax[0].bar(buys.keys(), [round(i)for i in abs_profits], label='$ profits', color=ATLAS_COLOR)
ax[1].bar(buys.keys(), pct_profits, label='% profits', color=ATLAS_COLOR_ALT)

ax[0].spines.right.set_visible(False)
ax[0].spines.top.set_visible(False)
ax[0].spines.left.set_visible(False)
ax[0].spines.bottom.set_visible(False)

ax[1].spines.right.set_visible(False)
ax[1].spines.top.set_visible(False)
ax[1].spines.left.set_visible(False)
ax[1].spines.bottom.set_visible(False)

fig.set_size_inches(12, 6)
fig.tight_layout()
plt.savefig('./out.png')
