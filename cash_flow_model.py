import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Streamlit UI Setup
st.set_page_config(page_title="Future Cash Flow Model", layout="wide")

# Sidebar with user inputs
st.sidebar.header("Adjust Your Parameters")

# Salary Inputs
salary = st.sidebar.number_input("Current Salary (£)", value=50000, step=1000)
salary_growth = st.sidebar.number_input("Annual Salary Growth Rate (%)", value=2.0, step=0.1, format="%.2f") / 100
retirement_age = st.sidebar.slider("Retirement Age", 55, 70, 65)

# Investment Inputs
investment = st.sidebar.number_input("Current Investments (£)", value=60000, step=1000)
investment_growth = st.sidebar.number_input("Investment Growth Rate (%)", value=5.0, step=0.1, format="%.2f") / 100
annual_investment = st.sidebar.number_input("Annual Investment Contribution (£)", value=5000, step=500)

# NHS Pension Inputs
nhs_years = st.sidebar.number_input("Years in NHS Pension", value=15, step=1)
nhs_pension_growth = st.sidebar.number_input("NHS Pension Growth Rate (%)", value=1.5, step=0.1, format="%.2f") / 100

# State Pension Inputs
state_pension_age = 67  # UK standard for now
state_pension_amount = 11000  # Estimated full state pension

# Inflation Assumption
inflation_rate = 2.5 / 100  # Fixed at 2.5%

# Timeframe
current_age = st.sidebar.number_input("Current Age", value=40, step=1)
end_age = st.sidebar.slider("Model End Age", retirement_age, 100, 85)

# Generate Yearly Data
years = list(range(current_age, end_age + 1))
salaries = []
investments = []
pension_income = []
state_pensions = []
cash_flows = []

total_investments = investment
for age in years:
    # Salary Growth
    if age < retirement_age:
        salaries.append(salary)
        salary *= (1 + salary_growth)
    else:
        salaries.append(0)
    
    # Investment Growth
    total_investments = (total_investments + annual_investment) * (1 + investment_growth)
    investments.append(total_investments)
    
    # Pension Income (NHS & State Pension)
    if age >= retirement_age:
        nhs_pension = (nhs_years / 45) * salary  # Rough NHS pension estimate
    else:
        nhs_pension = 0
    
    if age >= state_pension_age:
        state_pension = state_pension_amount
    else:
        state_pension = 0
    
    pension_income.append(nhs_pension)
    state_pensions.append(state_pension)
    
    # Cash Flow Calculation
    total_income = salaries[-1] + pension_income[-1] + state_pensions[-1]
    cash_flows.append(total_income)

# Data for Visualization
df = pd.DataFrame({
    "Age": years,
    "Salary (£)": salaries,
    "Investment Value (£)": investments,
    "NHS Pension (£)": pension_income,
    "State Pension (£)": state_pensions,
    "Total Income (£)": cash_flows,
})

# Plot using Plotly for interactivity
fig = px.line(df, x="Age", y=["Salary (£)", "Investment Value (£)", "NHS Pension (£)", "State Pension (£)", "Total Income (£)"],
              markers=True, title="Projected Cash Flow Over Time")
fig.update_traces(mode='lines+markers')
fig.update_layout(yaxis_title="£ Value", xaxis_title="Age", hovermode="x unified", 
                  legend=dict(x=0, y=1, bgcolor='rgba(255,255,255,0.5)', title_text="Legend"))

st.plotly_chart(fig, use_container_width=True)
