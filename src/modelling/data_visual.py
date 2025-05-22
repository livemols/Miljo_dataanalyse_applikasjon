import pandas as pd
import numpy as np
import os
import json
import ipywidgets as widgets
from IPython.display import display
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
#The class DataVisual contains functions and methods for plotting the visuals that is displayed in data_visual.ipynb
class DataVisual:
    def __init__(self, df, main, others, limits, known_bins=None):
        self.df = df.copy()
        self.main = main
        self.others = others
        self.limits = limits.copy()
        self.bins = known_bins or self.created_bins()

    def rain_type(self):
        bins_path = os.path.join(os.getcwd(), "..", "data", "bins.json")
        with open(bins_path, "r", encoding="utf-8") as f:
            bin_defs = json.load(f)
        df = self.df.copy()
        # Load Nedbør bins
        nedbør_bins = bin_defs["Nedbør"]

        def kategoriser_nedbør(verdi):
            for kategori in nedbør_bins:
                navn, nedre, øvre = kategori  # Unpack the list
                if nedre <= verdi <= øvre:
                    return navn
            return "Ukjent"

        df["Tid"] = pd.to_datetime(df["Tid"])
        df["Year"] = df["Tid"].dt.year
        df["NedbørKategori"] = df["Nedbør"].apply(kategoriser_nedbør)





        # Makes the pie chart
        def vis_pie(year):

            data = df[df["Year"] == year]
            counts = data["NedbørKategori"].value_counts().reset_index()
            counts.columns = ["Kategori", "Antall"]

            fig = px.pie(
                counts,
                values="Antall",
                names="Kategori",
                title=f"Nedbørskategorier – {year}",
                color_discrete_sequence=px.colors.sequential.Aggrnyl,
            )
            fig.update_traces(textposition='outside', textinfo='percent+label', sort=False)
            fig.show()

        # Makes the menu
        år_valg = widgets.Dropdown(options=sorted(df["Year"].unique()), description="År:")
        widgets.interact(vis_pie, year=år_valg)           # ChatGpt assisted with column placement in template for pie chart






    # Create a Plotly Gantt-like chart to visualize the dry periods
    def plot_dry_periods(self, dry_periods_df):
        fig = px.timeline(
            dry_periods_df,
            x_start="Start",
            x_end="End",
            y="Duration",
            
            labels={"Duration": "Tørkeperioder (dager)", "Start": "Start Date", "End": "End Date"},
            color="Duration",  # Color by duration
            color_continuous_scale="Bluered",
            hover_data=["Start", "End", "Duration"]
        )

        fig.update_layout(
                xaxis_title="Dato",
                yaxis_title="Tørkeperioder(dager)",
                showlegend=False
            )
        fig.show()



        

    def plot_snow_periods(self, snow_periods_df):
        fig = px.timeline(
            snow_periods_df,
            x_start="Start",
            x_end="End",
            y="Duration",
            
            labels={"Duration": "Snø (dager)", "Start": "Start Date", "End": "End Date"},
            color="Duration",  # Color by duration
            color_continuous_scale="dense",
            hover_data=["Start", "End", "Duration"]
        )

        fig.update_layout(
                xaxis_title="Dato",
                yaxis_title="Snø(dager)",
                showlegend=False
            )
        fig.show()





    def wind_precentiles(self):
        df = self.df.copy()
        # Get wind data and sorts it
        wind_serie=df["Middelvind"]
        wind_serie=wind_serie.sort_values().values
        percentiles=np.linspace(0,100,len(wind_serie))
        # Create and plot the figure
        fig = go.Figure()
        plot_title = "Vind i percentiler"
        fig.add_trace(go.Scatter(x=percentiles, y=wind_serie, mode='lines', name='Percentile',
                                line=dict(dash='solid', width=2)))
        fig.update_layout(title_text = plot_title, xaxis_title='Percentile', yaxis_title='Vind m/s',
                        legend=dict(x=0.7,  
                                    y=0.9), 
                        xaxis_range=[0, 105],
                        showlegend=False
        )
        fig.show()
    




    def linechart_wind(self):
        df = self.df.copy()
        # Calculate statistics
        df["Year"] = df["Tid"].dt.year
        max_wind = df.groupby('Year')['Middelvind'].max().reset_index()
        min_wind = df.groupby('Year')['Middelvind'].min().reset_index()
        mean_wind = df.groupby('Year')['Middelvind'].mean().reset_index()

        # Create figure
        fig = go.Figure(data=[
            go.Bar(name='Maksimal Vind', x=max_wind['Year'], y=max_wind['Middelvind']),
            go.Bar(name='Minimal Vind', x=min_wind['Year'], y=min_wind['Middelvind']),
            go.Bar(name='Gjennomsnittlig Vind', x=mean_wind['Year'], y=mean_wind['Middelvind']),
        ])

        # Update layout
        fig.update_layout(
            barmode='group',
            title='Vindhastighet over årene',
            xaxis_title='År',
            yaxis_title='Vindhastighet(m/s)'
        )

        fig.show()
    



    def heatmap(self):
        df = self.df.copy()
        sns.set_theme()

        # Create pivot table - months vs years with temperature values
        temp_pivot = df.pivot_table(
            index=df["Tid"].dt.month,
            columns=df["Tid"].dt.year,        #ChatGpt helped debugging an error in this logic
            values="Makstemp",
            aggfunc='mean'  
        )
        f, ax = plt.subplots(figsize=(9, 6))
        sns.heatmap(temp_pivot, annot=True, fmt=".1f", linewidths=.5, ax=ax)
        ax.set_title("Heatmap")
        ax.set_xlabel("År", labelpad=10)  # Set directly on the axis
        ax.set_ylabel("Måned", labelpad=10) # Month on x-axis





    def extreme_weather_cases(self,extreme_weather):
        fig = px.bar(extreme_weather, x="Tid", y=["Makstemp", "Mintemp", "Snø", "Nedbør", "Høye vindkast"], title="Tilfeller av ekstremvær")
        fig.update_yaxes(range=[0, 220])

        fig.update_xaxes(tickmode='linear', dtick=1)
        fig.show()