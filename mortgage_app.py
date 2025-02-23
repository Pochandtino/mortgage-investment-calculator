import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Streamlit UI Setup
st.set_page_config(page_title="Mortgage vs Investment Calculator", layout="wide")

# Sidebar with user inputs
st.sidebar.header("Adjust Your Parameters")

investment = st.sidebar.number_input("Investment Amount (£)", value=60000, step=1000)
investment_rate = st.sidebar.slider("Investment Return Rate (%)", 0.0, 15.0, 10.0) / 100
additional_investment = st.sidebar.number_input("Annual Additional Investment (£)", value=0, step=1000)
mortgage = st.sidebar.number_input("Mortgage Amount (£)", value=170000, step=5000)
mortgage_rate = st.sidebar.slider("Mortgage Interest Rate (%)", 0.0, 10.0, 3.98) / 100
term = st.sidebar.slider("Mortgage Term (Years)", 5, 30, 15)
income_allocation = st.sidebar.slider("Disposable Income for Investment (£ per month)", 0, 5000, 500, step=100)
remort_freq = st.sidebar.slider("Remortgage Every (Years)", 1, 15, 5)
product_fees = st.sidebar.number_input("Product Fees (£)", value=999, step=100)
investment_duration = st.sidebar.slider("Investment Duration (Years)", term, 40, 40)

# Mortgage Calculation
monthly_rate = mortgage_rate / 12
num_payments = term * 12
mortgage_payment = (mortgage * monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)

# Mortgage balance tracking
mortgage_balances = [mortgage]
remaining_balance = mortgage
for year in range(term):
    for _ in range(12):
        interest = remaining_balance * monthly_rate
        principal = mortgage_payment - interest
        remaining_balance -= principal
    mortgage_balances.append(remaining_balance)

# Investment growth tracking
investment_balances = [investment]
for year in range(investment_duration):
    investment_balances.append((investment_balances[-1] + additional_investment + income_allocation * 12) * (1 + investment_rate))

# Total Mortgage Cost
num_remortgages = term // remort_freq
total_mortgage_cost = mortgage_payment * num_payments + num_remortgages * product_fees

st.sidebar.write(f"### Monthly Mortgage Payment: £{mortgage_payment:,.2f}")
st.sidebar.write(f"### Total Mortgage Cost: £{total_mortgage_cost:,.2f}")

# Data for visualization
df = pd.DataFrame({
    "Year": list(range(investment_duration + 1)),
    "Mortgage Balance (£)": mortgage_balances + [None] * (investment_duration - term),
    "Investment Value (£)": investment_balances,
})

# Plot using Plotly for interactivity
fig = px.line(df, x="Year", y=["Mortgage Balance (£)", "Investment Value (£)"], 
              markers=True, title="Mortgage vs Investment Growth")
fig.update_traces(mode='lines+markers')
fig.update_layout(yaxis_title="£ Value", xaxis_title="Years", hovermode="x unified")

st.plotly_chart(fig, use_container_width=True)
