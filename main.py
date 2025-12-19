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
import plotly.express as px
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

### Your modules
import analysis.data_modelling as dm # loading in your data_modeling.py
import analysis.analysisMissingValues as vis_rq1 # loading in analysisMissingValues - individual analysis module
import analysis.analysisPotability as vis_rq2 # loading in analysisPotability - individual analysis module
#import analysis.analysis_rq3 as vis_rq3 # loading in your individual analysis module
#import analysis.analysis_rq4 as vis_rq4 # loading in your individual analysis module
import analysis.analysisInfluence as vis_rq5 # loading in your individual analysis module


# load in the dataset
# in our example, we use the Netflix dataset
df = dm.basic_cleaning("data/water_potability.csv")
df_rq2 = dm.read_clean_general("data/water_potability.csv")

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
text_rq1_2 = "It's clear from the heatmap that missing values of 'ph', 'sulfate', and 'trihalomethanes' are scattered throughout the dataset. \nLet's analyze the distribution of these columns with missing values and see how they relate to the target variable 'Potability'."
target = 'potability'
col_missing_values = ['ph', 'sulfate', 'trihalomethanes']
new_col = 'missing_value'
ph = "ph"
sulfate = "sulfate"
trih = "trihalomethanes"
fig_rq1_2 = vis_rq1.compare_distributions(df, col_missing_values, target)
rq1_plot1_2_id = "Distributions of columns with missing values vs potability"

###
text_rq1_3 = (
    "From the distributions in the histograms, we observe that the missing values in 'ph', 'sulfate', and 'trihalomethanes' "
    "do not show a strong bias towards either class of 'potability'.\n"
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
    "We conclude that the missing values of ph, sulfate, and trihalomethanes have very limited correlation with the potability of water samples."
)


title_rq2 = "RQ2: How can we correlate the Potability of water with the rest of the parameters?"
text_rq2 = (
    "The purpose of this research question is to find if there is any correlation" \
    "between the potability of the water and the rest of the parameters measured. \n" \
    "\n For starters, we've created a correlation heatmap function, shown below"
)
fig_rq2_0 = dm.correlation_heatmap(df_rq2)

text_rq2_2 = "Given our correlation heatmap, we can see that hardly any other parameter" \
            "correlate with Potability but just to be sure, we'll select the parameters with the highest" \
            "correlation values to see whether or not this is true. \n" \
            "Those parameters are: Solids and Chloramines and we'll show the relationship with Potability through" \
            "box plots and t-tests" 
fig_rq2_1 = vis_rq2.boxplot_chloramines(df_rq2)  # YOUR CODE
rq2_plot1_id = "Chloramines vs Potability boxplot"
fig_rq2_2 = vis_rq2.boxplot_solids(df_rq2)
rq2_plot2_id = "Solids vs Potability boxplot"
text_rq2_3 = ""


####Q5
title_rq5 = "RQ5: Which water quality parameter has the strongest predictive influence on potability?"

text_rq5 = (
    "This research question investigates which water quality parameter has the "
    "strongest relationship with the potability label. We compute the correlation "
    "between each numeric parameter and Potability, and rank them by absolute "
    "correlation strength."
)

corr_rq5 = vis_rq5.compute_potability_correlations(df_rq2)
fig_rq5 = vis_rq5.plot_potability_correlation_bar(corr_rq5)

rq5_plot_id = "rq5-correlation-bar"
###
# Dropdown options = all numeric columns except Potability
rq5_params = [c for c in df_rq2.select_dtypes(include="number").columns if c != "Potability"]
rq5_default_param = rq5_params[0] if rq5_params else None

####
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
            dbc.Col(dcc.Graph(id=rq1_plot1_1_id, figure=fig_rq1_1), width=8),
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
                    dcc.Graph(id="q1_plot_ph", figure=fig_rq1_2[ph]),
                    width=4
                ),
                dbc.Col(
                    dcc.Graph(id="rq1_plot_sulfate", figure=fig_rq1_2[sulfate]),
                    width=4
                ),
                dbc.Col(
                    dcc.Graph(id="rq1_plot_trihalo", figure=fig_rq1_2[trih]),
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
        dbc.Row(
            dbc.Col(html.H3(title_rq2,
                            className="text-center text-primary"), width=12),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(html.P(
                text_rq2,
                className="text-center lead"), width=12),
            className="mb-4"
        ),

        dbc.Row(
            dbc.Col(dcc.Graph(id=rq2_plot1_id, figure=fig_rq2_0), width=12),
            className="mb-5"
        ),
        
        dbc.Row(
            dbc.Col(html.P(
                text_rq2_2,
                className="text-center lead"), width=12),
            className="mb-4"
        ),

        dbc.Row(
            dbc.Col(dcc.Graph(id=rq2_plot1_id, figure=fig_rq2_1), width=12),
            className="mb-5"
        ),

         dbc.Row(
            dbc.Col(dcc.Graph(id=rq2_plot2_id, figure=fig_rq2_2), width=12),
            className="mb-5"
        ),

        # Research Question 5

        dbc.Row(
            dbc.Col(html.H3(title_rq5,
                            className="text-center text-primary"), width=12),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(html.P(
                text_rq5,
                className="text-center lead"), width=12),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id=rq5_plot_id, figure=fig_rq5), width=12),
            className="mb-5"
        ),
       ### Dropdown to choose parameter
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="rq5-parameter-dropdown",
                    options=[{"label": param, "value": param} for param in rq5_params],
                    value=rq5_default_param,
                    clearable=False,
                ),
                width=6
          ),
        
          className="mb-3",
          justify="center",
        
        ),

        # Output graph that updates 

        dbc.Row(
            dbc.Col(
                dcc.Graph(id="rq5-distribution-graph"), width=12),
            className="mb-5"
        ),


        ####



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



####Q5 Callback 
from dash import Input, Output 

@app.callback(
    Output("rq5-distribution-graph", "figure"),
    Input("rq5-parameter-dropdown", "value"),
)
def update_rq5_distribution(selected_param):
    # Create the boxplot dynamically based on dropdown selection
    fig = px.box(
        df_rq2,
        x="Potability",
        y=selected_param,
        points="all",
        title=f"Distribution of {selected_param} by Potability",
        labels={
            "Potability": "Potability (0 = Not Potable, 1 = Potable)",
            selected_param: selected_param,
        },
    )
    fig.update_layout(template="plotly_white")
    return fig



if __name__ == "__main__":
    app.run(debug=True)

###
### To see the results of your work, run this file (main.py)
### Then open your web browser and go to the website:
### Dash is running on http://127.0.0.1:8050/
###

### All the best of success with your final project!!!