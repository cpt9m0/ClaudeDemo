# Financial Performance Dashboard

An interactive Streamlit dashboard for exploring the `Financial_Sample.xlsx` sales dataset: 700 transactions across 5 segments, 5 countries and 6 products, from September 2013 to December 2014.

## Features

- **Sidebar filters**: segment, country, product, discount band and date range
- **KPI row**: gross sales, net sales, profit, units sold, profit margin and average discount rate
- **Trend over time**: a line chart of any measure, with an optional split by dimension
- **Breakdown by category**: a bar chart of any measure by any dimension
- **Composition**: a treemap sized by a measure you choose
- **Profit margin by category**: a bar chart with losses and profits in different colors
- **Sales vs. profit**: a scatter plot with one point for each segment × country × product combination
- **Filtered transactions**: a data table of the filtered rows, with CSV download

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Getting started

```bash
# Install dependencies
uv sync

# Launch the dashboard
uv run streamlit run src/app.py
```

The dashboard opens at <http://localhost:8501>.

## Project structure

```
.
├── Financial_Sample.xlsx     # Source dataset
├── docs/
│   └── Financial_Sample.md   # Dataset schema and data-quality notes
├── src/
│   ├── app.py                # Streamlit app: filters, KPIs, charts, table
│   ├── data.py               # Data loading/cleaning, measure and dimension definitions
│   └── theme.py              # Color palette and Plotly template
├── .streamlit/config.toml    # Streamlit theme
└── pyproject.toml            # Project metadata and dependencies
```

## Data

The full schema is in [docs/Financial_Sample.md](docs/Financial_Sample.md). `src/data.py` cleans the raw file when it loads it:

- Strips whitespace from column names. In the raw file the `Sales` column is named `" Sales"`.
- Fills missing `Discount Band` values with `"None"`.
- Adds `Profit Margin` (`Profit / Sales`) and `Discount Rate` (`Discounts / Gross Sales`) columns.

Streamlit caches the loaded data with `st.cache_data`.

## Tech stack

[Streamlit](https://streamlit.io/) · [Plotly](https://plotly.com/python/) · [pandas](https://pandas.pydata.org/) · [openpyxl](https://openpyxl.readthedocs.io/)
