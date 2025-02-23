import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Streamlit UI Setup
st.set_page_config(page_title="Mortgage vs Investment", layout="wide")

# Sidebar with user inputs
st.sidebar.header("Adjust Your Parameters")

investment = st.sidebar.number_input("Initial Investment Amount (£)", value=50000, step=1000)
investment_rate = st.sidebar.number_input("Investment Return Rate (%)", value=8.0, step=0.1, format="%.2f") / 100
additional_investment_mortgage = st.sidebar.number_input("Annual Additional Investment During Mortgage (£)", value=0, step=1000)
additional_investment_post_mortgage = st.sidebar.number_input("Annual Additional Investment Post Mortgage (£)", value=0, step=1000)
mortgage = st.sidebar.number_input("Mortgage Amount (£)", value=170000, step=5000)
mortgage_rate = st.sidebar.number_input("Mortgage Interest Rate (%)", value=4.0, step=0.1, format="%.2f") / 100
term = st.sidebar.slider("Mortgage Term (Years)", 5, 30, 20)
income_allocation = st.sidebar.number_input("Disposable Income for Investment (£ per month)", value=1000, step=100)
remort_freq = st.sidebar.slider("Remortgage Every (Years)", 1, 15, 5)
product_fees = st.sidebar.number_input("Product Fees (£)", value=1000, step=100)
investment_duration = st.sidebar.slider("Investment Duration (Years)", term, 40, 30)

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
surplus_deficit = [investment - mortgage]
for year in range(investment_duration):
    if year < term:
        new_value = (investment_balances[-1] + additional_investment_mortgage + income_allocation * 12) * (1 + investment_rate)
    else:
        new_value = (investment_balances[-1] + additional_investment_post_mortgage + income_allocation * 12) * (1 + investment_rate)
    investment_balances.append(new_value)
    mortgage_remaining = mortgage_balances[year] if year < len(mortgage_balances) else 0
    surplus_deficit.append(new_value - mortgage_remaining)

# Total Mortgage Cost
num_remortgages = term // remort_freq
total_mortgage_cost = mortgage_payment * num_payments + num_remortgages * product_fees

# Final values for display
total_investment_value = investment_balances[-1]
final_surplus_deficit = surplus_deficit[-1]

st.sidebar.write(f"### Monthly Mortgage Payment: £{mortgage_payment:,.2f}")
st.sidebar.write(f"### Total Mortgage Cost: £{total_mortgage_cost:,.2f}")
st.sidebar.write(f"### Total Investment Portfolio Size: £{total_investment_value:,.2f}")
st.sidebar.write(f"### Final Surplus/Deficit: £{final_surplus_deficit:,.2f}")

# Data for visualization
df = pd.DataFrame({
    "Year": list(range(investment_duration + 1)),
    "Mortgage Balance (£)": mortgage_balances + [None] * (investment_duration - term),
    "Investment Value (£)": investment_balances,
    "Surplus/Deficit (£)": surplus_deficit,
})

# Plot using Plotly for interactivity
fig = px.line(df, x="Year", y=["Mortgage Balance (£)", "Investment Value (£)", "Surplus/Deficit (£)"], 
              markers=True, title="Mortgage vs Investment")
fig.update_traces(mode='lines+markers')
fig.update_layout(yaxis_title="£ Value", xaxis_title="Years", hovermode="x unified", 
                  legend=dict(x=0, y=1, bgcolor='rgba(255,255,255,0.5)', title_text="Legend"))

st.plotly_chart(fig, use_container_width=True)
