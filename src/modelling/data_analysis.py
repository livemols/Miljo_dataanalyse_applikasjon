# This file make the class data_analysis to analyze data

# This file has used ChatGPT (OpenAI) for troubleshooting and explanation of error codes.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.dates as mdates
from statistics import mode
import seaborn as sns

class DataAnalysis:
    def __init__(self, df=None, main=None, others=None, limits=None, known_bins=None):
        self.df = df.copy() if df is not None else None
        self.main = main if main is not None else None
        self.others = others if others is not None else None
        self.limits = limits.copy() if limits is not None else None
        self.known_bins = known_bins if known_bins is not None else {}

    def statistical_values(self, df):
        df['Tid'] = pd.to_datetime(df['Tid'], errors='coerce')

        # Calculate the average, median and standard deviation for each column
        stats_df = pd.DataFrame({
            "Gjennomsnitt": df.mean(numeric_only=True).round(2),
            "Median": df.median(numeric_only=True).round(2),
            "Standardavvik": df.std(numeric_only=True).round(2)
        })
        print("Statistiske verdier for hver kolonne:")
        print(stats_df)

        # Calculate the seasonal average, median and standard deviation for each column
        def season(dato):
            month = dato.month
            if month in [12,1,2]:
                return "Vinter"
            elif month in [3,4,5]:
                return "Vår"
            elif month in [6,7,8]:
                return "Sommer"
            elif month in [9,10,11]:
                return "Høst"

        df['Sesong'] = df['Tid'].apply(season)

        print(f"Gjennomsnittet for hver sesong er:\n{(df.groupby('Sesong').mean(numeric_only=True)).T.round(2)}")
        print(f"Median for hver sesong er:\n{(df.groupby('Sesong').median(numeric_only=True)).T.round(2)}")
        print(f"Standardavviket for hver sesong er:\n{(df.groupby('Sesong').std(numeric_only=True)).T.round(2)}")

    def drydays(self, df, limit = 12, format = "print"):
        count = 0
        no_rain_days, dry_periods=[], []

        #Calculates the dataframe with dates and length of the period
        if format != "print":
            for i in range(len(df)-1):
                if df["Nedbør"][i] <= 0:
                    count += 1
                else:
                    if count >= limit:
                        end_date = pd.to_datetime(df["Tid"][i-1]).date()
                        start_date = end_date - pd.Timedelta(days=count-1)
                        dry_periods.append({
                            "Start": start_date,
                            "End": end_date,
                            "Duration": count
                        })
                    count = 0
            return pd.DataFrame(dry_periods)
        
        #Prints the length of the periods, the mode and the limit
        else: 
            for rain in range(len(df)-1):
                if df["Nedbør"][i] <= 0:
                    count += 1
                else:
                    if count >= limit:
                        no_rain_days.append(count)
                    count = 0     
            print(f"Antall dager uten nedbør etter en annen: {no_rain_days}")
            print(f"Typetall for antall dager uten nedbør sammenhengende: {mode(no_rain_days)}\nMinste antall dager er {limit}")

    def snowdays(self, df, limit = 5, format="print"):
        count = 0
        snowdays,snow_periods = [], []
        
        #Calculates the dataframe with dates and length of the period
        if format != "print":
            for i in range(len(df)-1):
                if df["Snø"][i] > 0:
                    count += 1
                else:
                    if count >= limit:
                        end_date = pd.to_datetime(df["Tid"][i-1]).date()
                        start_date = end_date - pd.Timedelta(days=count-1)
                        snow_periods.append({
                            "Start": start_date,
                            "End": end_date,
                            "Duration": count
                        })
                    count = 0

            return pd.DataFrame(snow_periods)
        
        #Prints the length of the periods, the mode and the limit
        else:
            for i in range(len(df)-1):
                if df["Snø"][i] > 0:
                    count += 1
                else:
                    if count >= limit:
                        snowdays.append(count)
                    count=0
            print(f"Antall dager med snø etter en annen: {snowdays}")
            print(f"Typetall for antall dager med snø sammenhengende: {mode(snowdays)}\nMinste antall dager er {limit}")

    def scatterplot(self, df, main, others):
        for column in others:
            plt.figure(figsize=(6, 3))
            plt.scatter(df[main], df[column], color='skyblue', edgecolor='black')
            plt.title(f'Sammenheng mellom {main.lower()} og {column.lower()}')
            plt.xlabel(f'{main} (°C)')
            plt.ylabel(f'{column} (mm)')
            plt.grid(True)
            plt.show()

    def years_max(self, df):
        df = df.copy()
        df["Tid"] = pd.to_datetime(df["Tid"])
        df["Tid"] = df["Tid"].dt.year
        numeric_columns = df.select_dtypes(include='number').columns
        
        # Takes the minimum values of mintemp, and the maximum value of everything else except middeltemp (per year). 
        
        agg_funcs = {}                                  # ChatGPT assisted with buildt-in pandas functions
        for col in numeric_columns:
            if col == "Mintemp":
                agg_funcs[col] = "min"
            elif col != "Middeltemp" and col != "Tid":
                agg_funcs[col] = "max"

        return df.groupby("Tid").agg(agg_funcs)

    def years_severity(self, df, limits):
        df["Tid"] = pd.to_datetime(df["Tid"])
        numeric_columns = df.select_dtypes(include='number').columns

        # Automatically supplement missing boundaries (25% (5/20) and 50% (5/10) highest level)
        agg_funcs = {}
        for col in numeric_columns:
            if col not in limits:
                if col == "Mintemp":
                    limits[col] = ((df[col].min() - df[col].max()) / 20) * 5
                elif col != "Tid":
                    limits[col] = ((df[col].max() - df[col].min()) / 10) * 5

        # Only colums who exist in df
        valid_columns = [col for col in limits if col in df.columns]

        # Count occurrences above danger limit per year . 
        results = {}
        for col in valid_columns:
            if col == "Mintemp":
                mask = df[col] <= limits[col]
            else:
                mask = df[col] >= limits[col]
            
            years = df.loc[mask, "Tid"].dt.year
            results[col] = years.value_counts()
            df_years_severity = pd.DataFrame(results).fillna(0).astype(int).sort_index() 
        
        df_years_severity = df_years_severity.reset_index() # ChatGPT assisted with buildt-in pandas functions

        return df_years_severity, limits
    
    def df_hist(self, df, known_bins):

        columns_to_plot = df.select_dtypes(include='number').columns.tolist()
        ncols = 2
        nrows = math.ceil(len(columns_to_plot) / ncols) # Lowest int with math.ceil()

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 6, nrows * 4))
        axes = axes.flatten()  # Makes it easier to use one index from 2D to 1D

        for i, column in enumerate(columns_to_plot):
            ax = axes[i]

            if column in known_bins:
                bin_def = known_bins[column]
                data = df[column]

                labels = [label for label, _, _ in bin_def] # "_" indicates that this variable is not needed
                bin_edges = [start for _, start, _ in bin_def] + [bin_def[-1][2]]
                bin_edges = sorted(set(bin_edges))

                data_cut = pd.cut(data, bins=bin_edges, labels=labels, right=True, include_lowest=True, duplicates='drop')
                counts = data_cut.value_counts().sort_index()

                ax.bar(range(len(counts)), counts.values, color='skyblue')
                ax.set_xticks(range(len(counts)))
                ax.set_xticklabels(counts.index, rotation=45, ha='right')

            else:
                ax.hist(df[column], bins=10, color="green", edgecolor="black")

            ax.set_title(f"{column}")
            ax.set_xlabel(column)
            ax.set_ylabel("Antall dager")

        # Remove empty subplot if it is an odd number
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        fig.tight_layout()
        plt.show()

    def years_averageplot(self, df):
        df['Tid'] = pd.to_datetime(df['Tid'])
        df['Dag'] = df['Tid'].dt.day
        df['Måned'] = df['Tid'].dt.month
        df['Ukedag'] = df['Tid'].dt.weekday
        df['År'] = df['Tid'].dt.year
        # Goes through numerical columns, except 'Tid', 'Dag'; 'Måned', 'Ukedag', 'År'
        for column in df.select_dtypes(include=np.number).columns:
            if column not in ['Tid', 'Dag', 'Måned', 'Ukedag', 'År']:
                per_måned = df.groupby(['År', 'Måned'])[column].sum().reset_index()
                plt.figure(figsize=(14,6))
                sns.barplot(data=per_måned, x='Måned', y=column, hue='År', palette='coolwarm')
                plt.title(f'Total månedlig {column.lower()} per år')
                plt.xlabel('Måned')
                plt.ylabel(f'{column} (mm)')
                plt.legend(title='År')
                plt.show()