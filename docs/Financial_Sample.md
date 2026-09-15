# Financial_Sample.xlsx — Data Structure

Sample financial/sales dataset used as the data source for the dashboard. Single-sheet Excel workbook.

## Overview

| Property | Value |
|---|---|
| Sheet name | `Sheet1` |
| Rows | 700 |
| Columns | 16 |
| Date range | 2013-09-01 to 2014-12-01 |
| Years covered | 2013, 2014 |

## Columns

| Column | Type | Description | Notes |
|---|---|---|---|
| `Segment` | string | Customer segment | 5 values: Channel Partners, Enterprise, Government, Midmarket, Small Business |
| `Country` | string | Sales country | 5 values: Canada, France, Germany, Mexico, United States of America |
| `Product` | string | Product name | 6 values: Amarilla, Carretera, Montana, Paseo, VTT, Velo |
| `Discount Band` | string | Discount tier applied | 3 values: Low, Medium, High. **53 rows have no value (empty/NaN)** — no discount applied |
| `Units Sold` | float | Number of units sold | Range: 200 – 4,492.5 |
| `Manufacturing Price` | int | Per-unit manufacturing cost | Range: 3 – 260 |
| `Sale Price` | int | Per-unit sale price | Range: 7 – 350 |
| `Gross Sales` | float | `Units Sold × Sale Price` | Range: 1,799 – 1,207,500 |
| `Discounts` | float | Discount amount deducted from gross sales | Range: 0 – 149,677.5 |
| ` Sales` | float | Net sales (`Gross Sales − Discounts`) | Note: column name has a **leading space** in the source file |
| `COGS` | float | Cost of goods sold | Range: 918 – 950,625 |
| `Profit` | float | `Sales − COGS` | Range: **-40,617.5** – 262,200 (can be negative) |
| `Date` | datetime | Transaction month/date | All values fall on the 1st of the month |
| `Month Number` | int | Numeric month (1–12) | Redundant with `Date` |
| `Month Name` | string | Month name (e.g. "January") | Redundant with `Date` |
| `Year` | int | Transaction year | 2013 or 2014 |

## Data Quality Notes

- `Discount Band` has 53 missing values out of 700 rows (~7.6%); these appear to be transactions with zero discount.
- The `Sales` column name is stored with a leading space (`" Sales"`) in the raw file — strip whitespace from column names before use.
- `Profit` can be negative, indicating loss-making transactions.
- `Date`, `Month Number`, and `Month Name` are redundant/derived from each other.

## Categorical Values

- **Segment**: Channel Partners, Enterprise, Government, Midmarket, Small Business
- **Country**: Canada, France, Germany, Mexico, United States of America
- **Product**: Amarilla, Carretera, Montana, Paseo, VTT, Velo
- **Discount Band**: Low, Medium, High (or blank)

## Suggested Use

This is a natural fact table for the dashboard: filter by `Segment` / `Country` / `Product` / `Discount Band` / `Year` or `Month`, and chart `Units Sold`, `Gross Sales`, `Sales`, `COGS`, and `Profit` as measures.
