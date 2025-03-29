#Siden dataen vår, blindern.csv, inneholder lite feil som missing values og duplikater, skal vi i denne filen addere noen feil i en ny cvs.

#Denne filen renser og behandler dataen vår
import pandas as pd
import os
import numpy as np
import numpy.ma as ma

# Finn absolutt sti til data-mappen
current_dir = os.path.dirname(os.path.abspath(__file__))  # Finner mappen der testnat.py er
data_path = os.path.join(current_dir, "..","..", "data")  # Går én mappe opp, deretter inn i data/

# Spesifiser filnavnet
filename = "blindern.csv"  

# Lag full sti til filen
original_file = os.path.join(data_path, filename)
modified_file = os.path.join(data_path, "blindern_dirty_data_generator.csv")  

# leser rådata
df = pd.read_csv(original_file,skipfooter=1, engine='python',delimiter=";")




#Adderer flere missing value "-", siden det var allerede slik fra før, i dataen
#vil at 30% av radene skal endres
frac = 0.3

#velger en random rad og columm og endrer tallet til "-"
idx = np.random.choice(range(df.shape[0]), int(df.shape[0]*frac), replace=True)
cols = np.random.choice([3,4,5,6,7], size=len(idx), replace=True)
x = df.to_numpy()
x[idx, cols] = "-"
df=pd.DataFrame(x, index=df.index, columns=df.columns)


#ADDERER DUPLIKATER
#velger de første 49 radene og addere de på slutten av DataFrame
rows_to_duplicate=list(range(1,50))
duplicates = df.iloc[rows_to_duplicate]  
df = pd.concat([df, duplicates], ignore_index=True)





#ADDERER OUTLIERS

#lager en liste med outliers
outliers = np.array([200.5, 220.3, -500,-301, 400.5, 420.3, -200,-201])


#velger en random rad og columm og endrer tallet til en fra outliers
idx1 = np.random.choice(range(df.shape[0]), int(df.shape[0]*frac), replace=True)
cols1 = np.random.choice([3,4,5,6,7], size=len(idx1), replace=True)
x1 = df.to_numpy()
x1[idx1, cols1] = np.random.choice(outliers,size=len(idx1))
df=pd.DataFrame(x1, index=df.index, columns=df.columns)





# lagrer DataFrame til ny cvs fil i samme mappe
df.to_csv(modified_file, index=False, sep=";")  # Holder den samme delimiter (;)



print(f"Modified CSV file saved as: {modified_file}")