import data_modelling as dm
import pandas as pd
import plotly.express as px


# Grouped summary stats (count/mean/std/min/25/50/75/max) for each class
def rq_summary(df, cols, target="Potability"):
    return df.groupby(target)[cols].describe()


# One box plot comparing distributions for multiple features by class
def rq_box(df, cols, target="Potability", labels=None):
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
    """Returns (summary_table, figures_dict) for the RQ."""
    cols = cols or ["ph", "Hardness", "Solids"]

    figs = {"box_all": rq_box(df, cols, target)}
    figs.update({f"hist_{c}": rq_hist(df, c, target) for c in cols})

    return rq_summary(df, cols, target), figs


# ----------------------------
# Run analysis
# ----------------------------

cols = ["ph", "Hardness", "Solids"]

# remove directory before delivering
df = dm.read_clean_general("data/water_potability.csv")

summary_tbl, figs = rq_outputs(df, cols)

print(summary_tbl)  # grouped descriptive stats table

figs["box_all"].show()
figs["hist_ph"].show()
figs["hist_Hardness"].show()
figs["hist_Solids"].show()

