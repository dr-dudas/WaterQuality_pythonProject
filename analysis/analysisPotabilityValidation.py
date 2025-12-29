import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from analysis import data_modelling as dm

# WHO-style reference thresholds (simplified)
TDS_LIMIT = 500    # mg/L
TURBIDITY_LIMIT = 5   # NTU


def run_analysis(df):
    """
    RQ4: To what extent do potable water samples exceed safety limits
    for key water quality parameters?
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
    # FIGURE 1: Safe vs Unsafe + %
    # -------------------------------
    safety_counts = potable_df["Unsafe"].value_counts().reset_index()
    safety_counts.columns = ["Unsafe", "Count"]

    safety_counts["Status"] = safety_counts["Unsafe"].map({
        True: "Exceeds safety limits",
        False: "Within safety limits"
    })

    total_potable = safety_counts["Count"].sum()
    safety_counts["Percentage"] = (
        safety_counts["Count"] / total_potable * 100
    ).round(2)

    fig1 = px.bar(
        safety_counts,
        x="Status",
        y="Count",
        text=safety_counts["Percentage"].astype(str) + "%",
        title="Extent of Safety Limit Exceedance in Potable Water Samples",
        labels={"Count": "Number of Samples"},
    )

    fig1.update_traces(textposition="outside")
    fig1.update_layout(template="plotly_white")

    # -------------------------------
    # FIGURE 2: TDS distribution
    # -------------------------------
    fig2 = px.box(
        df,
        x="Potability",
        y="Solids",
        title="TDS Distribution by Potability",
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

    # -------------------------------
    # FIGURE 4: Which parameter drives exceedance (%)
    # -------------------------------
    total_potable = len(potable_df)

    tds_exceed_pct = potable_df["Unsafe_TDS"].mean() * 100
    turb_exceed_pct = potable_df["Unsafe_Turbidity"].mean() * 100

    fig4 = go.Figure()

    fig4.add_bar(
        x=["TDS", "Turbidity"],
        y=[tds_exceed_pct, turb_exceed_pct],
        text=[f"{tds_exceed_pct:.1f}%", f"{turb_exceed_pct:.1f}%"],
        textposition="outside"
    )

    fig4.update_layout(
        title="Percentage of Potable Samples Exceeding Safety Limits by Parameter",
        xaxis_title="Water Quality Parameter",
        yaxis_title="Percentage of Samples (%)",
        yaxis=dict(range=[0, 100]),
        template="plotly_white"
    )

    # -------------------------------
    # RETURN
    # -------------------------------
    return fig1, fig2, fig3, fig4
