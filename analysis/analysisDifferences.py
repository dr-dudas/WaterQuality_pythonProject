from analysis import data_modelling as dm
import pandas as pd
import plotly.express as px

def rq_summary(df, cols, target="Potability"):
    """Grouped summary stats (count/mean/std/min/25/50/75/max) for each class."""
    return df.groupby(target)[cols].describe()

def rq_differences(df, cols, target="Potability", a=1, b=0):
    """Feature-by-feature difference between class a and class b (sorted by magnitude)."""
    def d(col):
        x = pd.to_numeric(df.loc[df[target] == a, col], errors="coerce").dropna()
        y = pd.to_numeric(df.loc[df[target] == b, col], errors="coerce").dropna()
        p = (((x.var(ddof=1)*(len(x)-1) + y.var(ddof=1)*(len(y)-1)) / (len(x)+len(y)-2)) ** 0.5) if (len(x) > 1 and len(y) > 1) else None
        return 0.0 if p in (0, None) else (x.mean() - y.mean()) / p
    return pd.Series({c: d(c) for c in cols}).sort_values(key=lambda s: s.abs(), ascending=False)

def rq_box(df, cols, target="Potability", labels=None):
    """One box plot comparing distributions for multiple features by class."""
    labels = labels or {0: "Non-potable", 1: "Potable"}
    long_df = df[cols + [target]].assign(**{target: df[target].map(labels)}).melt(target, var_name="Feature", value_name="Value")
    return px.box(long_df, x="Feature", y="Value", color=target, points="outliers", title="Feature distributions by potability")

def rq_hist(df, col, target="Potability", labels=None, bins=40):
    """Overlay histogram for a single feature by class."""
    labels = labels or {0: "Non-potable", 1: "Potable"}
    plot_df = df[[col, target]].assign(**{target: df[target].map(labels)})
    return px.histogram(plot_df, x=col, color=target, barmode="overlay", nbins=bins, opacity=0.55,
                        histnorm="probability density", title=col + " by potability")

def rq_outputs(df, cols=None, target="Potability"):
    """Returns (summary_table, effect_sizes, figures_dict) for the RQ."""
    cols = cols or ["ph", "Hardness", "Solids"]
    figs = {"box_all": rq_box(df, cols, target)}
    figs.update({"hist_" + c: rq_hist(df, c, target) for c in cols})
    return rq_summary(df, cols, target), rq_cohen_d(df, cols, target), figs

cols = ["ph", "Hardness", "Solids"]

summary_tbl, effect_sizes, figs = rq_outputs(df, cols)

print(summary_tbl)      # prints the grouped descriptive stats table
print(effect_sizes)     # prints differences for each column

figs["box_all"].show()
figs["hist_ph"].show()
figs["hist_Hardness"].show()
figs["hist_Solids"].show()
