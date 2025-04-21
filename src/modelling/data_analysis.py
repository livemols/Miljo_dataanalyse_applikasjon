# This file make the class data_analysis to analyze data 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.dates as mdates

class DataAnalysis:
    def __init__(self, df, main, others, limits, known_bins=None):
        self.df = df.copy()
        self.main = main
        self.others = others
        self.limits = limits.copy()
        self.bins = known_bins or self.created_bins()

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

        # Suppler automatisk med manglende grenser (50% nivå)
        for col in numeric_columns:
            if col not in self.limits:
                self.limits[col] = ((self.df[col].max() - self.df[col].min()) / 10) * 5

        # Kun kolonner som finnes i df
        gyldige_kolonner = [col for col in self.limits if col in self.df.columns]

        # Tell forekomster over faregrense per år
        df_years_severity = pd.concat({
            col: self.df.loc[self.df[col] >= self.limits[col], "Tid"].dt.year.value_counts()
            for col in gyldige_kolonner
        }, axis=1).fillna(0).astype(int).sort_index()

        return df_years_severity
    
    def df_hist(self, df):

        columns_to_plot = self.df.select_dtypes(include='number').columns.tolist()
        ncols = 2
        nrows = math.ceil(len(columns_to_plot) / ncols) # lowest int with math.ceil()

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 6, nrows * 4))
        axes = axes.flatten()  # Gjør det lettere å bruke én indeks fra 2D til 1D

        for i, column in enumerate(columns_to_plot):
            ax = axes[i]

            if column in self.bins:
                bin_def = self.bins[column]
                data = df[column]

                labels = [label for label, _, _ in bin_def] # "_" indikerer at denne variabelen ikke trengs
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

        # Fjern tomme subplot hvis det er oddetall
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        fig.tight_layout()
        plt.show()

    def years_averageplot(self, df):
        # Gjennomsnitt per mnd for hvert år fra 2015 til 2024

        # Sørg for at "Tid", "År", "Måned" er i datasettet
        self.df["Tid"] = pd.to_datetime(self.df["Tid"])
        self.df["År"] = self.df["Tid"].dt.year
        self.df["Måned"] = self.df["Tid"].dt.month

        # Velg numeriske kolonner
        numeric_columns = self.df.select_dtypes(include='number').columns.difference(["År", "Måned"])

        fig, ax = plt.subplots(len(numeric_columns), 1, figsize=(14, 4 * len(numeric_columns)))

        for i, column in enumerate(numeric_columns):
            for year in sorted(self.df["År"].unique()):
                subset = self.df[self.df["År"] == year].copy()
                
                # Lag fiktiv dato i 2020 (for å sammenligne like "dager i året" uavhengig av år)
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
