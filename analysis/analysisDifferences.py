from analysis import data_modelling as dm
import pandas as pd
import plotly.express as px

# Grouped summary stats (count/mean/std/min/25/50/75/max) for each class
def rq_summary(df, cols, target="Potability"):
    '''
    Docstring for rq_summary

    :param df: Cleaned water dataset
    :type df: pd.DataFrame
    :param cols: List of feature columns to summarize
    :type cols: list
    :param target: Target column used for grouping
    :type target: str
    :return: Grouped descriptive statistics table
    :rtype: pd.DataFrame
    '''
    return df.groupby(target)[cols].describe()

# One box plot comparing distributions for multiple features by class
def rq_box(df, cols, target="Potability", labels=None):
    '''
    Docstring for rq_box

    :param df: Cleaned water dataset
    :type df: pd.DataFrame
    :param cols: List of feature columns to plot
    :type cols: list
    :param target: Target column indicating potability
    :type target: str
    :param labels: Mapping of target values to readable labels
    :type labels: dict or None
    :return: Box plot comparing feature distributions by potability
    :rtype: Any
    '''
    labels = labels or {0: "Non-potable", 1: "Potable"}

    long_df = (
        df[cols + [target]]
        .assign(**{target: df[target].map(labels)})
        .melt(target, var_name="Feature", value_name="Value")
    )

    return px.box(
        long_df,
        x="Feature",
        y="Value",
        color=target,
        points="outliers",
        title="Feature distributions by potability",
    )

# Overlay histogram for a single feature by class
def rq_hist(df, col, target="Potability", labels=None, bins=40):
    '''
    Docstring for rq_hist

    :param df: Cleaned water dataset
    :type df: pd.DataFrame
    :param col: Feature column to plot
    :type col: str
    :param target: Target column indicating potability
    :type target: str
    :param labels: Mapping of target values to readable labels
    :type labels: dict or None
    :param bins: Number of histogram bins
    :type bins: int
    :return: Overlay histogram comparing distributions by potability
    :rtype: Any
    '''
    labels = labels or {0: "Non-potable", 1: "Potable"}

    plot_df = (
        df[[col, target]]
        .assign(**{target: df[target].map(labels)})
    )

    return px.histogram(
        plot_df,
        x=col,
        color=target,
        barmode="overlay",
        nbins=bins,
        opacity=0.55,
        histnorm="probability density",
        title=f"{col} by potability",
    )

# Returns (summary_table, figures_dict) for the RQ
def rq_outputs(df, cols=None, target="Potability"):
    '''
    Docstring for rq_outputs

    :param df: Cleaned water dataset
    :type df: pd.DataFrame
    :param cols: List of feature columns to analyze
    :type cols: list or None
    :param target: Target column indicating potability
    :type target: str
    :return: Summary table and dictionary of figures
    :rtype: tuple
    '''
    cols = cols or ["ph", "Hardness", "Solids"]

    figs = {"box_all": rq_box(df, cols, target)}
    figs.update({f"hist_{c}": rq_hist(df, c, target) for c in cols})

    return rq_summary(df, cols, target), figs


# ----------------------------
# Run analysis
# ----------------------------

if __name__ == "__main__":
    cols = ["ph", "Hardness", "Solids"]

    # remove directory before delivering
    df = dm.read_clean_general("data/water_potability.csv")

    summary_tbl, figs = rq_outputs(df, cols)

    print(summary_tbl) # print grouped statistics
