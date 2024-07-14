import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the SQLite database
conn = sqlite3.connect('sensor_data.db')

# Query to retrieve data
query = "SELECT * FROM sensor_data"

# Load data into a DataFrame
data = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Display the data in a table
st.write("Sensor Data", data)

# Visualize the data
st.write("Correlation Heatmap")
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
st.pyplot(plt)

# Additional plots as needed
st.write("Temperature over Time")
plt.figure(figsize=(10, 5))
plt.plot(data['Temperature'], label='Temperature')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Temperature')
st.pyplot(plt)
