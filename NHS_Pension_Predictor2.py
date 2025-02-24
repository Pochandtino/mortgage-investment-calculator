import streamlit as st
import pandas as pd

st.set_page_config(page_title="Advanced NHS Pension Predictor", layout="wide")

st.title("Advanced NHS Pension Predictor")

st.sidebar.header("Your NHS Pension Details")

# Toggle for advanced features
advanced = st.sidebar.checkbox("Advanced Details")

# Example Earnings Data
example_data = pd.DataFrame({
    "Year Ending": ["31/03/2010", "31/03/2011", "31/03/2012", "31/03/2013", "31/03/2014", "31/03/2015", "31/03/2016", "31/03/2017", "31/03/2018", "31/03/2019", "31/03/2020", "31/03/2021", "31/03/2022", "31/03/2023", "31/03/2024"],
    "Pensionable Earnings": [23203.30, 29298.30, 30293.96, 29062.02, 28555.02, 30081.52, 33283.89, 36423.02, 38323.91, 40779.51, 43008.22, 47088.40, 58685.57, 54266.96, 56964.96],
    "Section": ["2008"]*13 + ["2015"]*2,
    "Revaluation": [None]*13 + [11.6, 8.2],
    "Year": list(range(1,16)),
    "Age": list(range(30,45))
})

if advanced:
    st.subheader("Detailed Pensionable Earnings History")
    st.dataframe(example_data)

# Pension Calculation
final_salary_2008 = example_data[example_data.Section == "2008"]["Pensionable Earnings"].iloc[-3:].mean()
years_2008 = len(example_data[example_data.Section == "2008"])
pension_2008 = final_salary_2008 * (years_2008 / 60)

care_earnings = example_data[example_data.Section == "2015"]
care_pension = sum(care_earnings["Pensionable Earnings"] / 54)

# Revaluation factor
care_pension_revalued = care_pension
for rev in care_earnings["Revaluation"].dropna():
    care_pension_revalued *= (1 + rev / 100)

# Display results
st.subheader("Estimated NHS Pension")
st.write(f"### 2008 Section Pension: £{pension_2008:,.2f} per year")
st.write(f"### 2015 CARE Pension (Revalued): £{care_pension_revalued:,.2f} per year")
st.write(f"### Total Estimated Pension: £{pension_2008 + care_pension_revalued:,.2f} per year")
