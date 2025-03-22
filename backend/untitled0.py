# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1B85p0GJA-Xjcr9fGknCDDIHoIBwmj82Y
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("All required libraries are successfully imported!")


import tkinter as tk
from tkinter import filedialog

#root = tk.Tk()
#root.withdraw()  # Hide the main window
#file_path = filedialog.askopenfilename()  # Open file dialog
print("untitled0.py", "D:/vscodefol/Philanthropy_Insights/Philanthropy_Insights_Platform/backend")



import pandas as pd

# Read the uploaded file
df = pd.read_csv("D:/vscodefol/Philanthropy_Insights/Philanthropy_Insights_Platform/dataset/processed_philanthropy_data.csv")


# Display the first few rows
df.head()

# Display the first few rows
df.head()

# Check dataset structure
df.info()

# Summary statistics of numerical columns
df.describe()

df.isnull().sum()

df.fillna(df.select_dtypes(include=['number']).mean(), inplace=True)
 # Fills missing values with column mean

print(df.columns)

df.columns = df.columns.str.strip().str.lower()  # Remove spaces & convert to lowercase
print(df.columns)  # Check again

total_donations = df['donation amount'].sum()
print(f"Total Donations: ${total_donations}")

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

total_donations = df['donation_amount'].sum()

print(df.isnull().sum())  # Check missing values in each column

print(df.describe())  # Get summary statistics (min, max, mean, etc.)
print(df['donation_cause'].value_counts())  # Find top donation causes

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8,5))
sns.histplot(df['donation_amount'], bins=20, kde=True)
plt.title("Donation Amount Distribution")
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Convert 'date_of_last_donation' to datetime format
df['date_of_last_donation'] = pd.to_datetime(df['date_of_last_donation'], format='%d-%m-%Y')


# Plot donation trends over time (monthly)
df.set_index('date_of_last_donation').resample('ME')['donation_amount'].sum().plot(kind='line')

plt.title("Monthly Donation Trends")
plt.xlabel("Date")
plt.ylabel("Total Donations")
plt.grid(True)
plt.show()

df['date_of_last_donation'] = pd.to_datetime(df['date_of_last_donation'], format='%d-%m-%Y', errors='coerce')

df.set_index('date_of_last_donation').resample('ME')['donation_amount'].sum().plot(kind='line')

top_donors = df.groupby('donor_id')['donation_amount'].sum().sort_values(ascending=False).head(10)
print(top_donors)

import matplotlib.pyplot as plt

df.resample('ME', on='date_of_last_donation')['donation_amount'].sum().plot(kind='line', marker='o')
plt.title('Monthly Donation Trends')
plt.xlabel('Month')
plt.ylabel('Total Donations')
plt.grid()
plt.show()

df.groupby('gender')['donation_amount'].sum().plot(kind='bar', title="Total Donations by Gender")
plt.ylabel("Total Donations")
plt.show()

df['age_group'] = pd.cut(df['age'], bins=[18, 30, 50, 70, 100], labels=['18-30', '31-50', '51-70', '71+'])
df.groupby('age_group', observed=False)['donation_amount'].sum().plot(kind='bar', title="Total Donations by Age Group")

plt.ylabel("Total Donations")
plt.show()

df.groupby('cluster')['donation_amount'].sum().plot(kind='bar', title="Donations by Cluster")
plt.ylabel("Total Donations")
plt.show()

df.to_csv('processed_philanthropy_data_cleaned.csv', index=False)

df['donation_cause'].value_counts().plot(kind='bar', title="Top Donation Causes")
plt.ylabel("Number of Donations")
plt.show()

from sklearn.cluster import KMeans

X = df[['donation_amount', 'donation_frequency']]
kmeans = KMeans(n_clusters=3)
df['donor_cluster'] = kmeans.fit_predict(X)

df.groupby('donor_cluster')['donation_amount'].mean().plot(kind='bar', title="Average Donation by Cluster")
plt.ylabel("Donation Amount")
plt.show()

import plotly.express as px

fig = px.histogram(df, x='donation_amount', nbins=20, title="Donation Distribution")
fig.show()

df.to_csv('final_philanthropy_insights.csv', index=False)



import streamlit as st

st.title("Philanthropy Insights Dashboard")
st.write(f"Total Donations: ${total_donations}")
st.bar_chart(df.groupby('donation_cause')['donation_amount'].sum())

plt.savefig("monthly_donation_trend.png")





"""# New Section"""

# Summary of numerical columns
df.describe()

import matplotlib.pyplot as plt

# Convert to datetime format
df["date_of_last_donation"] = pd.to_datetime(df["date_of_last_donation"])

# Aggregate monthly donation amounts
monthly_donations = df.set_index("date_of_last_donation").resample("M")["donation_amount"].sum()

# Plot the trend
plt.figure(figsize=(10,5))
plt.plot(monthly_donations, marker="o", linestyle="-", color="b")
plt.title("Monthly Donation Trends")
plt.xlabel("Month")
plt.ylabel("Total Donation Amount")
plt.grid(True)
plt.show()

import seaborn as sns

plt.figure(figsize=(12,6))
sns.barplot(x=df["donation_cause"].value_counts().index,
            y=df["donation_cause"].value_counts().values,
            palette="viridis")

plt.title("Number of Donations Per Cause")
plt.xlabel("Donation Cause")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(8,5))
sns.histplot(df["donation_amount"], bins=20, kde=True, color="g")
plt.title("Distribution of Donation Amounts")
plt.xlabel("Donation Amount")
plt.ylabel("Frequency")
plt.show()

df.to_csv("final_philanthropy_analysis.csv", index=False)

#from google.colab import files
#files.download("final_philanthropy_analysis.csv")