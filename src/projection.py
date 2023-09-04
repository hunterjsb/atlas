import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set Matplotlib style
plt.style.use('dark_background')

st.title('Advanced Portfolio Growth Projection')

# Initialize variables
stocks = []
weights = []
quarterly_returns = []
quarterly_dividends = []

# Add stock information dynamically
n_stocks = st.number_input('How many stocks/ETFs in the portfolio?', min_value=1, max_value=20, value=2)

# Create columns
cols = st.columns(n_stocks)

remaining_weight = 100.0

for i in range(n_stocks):
    with cols[i]:
        stock_name = st.text_input(f'Stock', value=f'Stock{i + 1}', key=f'stock_{i}', label_visibility='collapsed')
        weight = st.number_input(f'Weight (%)', min_value=0.0, max_value=remaining_weight, value=remaining_weight,
                                 key=f'weight_{i}')
        q_return = st.number_input(f'Quarterly Return (%)', min_value=0.0, max_value=50.0, value=2.0, key=f'return_{i}')
        q_dividend = st.number_input(f'Quarterly Dividend (%)', min_value=0.0, max_value=50.0, value=0.5,
                                     key=f'dividend_{i}',)

        remaining_weight -= weight  # Update the remaining weight

    stocks.append(stock_name)
    weights.append(weight)
    quarterly_returns.append(q_return)
    quarterly_dividends.append(q_dividend)

# Validate weights
if np.sum(weights) != 100:
    st.error('The weights must sum up to 100%. Please adjust.')
else:
    initial_value = st.number_input('Initial Portfolio Value ($)', min_value=1000, value=10000)
    years = st.number_input('Number of Years to Project', min_value=1, max_value=70, value=30)

    # Initialize variables for plotting
    total_values = [initial_value]
    sans_div_values = [initial_value]
    dividend_values = [0]
    quarters = years * 4

    for q in range(1, quarters + 1):
        weighted_q_growth = 0
        weighted_q_dividend = 0

        for i in range(len(stocks)):
            weight_factor = weights[i] / 100.0
            q_growth = (1 + quarterly_returns[i] / 100) - 1
            q_div_yield = (1 + quarterly_dividends[i] / 100) - 1

            weighted_q_growth += weight_factor * q_growth
            weighted_q_dividend += weight_factor * q_div_yield

        # Update the total portfolio value for the next quarter
        new_total_value = total_values[-1] * (1 + weighted_q_growth) + weighted_q_dividend * total_values[-1]
        total_values.append(new_total_value)

        # Calculate the values without dividends
        new_sans_div_value = sans_div_values[-1] * (1 + weighted_q_growth)
        sans_div_values.append(new_sans_div_value)

        # Calculate the accumulated dividends
        new_dividend_value = total_values[-1] - sans_div_values[-1]
        dividend_values.append(new_dividend_value)

    time_axis = np.arange(0, years + years / quarters, years / quarters)

    # Plotting with a transparent background
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('none')  # Set outer color to transparent
    ax.set_facecolor('none')  # Set plot background to transparent
    ax.plot(time_axis, total_values, label='Total Return')
    ax.plot(time_axis, sans_div_values, label='Sans Div')
    ax.plot(time_axis, dividend_values, label='Dividends Accumulated')

    # Annotate specific points
    intervals = [10, 5, 3, 2, 1]
    annotate_years = [years // i for i in intervals]
    for year in annotate_years:
        if year <= years:
            idx = year * 4  # since we have 4 quarters in a year
            ax.annotate(f'{total_values[idx]:.2f}', (time_axis[idx], total_values[idx]), textcoords="offset points",
                        xytext=(0, 10), ha='center')
            ax.annotate(f'{sans_div_values[idx]:.2f}', (time_axis[idx], sans_div_values[idx]),
                        textcoords="offset points", xytext=(0, 10), ha='center')
            ax.annotate(f'{dividend_values[idx]:.2f}', (time_axis[idx], dividend_values[idx]),
                        textcoords="offset points", xytext=(0, 10), ha='center')

    ax.set_title('Advanced Portfolio Growth Over Time')
    ax.set_xlabel('Years')
    ax.set_ylabel('Value ($)')
    ax.legend()

    st.pyplot(fig, transparent=True)
