import streamlit as st

# Streamlit UI Setup
st.set_page_config(page_title="Simplified NHS Pension Predictor", layout="wide")

st.title("Simplified NHS Pension Predictor")

# User inputs
st.sidebar.header("Your NHS Details")

current_age = st.sidebar.number_input("Current Age", value=40, step=1)
retirement_age = st.sidebar.slider("Retirement Age", 55, 70, 65)

current_salary = st.sidebar.number_input("Current Annual Salary (£)", value=50000, step=1000)
salary_growth_rate = st.sidebar.number_input("Annual Salary Growth (%)", value=2.0, step=0.1, format="%.2f") / 100

st.sidebar.subheader("Scheme Membership")
years_1995 = st.sidebar.number_input("Years in 1995 Scheme", value=5, step=1)
years_2008 = st.sidebar.number_input("Years in 2008 Scheme", value=5, step=1)
years_2015 = st.sidebar.number_input("Years in 2015 Scheme", value=5, step=1)

# Constants based on NHS schemes
accrual_rates = {"2015 CARE": 1/54, "1995 Final Salary": 1/80, "2008 Final Salary": 1/60}

# Calculate predicted pension
final_salary = current_salary * ((1 + salary_growth_rate) ** (retirement_age - current_age))
avg_salary_care = (current_salary + final_salary) / 2

annual_pension_1995 = final_salary * years_1995 * accrual_rates["1995 Final Salary"]
annual_pension_2008 = final_salary * years_2008 * accrual_rates["2008 Final Salary"]
annual_pension_2015 = avg_salary_care * years_2015 * accrual_rates["2015 CARE"]

annual_pension_total = annual_pension_1995 + annual_pension_2008 + annual_pension_2015

# Display results
st.subheader("Estimated Pension at Retirement")
st.write(f"Based on a retirement age of {retirement_age}, your estimated annual NHS pension is:")
st.write(f"## £{annual_pension_total:,.2f} per year")

st.markdown("### Breakdown by Scheme:")
st.write(f"- **1995 Scheme:** £{annual_pension_1995:,.2f}")
st.write(f"- **2008 Scheme:** £{annual_pension_2008:,.2f}")
st.write(f"- **2015 CARE Scheme:** £{annual_pension_2015:,.2f}")

st.markdown("This is a simplified estimate and does not account for lump sums, exact CARE revaluations, or specific scheme rules.")
