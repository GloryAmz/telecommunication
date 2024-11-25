import streamlit as st
import pandas as pd
import sqlite3


# Load the data
@st.cache
def load_data():
    file_path = "telecommunications_data.csv"
    return pd.read_csv(file_path)

data = load_data()

# Set up the database connection
conn = sqlite3.connect("telecom_data.db")

st.title("Telecommunications Data Insights")
st.write("Welcome to the Telecommunications App. Analyze customer data, churn trends, and more!")
st.write("Here is a preview of the dataset:")
st.dataframe(data.head())
st.header("Data Validation")
st.write("Checking for missing values and duplicates...")

# Missing values
st.write("Missing Values:")
st.write(data.isnull().sum())

# Duplicate values
duplicates = data.duplicated(subset="CustomerID").sum()
st.write(f"Duplicate Records: {duplicates}")

st.header("Insights and Analysis")
st.write("Here are some key metrics from the dataset:")

# Churn rate
churn_rate = data["Churn"].value_counts(normalize=True) * 100
st.write("Churn Rate:")
st.bar_chart(churn_rate)

# Average monthly charges
avg_charges = data.groupby("PlanType")["MonthlyCharges"].mean()
st.write("Average Monthly Charges by Plan:")
st.bar_chart(avg_charges)

import matplotlib.pyplot as plt

st.header("Interactive Visualizations")

# Usage vs. Data Used
st.write("Usage Minutes vs. Data Used by Plan Type:")
fig, ax = plt.subplots()
for plan in data["PlanType"].unique():
    subset = data[data["PlanType"] == plan]
    ax.scatter(subset["UsageMinutes"], subset["DataUsedGB"], label=plan)

ax.set_xlabel("Usage Minutes")
ax.set_ylabel("Data Used (GB)")
ax.legend()
st.pyplot(fig)

st.header("Query the Database")
query = st.text_input("Enter an SQL query:", "SELECT * FROM CustomerID LIMIT 5;")
if st.button("Run Query"):
    results = pd.read_sql(query, conn)
    st.write("Query Results:")
    st.dataframe(results)

