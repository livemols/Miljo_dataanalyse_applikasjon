import pandas as pd
import ipywidgets as widgets
from IPython.display import display
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
#The class DataVisual calculate and plots the graph for data_visual.ipynb
# The structure of the DataVisual class was organized with help from ChatGPT. Most data logic and plots were developed independently.
class DataVisual:
    def __init__(self, df, bin_defs):
        self.df = df.copy()
        self.nedbør_bins = bin_defs["Nedbør"]
        self._preprocess()

    def _kategoriser_nedbør(self, verdi):
        for navn, nedre, øvre in self.nedbør_bins:
            if nedre <= verdi <= øvre:                 # Logic was clarified and cleaned up with feedback from ChatGPT.
                return navn
        return "Ukjent"
#Prep the data for visualizing
    def _preprocess(self):
        self.df["Tid"] = pd.to_datetime(self.df["Tid"])
        self.df["Year"] = self.df["Tid"].dt.year
        self.df["NedbørKategori"] = self.df["Nedbør"].apply(self._kategoriser_nedbør)





 #The functions vis_pie and plot_rainfall plots the yearly pie graph for categorized rainfall
    def vis_pie(self, year):
        data = self.df[self.df["Year"] == year]
        if data.empty:
            print(f"Ingen data for {year}")
            return

        counts = data["NedbørKategori"].value_counts().reset_index()
        counts.columns = ["Kategori", "Antall"]

        fig = px.pie(
            counts,
            values="Antall",                     # Method was integrated into the class with assistance from ChatGPT.
            names="Kategori",
            title=f"Nedbørskategorier – {year}",
            color_discrete_sequence=px.colors.sequential.Aggrnyl,
        )
        fig.update_traces(textposition='outside', textinfo='percent+label', sort=False)
        fig.show()

    def plot_rainfall(self):
        år_valg = widgets.Dropdown(
            options=sorted(self.df["Year"].unique()), 
            description="År:"
        )
        widgets.interact(self.vis_pie, year=år_valg)





#The functions drydays and plot_dry_periods plot dry periods
    def drydays(self, grense=12):
        dry_periods = []
        count = 0
        for i, row in self.df.iterrows():
            if row["Nedbør"] <= 0:
                count += 1
            else:
                if count >= grense:
                    end_date = self.df["Tid"].iloc[i - 1].date()
                    start_date = end_date - pd.Timedelta(days=count - 1)
                    dry_periods.append({
                        "Start": start_date,
                        "End": end_date,
                        "Duration": count
                    })
                count = 0

        self.dry_periods_df = pd.DataFrame(dry_periods)        # Method was integrated into the class with assistance from ChatGPT.
        return self.dry_periods_df

    def plot_dry_periods(self, grense=12):
        dry_df = self.drydays(grense)
        if dry_df.empty:
            print("Ingen tørkeperioder funnet.")
            return

        fig = px.timeline(
            dry_df,
            x_start="Start",
            x_end="End",
            y="Duration",
            color="Duration",
            labels={
                "Duration": "Tørkeperioder (dager)",
                "Start": "Startdato",
                "End": "Sluttdato"
            },
            color_continuous_scale="Bluered",
            hover_data=["Start", "End", "Duration"]
        )

        fig.update_layout(
            title=f"Tørkeperioder (≥{grense} dager)",
            xaxis_title="Dato",
            yaxis_title="Varighet (dager)",
            showlegend=False
        )
        fig.show()





#Plots wind data in percentiles
    def plot_wind_percentiles(self):
        
        wind_serie = self.df["Middelvind"].dropna().sort_values().values
        percentiles = np.linspace(0, 100, len(wind_serie))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=percentiles,                 
            y=wind_serie,
            mode='lines',
            name='Percentile',
            line=dict(dash='solid', width=2)
        ))

        fig.update_layout(
            title_text="Vind i percentiler",
            xaxis_title='Percentil',
            yaxis_title='Vind (m/s)',
            xaxis_range=[0, 105],
            showlegend=False,
            legend=dict(x=0.7, y=0.9)
        )

        fig.show()




#Plots histogram of wind types
    def plot_yearly_wind_stats(self):
        if "Middelvind" not in self.df.columns or "Tid" not in self.df.columns:
            print("Datasettet må inneholde kolonnene 'Tid' og 'Middelvind'.")
            return

        df = self.df.copy()
        df["Year"] = df["Tid"].dt.year

        max_wind = df.groupby('Year')['Middelvind'].max().reset_index()
        min_wind = df.groupby('Year')['Middelvind'].min().reset_index()
        mean_wind = df.groupby('Year')['Middelvind'].mean().reset_index()

        fig = go.Figure(data=[
            go.Bar(name='Maksimal Vind', x=max_wind['Year'], y=max_wind['Middelvind']),
            go.Bar(name='Minimal Vind', x=min_wind['Year'], y=min_wind['Middelvind']),
            go.Bar(name='Gjennomsnittlig Vind', x=mean_wind['Year'], y=mean_wind['Middelvind']),
        ])

        fig.update_layout(
            barmode='group',
            title='Vindhastighet over årene',
            xaxis_title='År',
            yaxis_title='Vindhastighet (m/s)'
        )

        fig.show()

    



#Plots a heatmap from the monthly average of the column "Makstemp"
    def plot_temperature_heatmap(self):
        if "Tid" not in self.df.columns or "Makstemp" not in self.df.columns:
            print("Datasettet må inneholde kolonnene 'Tid' og 'Makstemp'.")
            return

        temp_pivot = self.df.pivot_table(
            index=self.df["Tid"].dt.month,
            columns=self.df["Tid"].dt.year,                                    # Method was integrated into the class with assistance from ChatGPT.
            values="Makstemp",
            aggfunc="mean"
        )

        plt.figure(figsize=(10, 6))
        sns.heatmap(temp_pivot, annot=True, fmt=".1f", linewidths=0.5, cmap="rocket", cbar_kws={'label': '°C'})
        plt.title("Gjennomsnittlig makstemperatur per måned og år")
        plt.xlabel("År", labelpad=10)
        plt.ylabel("Måned", labelpad=10)
        plt.yticks(rotation=0)
        plt.show()



        

#Plots cases of extreme weather base on the method year_severity from data_analysis.py
    def plot_extreme_weather_cases(self, ekstremvær_df):
        """
        Plotter en oversikt over ekstreme værtilfeller per år.

        Parametere:
        - ekstremvær_df: DataFrame med kolonner ["Tid", "Makstemp", "Mintemp", "Snø", "Nedbør", "Høye vindkast"]
        """
        if ekstremvær_df.empty or "Tid" not in ekstremvær_df.columns:
            print("Ugyldig DataFrame: Mangler 'Tid' eller er tom.")        # Method was integrated into the class with assistance from ChatGPT.
            return

        fig = px.bar(
            ekstremvær_df,
            x="Tid",
            y=["Makstemp", "Mintemp", "Snø", "Nedbør", "Høye vindkast"],
            title="Tilfeller av ekstreme vær",
        )

        fig.update_yaxes(range=[0, 220])
        fig.update_xaxes(tickmode='linear', dtick=1)
        fig.show()
