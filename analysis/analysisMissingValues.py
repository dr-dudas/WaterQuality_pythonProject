##################################################
########### Missing Values Analysis ##############
##################################################

### Imports
from analysis import data_modelling as dm
import pandas as pd
import plotly.express as px

### RQ - How do missing values and data quality issues affect the reliability of potability predictions?


# Function to visualize missing data using a heatmap
def missing_values_heatmap(df: pd.DataFrame):
    """
    Heatmap showing missing values (binary: missing vs present)

    Missing values are encoded as black lines in the dataframe.
    
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

    # Remove the continuous color scale
    fig.update_layout(
        title="Missing values heatmap - black indicates missing value",
        height=400,
        coloraxis_showscale=False
    )

    return fig

# Function to compare distributions of selected columns by target variable
# In the main.py we will call this function to see how 'ph', 'Sulfate', and 'Trihalomethanes' relate to 'Potability'.
def compare_distributions(df: pd.DataFrame, cols: list[str], target: str) -> dict:
    """
    Compare distributions of selected features by target variable
    
    Produces a dict of figures.
    Each figure is a histogram.

    :param df: Dataframe
    :type df: pd.DataFrame
    :param cols: List of columns to compare
    :type cols: list[str]
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
def grouped_values(df: pd.DataFrame, col: str, target: str) -> pd.DataFrame:
    """
    Groups the dataframe by the specified column and target variable, counting occurrences.
    
    Example
    -------
    If col="missing_value" and target="Potability", the output counts how many
    Potability=0 and Potability=1 rows exist for each missing_value count.
    
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
    Compute potability proportions for each missing-value count group.

    This function:
      1) adds the missing-value count column using dm.add_missing_value_column(df)
      2) groups by (missing count, target) using grouped_values(df, col, target)
      3) converts counts to row-wise proportions (0–1)

    param df: Dataframe
    type df: pd.DataFrame
    returns: pd.DataFrame: Dataframe with percentages of target variable for each group.
    """
    # Get grouped counts
    grouped = grouped_values(dm.add_missing_value_column(df), col, target)
    # Convert counts to proportions per missing-value count
    percent = grouped.div(grouped.sum(axis=1), axis=0)
    
    return percent


# Visualize the percentages using a stacked bar chart
def plot_percentages(percent: pd.DataFrame):
    """
    Plot stacked bar chart of Potability percentages by missing-value count.

    Expects 'percent' in the format returned by compute_percentages():
      - index: missing-value count (e.g., 0, 1, 2, 3)
      - columns: target classes (e.g., 0 and 1)
      - values: proportions [0-1]
    """
    # Reset index so the missing-value count becomes a plotting column
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
