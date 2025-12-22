
"""
Research Question (Sanjana):
Does the potability label accurately indicate water safety, or are some
samples with unsafe values, such as high total dissolved solids (TDS)
or high turbidity, marked as potable?
"""

import pandas as pd
import plotly.express as px
from analysis import data_modelling as dm

# WHO-style reference thresholds (simplified for project)
TDS_LIMIT = 500        # mg/L
TURBIDITY_LIMIT = 5   # NTU


def run_analysis(df):
    """
    RQ4: Check whether potable water samples contain unsafe values
    """

    # -------------------------------
    # Step 1: Filter potable samples
    # -------------------------------
    potable_df = df[df["Potability"] == 1].copy()

    # -------------------------------
    # Step 2: Mark unsafe conditions
    # -------------------------------
    potable_df["Unsafe_TDS"] = potable_df["Solids"] > TDS_LIMIT
    potable_df["Unsafe_Turbidity"] = potable_df["Turbidity"] > TURBIDITY_LIMIT

    potable_df["Unsafe"] = potable_df["Unsafe_TDS"] | potable_df["Unsafe_Turbidity"]

    # -------------------------------
    # FIGURE 1: Safe vs Unsafe (bar)
    # -------------------------------
    safety_counts = potable_df["Unsafe"].value_counts().reset_index()
    safety_counts.columns = ["Unsafe", "Count"]
    safety_counts["Unsafe"] = safety_counts["Unsafe"].map(
        {True: "Unsafe", False: "Safe"}
    )

    fig1 = px.bar(
        safety_counts,
        x="Unsafe",
        y="Count",
        title="Potable Water Samples: Safe vs Unsafe",
        labels={"Count": "Number of Samples"},
        text="Count",
    )
    fig1.update_layout(template="plotly_white")

    # -------------------------------
    # FIGURE 2: TDS distribution
    # -------------------------------
    fig2 = px.box(
        df,
        x="Potability",
        y="Solids",
        title="TDS (Solids) Distribution by Potability",
        labels={
            "Potability": "Potability (0 = Not Potable, 1 = Potable)",
            "Solids": "Total Dissolved Solids (mg/L)",
        },
    )
    fig2.add_hline(
        y=TDS_LIMIT,
        line_dash="dash",
        annotation_text="TDS Safety Limit",
        annotation_position="top left",
    )
    fig2.update_layout(template="plotly_white")

    # -------------------------------
    # FIGURE 3: Turbidity distribution
    # -------------------------------
    fig3 = px.box(
        df,
        x="Potability",
        y="Turbidity",
        title="Turbidity Distribution by Potability",
        labels={
            "Potability": "Potability (0 = Not Potable, 1 = Potable)",
            "Turbidity": "Turbidity (NTU)",
        },
    )
    fig3.add_hline(
        y=TURBIDITY_LIMIT,
        line_dash="dash",
        annotation_text="Turbidity Safety Limit",
        annotation_position="top left",
    )
    fig3.update_layout(template="plotly_white")

    return fig1, fig2, fig3
