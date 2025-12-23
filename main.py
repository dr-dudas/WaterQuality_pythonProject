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
from dash import dash_table
import dash_bootstrap_components as dbc

### Your modules
import analysis.data_modelling as dm # loading in your data_modeling.py
import analysis.analysisMissingValues as vis_rq1 # loading in analysisMissingValues - individual analysis module
import analysis.analysisPotability as vis_rq2 # loading in analysisPotability - individual analysis module
import analysis.analysisDifferences as vis_rq3 # loading in analysisDifference - individual analysis module
import analysis.analysisPotabilityValidation as vis_rq4 # loading in your individual analysis module
import analysis.analysisInfluence as vis_rq5 # loading in your individual analysis module


# load in the dataset
df_bc = dm.basic_cleaning("data/water_potability.csv")
df = dm.read_clean_general("data/water_potability.csv")

# Visualization calls and texts for each research question
### RQ1
title_rq1 = "RQ1: How do missing values and data quality issues affect the reliability of potability predictions?"
text_rq1_1 = text_rq1_1 = (
    "This analysis explores the frequency of missing values and explore those parameters "
    "and frequenzy compared to the potability of water.\n"
    "Let's start by checking for missing values in each column:\n"
)
mv_df = dm.missing_values_summary(df_bc).reset_index()
mv_df.columns = ["Feature", "Missing values"]

fig_rq1_1 = vis_rq1.missing_values_heatmap(df_bc)
rq1_plot1_1_id = "Missing values heatmap"
###
text_rq1_2 = "It's clear from the heatmap that missing values of 'ph', 'Sulfate', and 'Trihalomethanes' are scattered throughout the dataset. \nLet's analyze the distribution of these columns with missing values and see how they relate to the target variable 'Potability'."
target = 'Potability'
col_missing_values = ['ph', 'Sulfate', 'Trihalomethanes']
new_col = 'missing_value'
ph = "ph"
sulfate = "Sulfate"
trih = "Trihalomethanes"
fig_rq1_2 = vis_rq1.compare_distributions(df_bc, col_missing_values, target)
rq1_plot1_2_id = "Distributions of columns with missing values vs potability"

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
fig_rq1_3 = vis_rq1.plot_percentages(vis_rq1.compute_percentages(df_bc, new_col, target))
rq1_plot1_3_id = "Percentage of Potability vs Missing Values"
###
text_rq1_4 = (
    "The stacked bar chart shows the percentage of potable and non-potable water samples for each "
    "count of missing values.\n "
    "We can see that as the number of missing values increases, the average potability tends to decrease, but the trend is not very strong.\n"
    "First when we have 3 missing values do we see a significant drop in potability - but the amount of data on those are low. "
    "We conclude that the missing values of ph, Sulfate, and Trihalomethanes have very limited correlation with the potability of water samples."
)


title_rq2 = "RQ2: How can we correlate the Potability of water with the rest of the parameters?"
text_rq2 = (
    "The purpose of this research question is to find if there is any correlation" \
    "between the potability of the water and the rest of the parameters measured. \n" \
    "\n For starters, we've created a correlation heatmap function, shown below"
)
fig_rq2_0 = dm.correlation_heatmap(df)

text_rq2_2 = "Given our correlation heatmap, we can see that hardly any other parameter" \
            "correlate with Potability but just to be sure, we'll select the parameters with the highest" \
            "correlation values to see whether or not this is true. \n" \
            "Those parameters are - Solids and Chloramines - and we'll show the relationship with Potability through \n" \
            "box plots, density plots and lastly, a logistics regression." 
fig_rq2_1 = vis_rq2.boxplot_chloramines(df)  # YOUR CODE
rq2_plot1_id = "Chloramines vs Potability boxplot"
fig_rq2_2 = vis_rq2.boxplot_solids(df)
rq2_plot2_id = "Solids vs Potability boxplot"

text_rq2_3 = "The box plot for Chloramines and Potability shows overlapping indicating no clear " \
            "distiction between potable and non-potable water based on Chloramines. Same can be said about " \
            "Solids and Potability box plot although non-potable water has a slightly wider spread and a " \
            "few outliers, but the medians are close. This means there's no strong relationship between Potability, " \
            "Solids and Chloramines"

text_rq2_4 = "Density plots"
fig_rq2_3 = vis_rq2.densityplot_chloramines(df)
rq2_plot3_id = "Chloramines vs Potability density plot"
fig_rq2_4 = vis_rq2.densityplot_solids(df)
rq2_plot4_id = "Solids vs Potability density plot"

text_rq2_5 = "Logistics regression"
fig_rq2_5 = vis_rq2.logRegression(df)[0]
rq2_plot5_id = "Confusion matrix"
text_rq2_6 = "Accuracy value obtained from the logistics regression calculation: " \
            f"{vis_rq2.logRegression(df)[1]} \n" \
            "Using the box plots, we argued that there was no strong relationship between Potability, Solids, " \
            "and Chloramines, and now regarding the density plots we can see that the density curves both for Solids " \
            "and Chloramines in potable and non-potable water are nearly identical, which suggests they alone do " \
            "not provide a meaningful distinction between potable and non-potable water. " \
            "Leaving us a logistics regression where we obtained a confusion matrix and an accuracy value. " \
            "The confusion matrix shows that the model fails to predict any samples as non-potable, " \
            "once again reinforcing the idea that Solids and Chloramines don't provide enough information" \
            "to differentiate between both. And given the accuracy value of 63%, we can suggest that the dataset is " \
            "imbalanced and the model fails to predict non-potable samples." \
            

text_rq2_7 = "In conclusion, we can argue that Potabibility has no correlation whatsoever with the rest of the parameters."

###Q3
title_rq3 = "RQ3: Are there clear differences in pH, hardness, or solids between potable and non-potable water samples?"

cols_rq3 = ["ph", "Hardness", "Solids"]
target_rq3 = "Potability"

# --- RQ3.1: Summary table (grouped descriptive statistics)
summary_tbl_rq3 = vis_rq3.rq_summary(df, cols_rq3, target=target_rq3)
summary_flat_rq3 = (
    summary_tbl_rq3
    .stack(future_stack=True)
    .reset_index()
    .rename(columns={0: "Value"})
)

text_rq3_1 = (
    "We start by comparing grouped descriptive statistics (count, mean, std, min, quartiles, max) "
    "for pH, hardness, and solids between potable (1) and non-potable (0) water samples.\n\n"
    f"{summary_tbl_rq3}"
)

# --- RQ3.2: Box plot (all features together)
text_rq3_2 = (
    "Next, we use a box plot to compare the distributions of pH, hardness, and solids across the two classes. "
    "This helps us see median shifts, spread (IQR), and outliers between potable and non-potable samples."
)

fig_rq3_2 = vis_rq3.rq_box(df, cols_rq3, target=target_rq3)
rq3_plot3_2_id = "RQ3 Box plot: Feature distributions by potability"

# --- RQ3.3: Histograms (feature-by-feature)
text_rq3_3 = (
    "Finally, we inspect overlay histograms for each feature. "
    "These show how much the two classes overlap for each variable."
)

fig_rq3_3a = vis_rq3.rq_hist(df, "ph", target=target_rq3, bins=40)
rq3_plot3_3a_id = "RQ3 Histogram: pH by potability"

fig_rq3_3b = vis_rq3.rq_hist(df, "Hardness", target=target_rq3, bins=40)
rq3_plot3_3b_id = "RQ3 Histogram: Hardness by potability"

fig_rq3_3c = vis_rq3.rq_hist(df, "Solids", target=target_rq3, bins=40)
rq3_plot3_3c_id = "RQ3 Histogram: Solids by potability"

text_rq3_4 = "In conclusion, the differences between potable and non-potable water samples are subtle, with significant overlaps in distributions of pH, Hardness, and Solids."

####Q4

title_rq4 = (
    "RQ4: Does the potability label accurately indicate water safety, "
    "or are some samples with unsafe values marked as potable?"
)

text_rq4 = (
    "This analysis focuses on validating the potability label by examining whether "
    "water samples classified as potable (1) still exhibit unusually high values of "
    "Total Dissolved Solids (TDS) or Turbidity. "
    "High values in these parameters may indicate potential water safety concerns "
    "despite the potable classification."
)

# Call your analysis function
fig_rq4_1, fig_rq4_2, fig_rq4_3 = vis_rq4.run_analysis(df)
rq4_plot_id = "rq4-potability-validation"


####Q5
title_rq5 = "RQ5: Which water quality parameter has the strongest predictive influence on potability?"

text_rq5 = (
    "This research question investigates which water quality parameter has the "
    "strongest relationship with the potability label. We compute the correlation "
    "between each numeric parameter and Potability, and rank them by absolute "
    "correlation strength."
)

corr_rq5 = vis_rq5.compute_potability_correlations(df)
fig_rq5 = vis_rq5.plot_potability_correlation_bar(corr_rq5)

rq5_plot_id = "rq5-correlation-bar"
###
# Dropdown options = all numeric columns except Potability
rq5_params = [c for c in df.select_dtypes(include="number").columns if c != "Potability"]
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
        # Summary table
        dbc.Row(
            [
            dbc.Col(
                dash_table.DataTable(
                    data=mv_df.to_dict("records"),
                    columns=[{"name": c, "id": c} for c in mv_df.columns],
                    page_size=12,
                    style_table={"overflowX": "auto"},
                    style_cell={"fontSize": 13, "padding": "6px"},
                    style_header={"fontWeight": "bold"},
                ),
                width=5,
            ),
            dbc.Col(dcc.Graph(id=rq1_plot1_1_id, figure=fig_rq1_1), width=5, className="mx-auto"
            ),
            ],
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
            dbc.Col(dcc.Graph(id=rq1_plot1_3_id, figure=fig_rq1_3), width=6, className="mx-auto"),
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
            [
                dbc.Col(dbc.Col(dcc.Graph(id=rq2_plot1_id, figure=fig_rq2_1), width=12)),
                dbc.Col(dbc.Col(dcc.Graph(id=rq2_plot2_id, figure=fig_rq2_2), width=12)),
            ],
            className="mb-5"
        ),
        
         dbc.Row(
            dbc.Col(html.P(
                text_rq2_3,
                className="text-center lead"), width=12),
            className="mb-4"
        ),

        dbc.Row(
            [
                dbc.Col(dbc.Col(dcc.Graph(id=rq2_plot3_id, figure=fig_rq2_3), width=12)),
                dbc.Col(dbc.Col(dcc.Graph(id=rq2_plot4_id, figure=fig_rq2_4), width=12)),
            ],
            className="mb-5"
        ),

        dbc.Row(
            dbc.Col(html.P(
                text_rq2_5,
                className="text-center lead"), width=12),
            className="mb-4"
        ),

        dbc.Row(
            dbc.Col(dcc.Graph(id=rq2_plot5_id, figure=fig_rq2_5), width=12),
        ),
        dbc.Row(
            dbc.Col(html.P(text_rq2_6,className="text-center lead"), width=12),
        ), 

        dbc.Row(
            dbc.Col(html.P(text_rq2_7,className="text-center lead"), width=12),
        ),
        
        # Research Question 3
        dbc.Row(
            dbc.Col(html.H3(title_rq3, className="text-center text-primary"), width=12),
            className="mb-3"
        ),

        dbc.Row(
            dbc.Col(html.P(text_rq3_1, className="text-center lead"), width=12),
            className="mb-4"
        ),

        # Summary table
        dbc.Row(
            dbc.Col(
                dash_table.DataTable(
                    data=summary_flat_rq3.to_dict("records"),
                    columns=[{"name": c, "id": c} for c in summary_flat_rq3.columns],
                    page_size=10,
                    style_table={"overflowX": "auto"},
                    style_cell={"fontSize": 13, "padding": "6px"},
                    style_header={"fontWeight": "bold"},
                ),
                width=12
            ),
            className="mb-5"
        ),

        dbc.Row(
            dbc.Col(html.P(text_rq3_2, className="text-center lead"), width=12),
            className="mb-4"
        ),

        dbc.Row(
            dbc.Col(dcc.Graph(id=rq3_plot3_2_id, figure=fig_rq3_2), width=12),
            className="mb-5"
        ),

        dbc.Row(
            dbc.Col(html.P(text_rq3_3, className="text-center lead"), width=12),
            className="mb-4"
        ),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(id=rq3_plot3_3a_id, figure=fig_rq3_3a), width=4),
                dbc.Col(dcc.Graph(id=rq3_plot3_3b_id, figure=fig_rq3_3b), width=4),
                dbc.Col(dcc.Graph(id=rq3_plot3_3c_id, figure=fig_rq3_3c), width=4),
            ],
            className="mb-5"
        ),

                dbc.Row(
            dbc.Col(html.P(text_rq3_4, className="text-center lead"), width=12),
            className="mb-4"
        ),

        # controls row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Feature"),
                        dcc.Dropdown(
                            id="rq3-feature-dropdown",
                            options=[{"label": c, "value": c} for c in cols_rq3],
                            value="ph",
                            clearable=False,
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.Label("Bins"),
                        dcc.Slider(
                            id="rq3-bins-slider",
                            min=10,
                            max=100,
                            step=5,
                            value=40,
                            tooltip={"placement": "bottom", "always_visible": True},
                            updatemode="mouseup",
                        ),
                    ],
                    width=8,
                ),
            ],
            className="mb-4"
        ),

        dbc.Row(
            dbc.Col(
                dcc.Graph(id="rq3-hist-graph", figure=vis_rq3.rq_hist(df, "ph", bins=40)),
                width=12
            ),
            className="mb-5"
        ),
        
        # Research Question 4

         dbc.Row(
            dbc.Col(html.H3(title_rq4, className="text-center text-primary"), width=12),
            className="mb-3"
        ),

        dbc.Row(
            dbc.Col(html.P(text_rq4, className="text-center lead"), width=12),
            className="mb-4"
        ),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="rq4-safe-unsafe", figure=fig_rq4_1), width=4),
                dbc.Col(dcc.Graph(id="rq4-tds", figure=fig_rq4_2), width=4),
                dbc.Col(dcc.Graph(id="rq4-turbidity", figure=fig_rq4_3), width=4),
            ],
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

# Q3 CALLBACK
from dash import Input, Output

@app.callback(
    Output("rq3-hist-graph", "figure"),
    Input("rq3-feature-dropdown", "value"),
    Input("rq3-bins-slider", "value"),
)
def update_rq3_histogram(selected_feature, bins):
    return vis_rq3.rq_hist(df, selected_feature, bins=bins)

####Q5 Callback 
from dash import Input, Output 

@app.callback(
    Output("rq5-distribution-graph", "figure"),
    Input("rq5-parameter-dropdown", "value"),
)
def update_rq5_distribution(selected_param):
    # Create the boxplot dynamically based on dropdown selection
    fig = px.box(
        df,
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
