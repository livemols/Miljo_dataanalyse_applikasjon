# Since our data, blindern.csv, contains few mistakes,like missing values or duplicates. We wil add some mistakes in a new csv-file, like missing values, duplicates and outliers.

import pandas as pd
import os
import numpy as np
import numpy.ma as ma

# Find absolute path to data-file
current_dir = os.path.dirname(os.path.abspath(__file__))  # Finds folder where this file is
data_path = os.path.join(current_dir, "..","..", "data")  # Go two folders up, then into data/

# Spesifi the filename
filename = "blindern.csv"  

# Make full path til the file
original_file = os.path.join(data_path, filename)
modified_file = os.path.join(data_path, "blindern_dirty_data_generator.csv")  

# Read raw data
df = pd.read_csv(original_file,skipfooter=1, engine='python',delimiter=";")



# Add more missing value "-", because there were already "-" in the file.
# Want 30% of the rows to change 
frac = 0.3

# Choose a random row and column and change the number to "-" 
idx = np.random.choice(range(df.shape[0]), int(df.shape[0]*frac), replace=True)
cols = np.random.choice([3,4,5,6,7], size=len(idx), replace=True)
x = df.to_numpy()                                                   # My own concept and solution; ChatGPT was used to help translate it into code. 
x[idx, cols] = "-"
df=pd.DataFrame(x, index=df.index, columns=df.columns)

# ADD DUPLICATES 
# Choose the first 49 rows and add them to the end of DataFrame

rows_to_duplicate=list(range(1,50))
duplicates = df.iloc[rows_to_duplicate]  
df = pd.concat([df, duplicates], ignore_index=True)   #ChatGpt assisted with buildt-in pandas functions




# ADD OUTLIERS
# Make a list with outliers
outliers = np.array([200.5, 220.3, -500,-301, 400.5, 420.3, -200,-201])

# Choose a random row and column and change the number to one from outliers
idx1 = np.random.choice(range(df.shape[0]), int(df.shape[0]*frac), replace=True)
cols1 = np.random.choice([3,4,5,6,7], size=len(idx1), replace=True)
x1 = df.to_numpy()
x1[idx1, cols1] = np.random.choice(outliers,size=len(idx1))
df=pd.DataFrame(x1, index=df.index, columns=df.columns)




# Make DataFrame to new csv file in the same folder
df.to_csv(modified_file, index=False, sep=";")  # Keep the same delimiter (;)



print(f"Modified CSV file saved as: {modified_file}")