import pandas as pd
import os
import sys
from tabulate import tabulate
from datetime import datetime
import matplotlib.pyplot as plt



# Find absolute path to data-file
current_dir = os.path.dirname(os.path.abspath(__file__))   # Finds folder where this file is
data_path = os.path.join(current_dir, "..", "..", "data")  # Go two folders up, then into data/

# Spesifi the filename
filename = "blindern_data_cleaning.csv"  

# Make full path til the file
file_path = os.path.join(data_path, filename)

# Sort data after ";" and format "Tid" column to datetime format
df = pd.read_csv(file_path,delimiter=";",parse_dates=['Tid'])

script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir)

print(df)


# Adds a new column for month
df['Month'] = df['Tid'].dt.month

# Sorts after month and calculate the average for every column
monthly_means = df.groupby('Month').mean(numeric_only=True)



print(tabulate(monthly_means, tablefmt="fancy_grid",headers=["Måned","Makstemp","Mintemp","Middeltemp","Snø","Nedbør","Snø", ]))
monthly_means.plot(kind="bar", title="Gjennomsnittlig målinger")
plt.show()