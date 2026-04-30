# Customer Cohort Retention Analysis

## Project Overview

This project performs a **customer cohort retention analysis** on the Northwind database to understand how customer retention changes over time. The analysis identifies when customers make their first purchase, groups them into monthly cohorts, and tracks their purchasing behavior over the following months.

## Key Questions Answered

- How many new customers are acquired each month?
- What percentage of customers return to make additional purchases?
- Which customer cohorts show the strongest retention?
- How does retention change over the first 6 months after the first purchase?

## Folder Structure

02_cohort_retention/
│
├── CohortAnalysis.ipynb # Main Jupyter notebook with full analysis
├── CohortAnalysis.pdf # Exported PDF version of the report
├── CohortAnalysis.tex # LaTeX source file for the report
│
├── cohort_analysis.sql # SQL query for cohort retention calculation
├── cohort_heatmap.png # Generated heatmap visualization
│
├── CohortAnalysis_files/ # Supporting files for the notebook
│ └── cell-6-output-1.png # Embedded visualization output
│
└── README.md 

## Files Description

| File | Description |
|------|-------------|
| `CohortAnalysis.ipynb` | Main Jupyter notebook containing code, SQL, visualizations, and explanatory text |
| `CohortAnalysis.pdf` | Rendered report suitable for sharing with stakeholders |
| `CohortAnalysis.tex` | LaTeX source for typesetting the report |
| `cohort_analysis.sql` | SQL query (CTE-based) that computes cohort retention rates |
| `cohort_heatmap.png` | Heatmap visualization of retention rates by cohort |
| `CohortAnalysis_files/` | Directory containing notebook output assets |

## Methodology

The analysis uses a **cohort retention approach**:

1. **Step 1:** Identify each customer's first purchase month (cohort month)
2. **Step 2:** Track all subsequent purchases and calculate months elapsed
3. **Step 3:** For each cohort, compute retention rate for months 0 through 6
4. **Step 4:** Visualize results as a heatmap and export as PDF

## Requirements

To run this analysis, you need:

- Python 3.x with the following packages:
  - pandas
  - seaborn
  - matplotlib
  - pyodbc
- Access to a SQL Server instance with the Northwind database
- ODBC Driver 17 for SQL Server

## How to Run

1. Ensure your Northwind database is accessible via the connection string in the notebook
2. Open `CohortAnalysis.ipynb` in Jupyter Notebook or JupyterLab
3. Run all cells sequentially
4. The heatmap will be saved as `cohort_heatmap.png`

## Key Insight

The analysis reveals a sharp drop in retention after Month 1 (often falling to 20-40%), followed by gradual stabilization around months 5-6. Cohorts vary in their retention patterns, suggesting opportunities to investigate what drives stronger retention in certain months.



## Part of the SQL Analytics Portfolio

[![SQL Portfolio](https://img.shields.io/badge/SQL-Analytics%20Portfolio-1F4E79?style=flat)](https://github.com/ChristianLG2/SQL-Analytics-Portfolio)
[![Christian Lira](https://img.shields.io/badge/Built%20by-Christian%20Lira-2E74B5?style=flat)](https://clirago.com)
