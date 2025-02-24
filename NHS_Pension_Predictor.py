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
nhs_years = st.sidebar.number_input("Years in NHS Scheme", value=15, step=1)
scheme_type = st.sidebar.selectbox("NHS Scheme Type", ("2015 CARE", "1995 Final Salary", "2008 Final Salary"))

# Constants based on NHS schemes
accrual_rates = {"2015 CARE": 1/54, "1995 Final Salary": 1/80, "2008 Final Salary": 1/60}

# Calculate predicted pension
final_salary = current_salary * ((1 + salary_growth_rate) ** (retirement_age - current_age))

if scheme_type == "2015 CARE":
    avg_salary = (current_salary + final_salary) / 2
    annual_pension = avg_salary * nhs_years * accrual_rates[scheme_type]
else:
    annual_pension = final_salary * nhs_years * accrual_rates[scheme_type]

# Display results
st.subheader("Estimated Pension at Retirement")
st.write(f"Based on a retirement age of {retirement_age}, your estimated annual NHS pension is:")
st.write(f"## £{annual_pension:,.2f} per year")

st.markdown("This is a simplified estimate and does not account for lump sums, exact CARE revaluations, or specific scheme rules.")
