import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title("Florida Minimum Wage vs Cost of Living - Miami-Dade")

# Description at top
st.markdown("""
This app analyzes how Florida's minimum wage compares to Miami-Dade's cost of living from 2015 to 2024.
We use data from:
- Florida Department of Economic Opportunity
- MIT Living Wage Calculator
- U.S. Census (Median Household Income)

Use the dropdown below to explore the relationship between wages, cost of living, and affordability.
""")

min_wage = pd.read_csv("minimum_wage.csv")
living_wage = pd.read_csv("living_wage.csv")
median_income = pd.read_csv("median_income.csv")

df = pd.merge(min_wage, living_wage, on="Year")
df = pd.merge(df, median_income, on="Year")

# Calculate metrics
df["Wage Gap"] = df["Living Wage"] - df["Minimum Wage"]
df["Wage Gap %"] = (df["Minimum Wage"] / df["Living Wage"]) * 100
df["Income Adequacy %"] = (df["Median Income"] / df["Living Wage"]) * 100

# Show full data table
with st.expander(" View Raw Data Table"):
    st.dataframe(df)

# Dropdown chart selector
chart = st.selectbox("Select Chart to View:",
                     ["Minimum Wage vs Living Wage",
                      "Minimum Wage Coverage (%)",
                      "Median Income Adequacy (%)"])

# Plot 1
if chart == "Minimum Wage vs Living Wage":
    st.subheader(" Minimum Wage vs Living Wage")
    st.markdown("""
    This chart shows how Florida’s minimum wage compares to the cost of living for a single adult in Miami-Dade County.
    Although wages increased sharply after 2021 (due to the $15/hr amendment), minimum wage still trails the living wage by several dollars.
    """)
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.plot(df["Year"], df["Minimum Wage"], marker="o", label="Minimum Wage")
    plt.plot(df["Year"], df["Living Wage"], marker="o", label="Living Wage")
    plt.title("Florida Minimum Wage vs Living Wage (Miami-Dade)")
    plt.xlabel("Year")
    plt.ylabel("Wage ($)")
    plt.legend()
    plt.grid(True)
    st.pyplot(fig)

# Plot 2
elif chart == "Minimum Wage Coverage (%)":
    st.subheader("Minimum Wage Coverage of Living Wage (%)")
    st.markdown("""
    This chart shows what % of the living wage is covered by minimum wage each year.
    In 2015, minimum wage covered about 64% of the living wage. After years of decline, wage reforms helped recover coverage but full living wage coverage has not yet been reached.
    """)
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.plot(df["Year"], df["Wage Gap %"], marker="o", color="red")
    plt.title("Minimum Wage Coverage of Living Wage (%)")
    plt.xlabel("Year")
    plt.ylabel("Minimum Wage as % of Living Wage")
    plt.grid(True)
    st.pyplot(fig)

# Plot 3
else:
    st.subheader("Median Household Income as % of Living Wage")
    st.markdown("""
    This chart shows how Miami-Dade’s median household income compares to living wage levels.
    While middle-class households remain above basic living wage levels, income growth has been volatile due to inflation and post-pandemic shifts.
    """)
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.plot(df["Year"], df["Income Adequacy %"], marker="o", color="green")
    plt.title("Median Household Income as % of Living Wage")
    plt.xlabel("Year")
    plt.ylabel("Income Adequacy (%)")
    plt.grid(True)
    st.pyplot(fig)

