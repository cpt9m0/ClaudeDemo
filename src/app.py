"""Interactive dashboard for the Financial_Sample dataset."""

import pandas as pd
import plotly.express as px
import streamlit as st

from data import DIMENSIONS, MEASURES, load_data
from theme import (
    CATEGORICAL,
    DIVERGING_NEG,
    DIVERGING_POS,
    DIVERGING_SCALE,
    category_color_map,
    register_template,
)

st.set_page_config(page_title="Financial Performance Dashboard", layout="wide", page_icon="📊")
register_template()

df = load_data()

# ---------------------------------------------------------------- filters --
st.sidebar.header("Filters")


def multiselect_all(label: str, options: list[str], key: str) -> list[str]:
    return st.sidebar.multiselect(label, options, default=options, key=key)


segments = multiselect_all("Segment", sorted(df["Segment"].unique()), "f_segment")
countries = multiselect_all("Country", sorted(df["Country"].unique()), "f_country")
products = multiselect_all("Product", sorted(df["Product"].unique()), "f_product")
bands = multiselect_all("Discount Band", sorted(df["Discount Band"].unique()), "f_band")

min_date, max_date = df["Date"].min().to_pydatetime(), df["Date"].max().to_pydatetime()
date_range = st.sidebar.slider(
    "Date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="MMM YYYY",
)

mask = (
    df["Segment"].isin(segments)
    & df["Country"].isin(countries)
    & df["Product"].isin(products)
    & df["Discount Band"].isin(bands)
    & (df["Date"] >= date_range[0])
    & (df["Date"] <= date_range[1])
)
fdf = df[mask]

st.title("Financial Performance Dashboard")
st.caption("Sample sales data · Segment / Country / Product / Discount Band, 2013–2014")

if fdf.empty:
    st.warning("No transactions match the current filters. Adjust the filters in the sidebar.")
    st.stop()

st.caption(
    f"Showing {len(fdf):,} of {len(df):,} transactions · "
    f"{fdf['Date'].min():%b %Y} – {fdf['Date'].max():%b %Y}"
)

# ------------------------------------------------------------------- KPIs --
total_sales = fdf["Sales"].sum()
total_gross = fdf["Gross Sales"].sum()
total_profit = fdf["Profit"].sum()
total_units = fdf["Units Sold"].sum()
margin = total_profit / total_sales if total_sales else 0
discount_rate = fdf["Discounts"].sum() / total_gross if total_gross else 0

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Gross Sales", f"${total_gross:,.0f}")
k2.metric("Net Sales", f"${total_sales:,.0f}")
k3.metric("Profit", f"${total_profit:,.0f}")
k4.metric("Units Sold", f"{total_units:,.0f}")
k5.metric("Profit Margin", f"{margin:.1%}")
k6.metric("Avg Discount Rate", f"{discount_rate:.1%}")

st.divider()

# ----------------------------------------------------------------- trend --
st.subheader("Trend over time")
tc1, tc2 = st.columns(2)
trend_measure_label = tc1.selectbox("Measure", list(MEASURES.keys()), index=1, key="trend_measure")
trend_breakdown = tc2.selectbox("Break down by", ["None"] + DIMENSIONS, key="trend_breakdown")
trend_measure = MEASURES[trend_measure_label]

if trend_breakdown == "None":
    trend = fdf.groupby(pd.Grouper(key="Date", freq="MS"))[trend_measure].sum().reset_index()
    fig_trend = px.line(trend, x="Date", y=trend_measure, markers=True)
    fig_trend.update_traces(line_color=CATEGORICAL[0], marker_color=CATEGORICAL[0])
else:
    trend = (
        fdf.groupby([pd.Grouper(key="Date", freq="MS"), trend_breakdown])[trend_measure]
        .sum()
        .reset_index()
    )
    cmap = category_color_map(fdf[trend_breakdown].unique().tolist())
    fig_trend = px.line(
        trend, x="Date", y=trend_measure, color=trend_breakdown,
        color_discrete_map=cmap, markers=True,
    )

fig_trend.update_layout(hovermode="x unified", yaxis_title=trend_measure_label, xaxis_title=None)
st.plotly_chart(fig_trend, use_container_width=True, theme=None)

st.divider()

# ------------------------------------------------------------- breakdown --
bc1, bc2 = st.columns(2)
with bc1:
    st.subheader("Breakdown by category")
    b1, b2 = st.columns(2)
    bd_measure_label = b1.selectbox("Measure", list(MEASURES.keys()), index=1, key="bd_measure")
    bd_dimension = b2.selectbox("Dimension", DIMENSIONS, index=0, key="bd_dimension")
    bd_measure = MEASURES[bd_measure_label]

    agg = fdf.groupby(bd_dimension)[bd_measure].sum().reset_index().sort_values(bd_measure)
    cmap = category_color_map(agg[bd_dimension].tolist())
    fig_bar = px.bar(
        agg, x=bd_measure, y=bd_dimension, orientation="h",
        color=bd_dimension, color_discrete_map=cmap,
    )
    fig_bar.update_layout(showlegend=False, yaxis_title=None, xaxis_title=bd_measure_label)
    st.plotly_chart(fig_bar, use_container_width=True, theme=None)

with bc2:
    st.subheader("Composition")
    tree_measure_label = st.selectbox("Size by", list(MEASURES.keys()), index=1, key="tree_measure")
    tree_measure = MEASURES[tree_measure_label]

    tree = fdf.groupby(["Segment", "Product"])[tree_measure].sum().reset_index()
    tree = tree[tree[tree_measure] > 0]
    if tree.empty:
        st.info(f"No positive {tree_measure_label} values to display as a treemap.")
    else:
        cmap = category_color_map(tree["Segment"].unique().tolist())
        fig_tree = px.treemap(
            tree, path=["Segment", "Product"], values=tree_measure,
            color="Segment", color_discrete_map=cmap,
        )
        fig_tree.update_traces(marker=dict(line=dict(color="#fcfcfb", width=2)))
        fig_tree.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_tree, use_container_width=True, theme=None)

st.divider()

# --------------------------------------------------------- profit margin --
pmc1, pmc2 = st.columns(2)
with pmc1:
    st.subheader("Profit margin by category")
    pm_dimension = st.selectbox("Dimension", DIMENSIONS, index=0, key="pm_dimension")

    pm = (
        fdf.groupby(pm_dimension)
        .apply(lambda g: g["Profit"].sum() / g["Sales"].sum() if g["Sales"].sum() else 0, include_groups=False)
        .reset_index(name="Profit Margin")
        .sort_values("Profit Margin")
    )
    bar_colors = [DIVERGING_NEG if v < 0 else DIVERGING_POS for v in pm["Profit Margin"]]
    fig_pm = px.bar(pm, x="Profit Margin", y=pm_dimension, orientation="h")
    fig_pm.update_traces(marker_color=bar_colors)
    fig_pm.update_layout(yaxis_title=None, xaxis_tickformat=".0%")
    fig_pm.add_vline(x=0, line_color="#c3c2b7", line_width=1)
    st.plotly_chart(fig_pm, use_container_width=True, theme=None)

with pmc2:
    st.subheader("Sales vs. profit")
    scatter = fdf.groupby(["Segment", "Country", "Product"]).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"), Units=("Units Sold", "sum"),
    ).reset_index()
    scatter["Profit Margin"] = scatter["Profit"] / scatter["Sales"]
    bound = max(abs(scatter["Profit Margin"].min()), abs(scatter["Profit Margin"].max()), 0.01)
    fig_scatter = px.scatter(
        scatter, x="Sales", y="Profit", size="Units", color="Profit Margin",
        color_continuous_scale=[c for _, c in DIVERGING_SCALE],
        range_color=(-bound, bound),
        hover_data=["Segment", "Country", "Product"],
    )
    fig_scatter.update_layout(coloraxis_colorbar=dict(title="Margin", tickformat=".0%"))
    fig_scatter.add_hline(y=0, line_color="#c3c2b7", line_width=1)
    st.plotly_chart(fig_scatter, use_container_width=True, theme=None)

st.divider()

# -------------------------------------------------------------- data table --
st.subheader("Filtered transactions")
display_cols = [
    "Date", "Segment", "Country", "Product", "Discount Band",
    "Units Sold", "Gross Sales", "Discounts", "Sales", "COGS", "Profit", "Profit Margin",
]
st.dataframe(fdf[display_cols].sort_values("Date"), use_container_width=True, hide_index=True)

csv = fdf[display_cols].to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data as CSV", csv, "financial_data_filtered.csv", "text/csv")
