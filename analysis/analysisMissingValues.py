##################################################
##################################################
######### Water Quality Data Analysis ############
##################################################
##################################################
########### Missing Values Analysis ##############
##################################################

### Imports
from analysis import data_modelling as dm
import pandas as pd
import plotly.express as px

##################################################

### RQ - How do missing values and data quality issues affect the reliability of potability predictions?


# Function to visualize missing data using a heatmap
def missing_values_heatmap(df: pd.DataFrame):
    """
    Heatmap showing missing values (binary: missing vs present)

    :param df: Dataframe
    :type df: pd.DataFrame
    :requires: plotly.express as px
    :return: Heatmap showing missing values as black lines in the dataframe
    """
    # Encode missing as 1, present as 0
    missing = df.isna().astype(int)

    fig = px.imshow(
        missing,
        labels=dict(
            x="Feature",
            y="Sample index",
            color="Missing value"
        ),
        color_continuous_scale=[
            [0, "white"],   # present
            [1, "black"]    # missing
        ]
    )

    # Remove numeric color scale
    fig.update_layout(
        title="Missing values heatmap - black indicates missing value",
        height=400,
        coloraxis_showscale=False
    )

    return fig

# Function to compare distributions of selected columns by target variable
# In the main.py we will call this function to see how 'ph', 'Sulfate', and 'Trihalomethanes' relate to 'Potability'.
def compare_distributions(df, cols, target):
    """
    Compare distributions of selected columns by target variable
    
    :param df: Dataframe
    :type df: pd.DataFrame
    :param cols: List of columns to compare
    :type cols: list
    :param target: Target variable for comparison
    :type target: str
    :return: returns a dictionary of figures (one per column)

    """
    # Dictionary to hold figures
    figures = {} 

    # Create histograms for each column
    for col in cols:
        fig = px.histogram(
            df,
            x=col,
            color=target,
            barmode="overlay",
            histnorm="probability density",
            opacity=0.6,
            title=f"Distribution of {col} by {target}"
        )
        # Store the figure in the dictionary
        figures[col] = fig 

    return figures


# Function to group values by specified column and target variable
# Used in compute_percentages function below 
def grouped_values(df: pd.DataFrame, col: str, target: str):
    """
    Groups the dataframe by the specified column and target variable, counting occurrences.
    
    Eg. for each value in 'col', counts how many times each value of 'target' occurs.
    Eg2. col = 'missing_value', target = 'Potability'    
    Used in compute_percentages function.

    param df: Dataframe
    type df: pd.DataFrame
    param target: Target variable for grouping
    type target: str
    param col: Column to group by
    type col: str
    returns: pd.DataFrame: Grouped dataframe with counts of target variable for each value in col.
    """
    grouped = df.groupby([col, target]).size().unstack(fill_value=0)
    
    return grouped


# Compute percentages for each missing value count group
def compute_percentages(df: pd.DataFrame, col: str, target: str) -> pd.DataFrame:
    """
    Takes the dataframe and creates a grouped dataframe counting potability for each missing value count,
    then computes the percentage of each target variable.

    param df: Dataframe
    type df: pd.DataFrame
    returns: pd.DataFrame: Dataframe with percentages of target variable for each group.
    """
    grouped = grouped_values(dm.add_missing_value_column(df), col, target)
    percent = grouped.div(grouped.sum(axis=1), axis=0)
    
    return percent


# Visualize the percentages using a stacked bar chart
def plot_percentages(percent: pd.DataFrame):
    """
    Plot stacked bar chart of potability percentages by missing-value count.

    Expects `percent` in the format returned by compute_percentages():
      - index: missing-value count (e.g., 0,1,2,3)
      - columns: potability classes (e.g., 0,1)
      - values: proportions (0-1) OR percentages (0-100)
    """
    # Reset index for plotting
    df_plot = percent.reset_index() 

    # Melt the dataframe for plotly
    df_long = df_plot.melt(
        id_vars=df_plot.columns[0],
        var_name="Potability",
        value_name="Proportion"
    )
    # Create the stacked bar chart
    fig = px.bar(
        df_long,
        x=df_plot.columns[0],
        y="Proportion",
        color="Potability",
        barmode="stack",
        title="Potability Proportion by number of missing values for each sample"
    )
    # Format y-axis as percentage
    fig.update_yaxes(
        tickformat=".0%",
        range=[0, 1]
    )
    # Update layout
    fig.update_layout(
        yaxis_title="Proportion",
        legend_title_text="Potability"
    )

    return fig
