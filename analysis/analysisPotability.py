####
####
####
####

########################################################################################################

### IMPORTS
import data_presentation as data_presentation
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


########################################################################################################

### RQ - How can we correlate the Potability of water with the rest of the parameters?

def potability_to_ph(df: pd.DataFrame):

    clean_df = data_presentation.read_clean_general(df)
    clean_df.info()
    print(clean_df.head())
    clean_df.hist(figsize=(12,10), bins=30)
    plt.suptitle("Feature Distributions", fontsize=16)
    plt.show()

potability_to_ph('water_potability.csv')

########################################################################################################

#### TESTING ####

### Research Question 1:
### What is the distribution of genres on Netflix?
### We will define a function to plot the genre distribution
### The function will take as input a pandas DataFrame "df_genre_distribution" created in the module "data_modelling.py"

### It will return a px.plotly figure object
### The function will use seaborn to create a bar plot
### The function will set appropriate titles and labels for the plot
def plot_genre_distribution(df_genre_distribution: pd.DataFrame) -> px:
    """
    plots the distribution of genres on Netflix
    genre_distribution: pd.DataFrame
        A pandas df with genre and counts   
    returns: plt.Figure
        A matplotlib plot object
    """
    fig = px.bar(
        df_genre_distribution,
        x="count",
        y="name",
        orientation="h",
        color="count",
        color_continuous_scale="viridis",
        labels={"count": "Number of Titles", "name": "Genre"},
        title="Distribution of Genres on Netflix",
        height=600,
        width=900,
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total descending"),
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False,
    )

    return fig