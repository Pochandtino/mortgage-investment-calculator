import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Streamlit UI Setup
st.set_page_config(page_title="Mortgage vs Investment", layout="wide")

# Sidebar with user inputs
st.sidebar.header("Adjust Your Parameters")

investment = st.sidebar.number_input("Initial Investment Amount (£)", value=60000, step=1000)
investment_rate = st.sidebar.number_input("Investment Return Rate (%)", value=10.0, step=0.1, format="%.2f") / 100
additional_investment_mortgage = st.sidebar.number_input("Annual Additional Investment During Mortgage (£)", value=0, step=1000)
additional_investment_post_mortgage = st.sidebar.number_input("Annual Additional Investment Post Mortgage (£)", value=5000, step=1000)
mortgage = st.sidebar.number_input("Mortgage Amount (£)", value=170000, step=5000)
mortgage_rate = st.sidebar.number_input("Mortgage Interest Rate (%)", value=3.98, step=0.1, format="%.2f") / 100
term = st.sidebar.number_input("Mortgage Term (Years)", value=15, step=1)
income_allocation = st.sidebar.number_input("Disposable Income for Investment (£ per month)", value=500, step=100)
remort_freq = st.sidebar.number_input("Remortgage Every (Years)", value=5, step=1)
product_fees = st.sidebar.number_input("Product Fees (£)", value=999, step=100)
investment_duration = st.sidebar.number_input("Investment Duration (Years)", value=40, step=1)

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

# Investment growth tracking with different pre- and post-mortgage contributions
investment_balances = [investment]
for year in range(investment_duration):
    if year < term:
        investment_balances.append((investment_balances[-1] + additional_investment_mortgage + income_allocation * 12) * (1 + investment_rate))
    else:
        investment_balances.append((investment_balances[-1] + additional_investment_post_mortgage + income_allocation * 12) * (1 + investment_rate))

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
              markers=True, title="Mortgage vs Investment")
fig.update_traces(mode='lines+markers')
fig.update_layout(yaxis_title="£ Value", xaxis_title="Years", hovermode="x unified", 
                  legend=dict(x=0, y=1, bgcolor='rgba(255,255,255,0.5)', title_text="Legend"))

st.plotly_chart(fig, use_container_width=True)
