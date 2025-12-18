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
#import analysis.analysis_rq5 as vis_rq5 # loading in your individual analysis module


# load in the dataset
# in our example, we use the Netflix dataset
df = pd.read_csv("data/water_potability.csv")
df_rq2 = dm.read_clean_general("data/water_potability.csv")

# call visualizations
# This is your individual work, each one of you will have different figures
# REPLACE BY YOUR OWN FIGURES AND TEXTS
title_rq1 = "RQ1: How do missing values and data quality issues affect the reliability of potability predictions?"
text_rq1_1 = (
    "This analysis investigates how missing values and data quality issues may influence the "
    "reliability of water potability predictions.\n"
    "As a first step, we examine the frequency and distribution of missing values across all "
    "features in the dataset.\n"
    "This provides an overview of which variables are affected by missing data and how extensive "
    "the data quality issues are.\n\n"
    f"{dm.missing_values_summary(df)}"
)
fig_rq1_1 = vis_rq1.missing_values_heatmap(df)
rq1_plot1_1_id = "Missing values heatmap"
###
text_rq1_2 = (
    "From the heatmap, it is clear that missing values in 'ph', 'Sulfate', and 'Trihalomethanes' "
    "are scattered throughout the dataset.\n"
    "Next, we analyze the distributions of these variables and examine how they relate to the target variable 'Potability'."
)
text_rq1_2 = (
    "The heatmap visualization shows that missing values only occur in the variables "
    "'ph', 'Sulfate', and 'Trihalomethanes'.\n"
    "These missing values are distributed throughout the dataset rather than being concentrated "
    "in specific rows or segments.\n"
    "This suggests that missingness is not caused by a single systematic issue but is instead "
    "spread across multiple samples.\n"
    "To assess whether this missing data may be related to water potability, we next examine the "
    "distributions of these variables in relation to the target variable 'Potability'."
)
target = 'Potability'
col_missing_values = ['ph', 'Sulfate', 'Trihalomethanes']
new_col = 'missing_value'
fig_rq1_2 = vis_rq1.compare_distributions(df, col_missing_values, target)
rq1_plot1_2_id = "Distributions of columns with missing values vs Potability"
###
text_rq1_3 = (
    "The distribution plots show that values of 'ph', 'Sulfate', and 'Trihalomethanes' span similar "
    "ranges for both potable and non-potable water samples.\n"
    "No strong separation between the two potability classes is visible based solely on the "
    "observed values of these variables.\n"
    "This indicates that missing values in these features do not appear to be strongly associated "
    "with either class of water potability.\n\n"
    "To further quantify this observation, we analyze whether the presence of missing values "
    "themselves is related to potability.\n"
    "Specifically, we examine whether having one or more missing values in a single sample "
    "correlates with the probability of the water being potable.\n"
    "This is visualized by computing and plotting the percentage of potable samples for each count "
    "of missing values."
)
fig_rq1_3 = vis_rq1.plot_percentages(vis_rq1.compute_percentages(df, new_col, target))
rq1_plot1_3_id = "Percentage of Potability vs Missing Values"
###
text_rq1_4 = (
    "The stacked bar chart displays the percentage of potable and non-potable water samples for "
    "each observed count of missing values.\n"
    "Across samples with one or two missing values, the proportion of potable water remains "
    "relatively stable, indicating only a weak association between missingness and potability.\n"
    "A more noticeable decrease in potability is observed for samples with three missing values; "
    "however, this group contains relatively few observations, which limits the reliability of "
    "this result.\n\n"
    "Overall, the analysis suggests that missing values in 'ph', 'Sulfate', and 'Trihalomethanes' "
    "have a limited impact on water potability.\n"
    "In the context of RQ1, this indicates that data quality issues related to missing values alone "
    "are unlikely to significantly affect the reliability of potability predictions, and that "
    "other factors are likely more influential."
)

#########################################################################################################
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
                    dcc.Graph(id="q1_plot_ph", figure=fig_rq1_2["ph"]),
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
