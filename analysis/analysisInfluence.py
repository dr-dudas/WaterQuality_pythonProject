"""

Research Question (5):
    Which water quality parameter has the strongest predictive influence on
    determining whether a water sample is potable?

"""


import pandas as pd
import plotly.express as px


# 1. COMPUTE CORRELATIONS WITH POTABILITY
# -----------------------------------------------------------------------------

def compute_potability_correlations(df: pd.DataFrame) -> pd.Series:
    """
    Compute correlation of each numeric feature with Potability.

    Returns:
        Series sorted by absolute correlation strength.
    """
    corr_matrix = df.corr(numeric_only=True)
    pot_corr = corr_matrix["Potability"].drop(labels=["Potability"])

    pot_corr_sorted = pot_corr.reindex(
        pot_corr.abs().sort_values(ascending=False).index
    )

    return pot_corr_sorted


# 2. INTERACTIVE BAR CHART (Plotly)
# -----------------------------------------------------------------------------

def plot_potability_correlation_bar(corr_series: pd.Series):
    """
    Return an interactive Plotly bar chart of correlations.
    """
    df_plot = corr_series.reset_index()
    df_plot.columns = ["parameter", "correlation"]

    df_plot["direction"] = df_plot["correlation"].apply(
        lambda x: "Positive" if x >= 0 else "Negative"
    )

    fig = px.bar(
        df_plot,
        x="correlation",
        y="parameter",
        orientation="h",
        color="direction",
        title="Correlation of Water Quality Parameters with Potability",
        labels={
            "correlation": "Correlation with Potability",
            "parameter": "Water Quality Parameter",
            "direction": "Correlation Direction",
        },
    )

    fig.update_layout(
        yaxis=dict(categoryorder="array", categoryarray=df_plot["parameter"]),
        template="plotly_white",
    )

    return fig



# 3. INTERACTIVE BOXPLOT FOR STRONGEST PARAMETER
def plot_strongest_parameter_boxplot(df: pd.DataFrame, corr_series: pd.Series):
    """
    Create an interactive Plotly boxplot for the strongest correlated parameter,
    comparing Potability=0 vs Potability=1.

    Args:
        df: Cleaned DataFrame containing 'Potability' and the feature columns.
        corr_series: Correlations with Potability sorted by absolute strength.

    Returns:
        A Plotly Figure (interactive).
    """
    strongest_param = corr_series.index[0]

    fig = px.box(
        df,
        x="Potability",
        y=strongest_param,
        points="all",  # shows sample points (interactive)
        title=f"Distribution of {strongest_param} by Potability",
        labels={
            "Potability": "Potability (0 = Not Potable, 1 = Potable)",
            strongest_param: strongest_param,
        },
    )

    fig.update_layout(template="plotly_white")
    return fig
