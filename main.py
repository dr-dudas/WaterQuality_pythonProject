##################################################
##################################################
######### Water Quality Data Analysis ############
##################################################
##################################################

###### WORK IN PROGRESS ####
###### main.py ######


### This is for the group work, collaborative part of your final project
### This is just a template, feel free to modify the layout, and look and feel as needed

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc



### Your modules
import analysis.data_modelling as dm # loading in your data_modeling.py
import analysis.analysisMissingValues as vis_rq1 # loading in analysisMissingValues - individual analysis module
#import analysis.analysisPotability as vis_rq2 # loading in analysisPotability - individual analysis module
#import analysis.analysis_rq3 as vis_rq3 # loading in your individual analysis module
#import analysis.analysis_rq4 as vis_rq4 # loading in your individual analysis module
#import analysis.analysis_rq5 as vis_rq5 # loading in your individual analysis module


# load in the dataset
# in our example, we use the Netflix dataset
df = pd.read_csv("data/water_potability.csv")


# call visualizations
# This is your individual work, each one of you will have different figures
# REPLACE BY YOUR OWN FIGURES AND TEXTS
title_rq1 = "RQ1: How do missing values and data quality issues affect the reliability of potability predictions?"
text_rq1_1 = text_rq1_1 = (
    "This analysis explores the frequency missing values and explore those parameters "
    "and frequenzy compared to the potability of water.\n"
    "Let's start by checking for missing values in each column:\n\n"
    f"{dm.missing_values_summary(df)}"
)

fig_rq1_1 = vis_rq1.missing_values_heatmap(df)
rq1_plot1_1_id = "Missing values heatmap"
###
text_rq1_2 = "It's clear from the heatmap that missing values of 'ph', 'Sulfate', and 'Trihalomethanes' are scattered throughout the dataset. \nLet's analyze the distribution of these columns with missing values and see how they relate to the target variable 'Potability'."
target = 'Potability'
col_missing_values = ['ph', 'Sulfate', 'Trihalomethanes']
new_col = 'missing_value'
fig_rq1_2 = vis_rq1.compare_distributions(df, col_missing_values, target)
rq1_plot1_2_id = "Distributions of columns with missing values vs Potability"

###
text_rq1_3 = (
    "From the distributions in the histograms, we observe that the missing values in 'ph', 'Sulfate', and 'Trihalomethanes' "
    "do not show a strong bias towards either class of 'Potability'.\n"
    "Even high or low values of these features are present in both potable and non-potable water samples.\n"
    "Further statistical analysis can be performed to quantify the relationship between missing values and potability.\n"
    "We will compute this correlation between the presence of missing values and potability.\n"
    "Does 1 or more missing values in a row correlate with potability?\n"
    "Let's compute and plot the percentage of potability for each count of missing values."
)
fig_rq1_3 = vis_rq1.plot_percentages(vis_rq1.compute_percentages(df, new_col, target))
rq1_plot1_3_id = "Percentage of Potability vs Missing Values"
###
text_rq1_4 = (
    "The stacked bar chart shows the percentage of potable and non-potable water samples for each "
    "count of missing values.\n "
    "We can see that as the number of missing values increases, the average potability tends to decrease, but the trend is not very strong.\n"
    "First when we have 3 missing values do we see a significant drop in potability - but the amount of data on those are low."
    "We conclude that the missing values of pH, Sulfate, and Trihalomethanes have very limited correlation with the potability of water samples."
)


title_rq2 = "RQ2: How can we correlate the Potability of water with the rest of the parameters?"
text_rq2 = "YOUR THOROUGH EXPLANATION HERE"
fig_rq2 = None  # YOUR CODE
rq2_plot_id = "your-plot"

# Placeholder for more research questions


# Repeat the same pattern for RQ2, RQ3, etc.
# UNCOMMENT AND MODIFY THE FOLLOWING LINES FOR EACH ADDITIONAL RQ
# Replace 'X' with the respective research question number
#title_rqX = "RQx : YOUR TITLE HERE"
#text_rqX = "YOUR THOROUGH EXPLANATION HERE"
#fig_rX = YOUR CODE
#rqX_plot_id = "genre-plot"


# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        # Dashboard Title
        html.H1("Water Quality Data Analysis", className="text-center my-4"),

        # Research Question 1
        dbc.Row(
            dbc.Col(html.H3(title_rq1,
                            className="text-center text-primary"), width=12),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(html.P(
                text_rq1_1,
                className="text-center lead"), width=12),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id=rq1_plot1_1_id, figure=fig_rq1_1), width=12),
            className="mb-5"
        
        ),
        # Additional text and plots for RQ1
         dbc.Row(
            dbc.Col(html.P(
                text_rq1_2,
                className="text-center lead"), width=12),
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="rq1_plot_ph", figure=fig_rq1_2["ph"]),
                    width=4
                ),
                dbc.Col(
                    dcc.Graph(id="rq1_plot_sulfate", figure=fig_rq1_2["Sulfate"]),
                    width=4
                ),
                dbc.Col(
                    dcc.Graph(id="rq1_plot_trihalo", figure=fig_rq1_2["Trihalomethanes"]),
                    width=4
                ),
            ],
            className="mb-5"
        ),

        
        # Additional text and plots for RQ1
         dbc.Row(
            dbc.Col(html.P(
                text_rq1_3,
                className="text-center lead"), width=12),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id=rq1_plot1_3_id, figure=fig_rq1_3), width=12),
            className="mb-5"
        
        ),
        dbc.Row(
            dbc.Col(html.P(
                text_rq1_4,
                className="text-center lead"), width=12),
            className="mb-4"
        ),
        # Additional text and plots for RQ1

        # Research Question 2
        #dbc.Row(
            #dbc.Col(html.H3(title_rq2,
                            #className="text-center text-primary"), width=12),
            #className="mb-3"
        #),
        #dbc.Row(
            #dbc.Col(html.P(
        #        text_rq2,
        #        className="text-center lead"), width=12),
        #    className="mb-4"
        #),
        #dbc.Row(
        #    dbc.Col(dcc.Graph(id=rq2_plot_id, figure=fig_rq2), width=12),
        #    className="mb-5"
        #),
        # Placeholder for more research questions
        # Repeat the same pattern for RQ2, RQ3, etc.
        # UNCOMMENT AND MODIFY THE FOLLOWING LINES FOR EACH ADDITIONAL RQ
        # Research Question X
        # dbc.Row(
        #    dbc.Col(html.H3(title_rqX,
        #                    className="text-center text-primary"), width=12),
        #    className="mb-3"
        #),
        #dbc.Row(
        #    dbc.Col(html.P(
        #        text_rqX,
        #        className="text-center lead"), width=12),
        #    className="mb-4"
        #),
        #dbc.Row(
        #    dbc.Col(dcc.Graph(id=rqX_plot_id, figure=fig_rqX), width=12),
        #    className="mb-5"
        #),

    ],
    fluid=True
)

### You can create callbacks here if needed for interactivity
### For example, if you want to update plots based on user input
### You can define your callbacks below
### It is optional. Bonus points if you implement interactivity!!!

if __name__ == "__main__":
    app.run(debug=True)

###
### To see the results of your work, run this file (main.py)
### Then open your web browser and go to the website:
### Dash is running on http://127.0.0.1:8050/
###

### All the best of success with your final project!!!