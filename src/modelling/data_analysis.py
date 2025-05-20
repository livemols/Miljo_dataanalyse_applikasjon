#from dataclasses import dataclass

#@dataclass
#class VærKategori:
#    navn: str
#    nedre_grense: float
#    øvre_grense: float

#bins = {
#    "Nedbør": [
#        VærKategori("Pent vær", 0.0, 0.0),
#        VærKategori("Stort sett oppholdsvær", 0.0001, 0.4),
#        VærKategori("Litt nedbør", 0.5, 2.0),
#        VærKategori("Regn/sludd/snø/byger", 2.0001, 20.0),
#        VærKategori("Store mengder", 20.0001, 200.0),
#    ],
#    "Vind": [
#        VærKategori("Stille", 0.0, 0.2),
#        VærKategori("Flau vind", 0.3, 1.5),
#        VærKategori("Svak vind", 1.6, 3.3),
#        VærKategori("Lett bris", 3.4, 5.4),
#        VærKategori("Laber bris", 5.5, 7.9),
#        VærKategori("Frisk bris", 8.0, 10.7),
#        VærKategori("Liten kuling", 10.8, 13.8),
#        VærKategori("Stiv kuling", 13.9, 17.1),
#        VærKategori("Sterk kuling", 17.2, 20.7),
#        VærKategori("Liten storm", 20.8, 24.4),
#        VærKategori("Full storm", 24.5, 28.4),
#        VærKategori("Sterk storm", 28.5, 32.6),
#        VærKategori("Orkan", 32.7, 200.0),
#    ],
#}

# NB: Precipitation is for the last 24 hours, but downpour is only for one hour. Wind is in m/s
# Limits is form https://www.met.no/vaer-og-klima/begreper-i-vaervarsling, 14.april 2025


# This file make the class data_analysis to analyze data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.dates as mdates
from statistics import mode

class DataAnalysis:
    def __init__(self, df, main, others, limits, known_bins=None):
        self.df = df.copy()
        self.main = main
        self.others = others
        self.limits = limits.copy()
        self.bins = known_bins or self.created_bins()

    def statistical_values(self):
        df = self.df.copy()
        df['Tid'] = pd.to_datetime(df['Tid'], errors='coerce')

        # Calculate the average, median and standard deviation for each column
        print(f"The average for each column is:\n{df.mean(numeric_only=True)}")
        print(f"The median for each column is:\n{df.median(numeric_only=True)}")
        print(f"The standard deviation for each column is:\n{df.std(numeric_only=True)}")

        # Calculate the seasonal average, median and standard deviation for each column
        def season(dato):
            month=dato.month
            if month in [12,1,2]:
                return "Winter"
            elif month in [3,4,5]:
                return "Spring"
            elif month in [6,7,8]:
                return "Summer"
            elif month in [9,10,11]:
                return "Autumn"

        df['season'] = df['Tid'].apply(season)

        print(f"The average for each season is:\n{df.groupby('season').mean(numeric_only=True)}")
        print(f"The median for each season is:\n{df.groupby('season').median(numeric_only=True)}")
        print(f"The standard deviation for each season is:\n{df.groupby('season').std(numeric_only=True)}")

    def drydays(self, limit=12, format="print"):
        count=0
        no_rain_days, dry_periods=[], []
        df = self.df.copy()

        #Calculates the dataframe with dates and length of the period
        if format !="print":
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
            for i in range(len(df)-1):
                if df["Nedbør"][i] <= 0:
                    count += 1
                else:
                    if count >=limit:
                        no_rain_days.append(count)
                    count=0     
            print(f"Antall dager uten nedbør etter en annen: {no_rain_days}")
            print(f"Typetall for antall dager uten nedbør sammenhengende: {mode(no_rain_days)}\nMinste antall dager er {limit}")

    def snowdays(self, limit=5, format="print"):
        count=0
        snowdays,snow_periods = [], []
        df = self.df.copy()
        
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

    def scatterplot(self):
        for column in self.others:
            plt.figure(figsize=(6, 3))
            plt.scatter(self.df[self.main], self.df[column], color='skyblue', edgecolor='black')
            plt.title(f'Sammenheng mellom {self.main.lower()} og {column.lower()}')
            plt.xlabel(f'{self.main} (°C)')
            plt.ylabel(f'{column} (mm)')
            plt.grid(True)
            plt.show()

    def years_max(self):
        df = self.df.copy()
        df["Tid"] = pd.to_datetime(df["Tid"])
        df["Tid"] = df["Tid"].dt.year
        numeric_columns = df.select_dtypes(include='number').columns
        return df.groupby("Tid")[numeric_columns].max()

    def years_severity(self):
        self.df["Tid"] = pd.to_datetime(self.df["Tid"])
        numeric_columns = self.df.select_dtypes(include='number').columns

        # Automatically supplement missing boundaries (50% level)
        for col in numeric_columns:
            if col not in self.limits:
                self.limits[col] = ((self.df[col].max() - self.df[col].min()) / 10) * 5

        # Only colums who exist in df
        gyldige_kolonner = [col for col in self.limits if col in self.df.columns]

        # Count occurrences above danger limit per year
        df_years_severity = pd.concat({
            col: self.df.loc[self.df[col] >= self.limits[col], "Tid"].dt.year.value_counts()
            for col in gyldige_kolonner
        }, axis=1).fillna(0).astype(int).sort_index()

        return df_years_severity
    
    def df_hist(self, df):

        columns_to_plot = self.df.select_dtypes(include='number').columns.tolist()
        ncols = 2
        nrows = math.ceil(len(columns_to_plot) / ncols) # Lowest int with math.ceil()

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 6, nrows * 4))
        axes = axes.flatten()  # Makes it easier to use one index from 2D to 1D

        for i, column in enumerate(columns_to_plot):
            ax = axes[i]

            if column in self.bins:
                bin_def = self.bins[column]
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
        # Average per month for each year from 2014 to 2024

        # Make sure that "Tid", "År" and "Måned" are in the dataset
        self.df["Tid"] = pd.to_datetime(self.df["Tid"])
        self.df["År"] = self.df["Tid"].dt.year
        self.df["Måned"] = self.df["Tid"].dt.month

        # Select numeric columns
        numeric_columns = self.df.select_dtypes(include='number').columns.difference(["År", "Måned"])

        fig, ax = plt.subplots(len(numeric_columns), 1, figsize=(14, 4 * len(numeric_columns)))

        for i, column in enumerate(numeric_columns):
            for year in sorted(self.df["År"].unique()):
                subset = self.df[self.df["År"] == year].copy()
                
                # Create fictitious date in 2020 (to compare equal "days of the year" regardless of year)
                subset["Tid_syntetisk"] = pd.to_datetime("2020-" + subset["Tid"].dt.strftime("%m-%d"))
                
                ax[i].plot(subset["Tid_syntetisk"], subset[column], label=str(year), linewidth=0.8)

            ax[i].set_title(f"{column} – daglig utvikling per år")
            ax[i].set_xlabel("Måned")
            ax[i].set_ylabel(column)
            ax[i].xaxis.set_major_locator(mdates.MonthLocator())
            ax[i].xaxis.set_major_formatter(mdates.DateFormatter('%b'))  # Jan, Feb, ...
            ax[i].legend()
            ax[i].grid(True)

        plt.tight_layout()
        plt.show()
