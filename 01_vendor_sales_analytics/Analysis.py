#%%
#Load libraries
import os
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.patches import Patch

# Establish Database Connection
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=Northwind;"
    "Trusted_Connection=yes;"
)

print("Connection Succesful")

#%%
# Import supplier_ranking query from SQL files in dir
base_dir = os.path.dirname(os.path.abspath(__file__))
sql_path = os.path.join(base_dir, "01_supplier_ranking.sql")

with open(sql_path, "r") as file:
    supplier_ranking = file.read()

supplier_ranking = pd.read_sql(supplier_ranking, conn)
conn.close()

#%%
#EDA
print(supplier_ranking.head(10))
print(f"\nShape: {supplier_ranking.shape}")
print(f"Categories: {supplier_ranking["CategoryName"].unique()}")

print(supplier_ranking.columns.tolist())
# %%
import os
os.makedirs("outputs", exist_ok=True)

#%%

fig, ax = plt.subplots(figsize=(12, 7))

# Take top 15 by revenue rank
top15 = supplier_ranking.head(15).sort_values("total_order_revenue", ascending=True)

# Color bars by category
categories = top15["CategoryName"].unique()
color_map = {
    "Beverages":      "#2196F3",
    "Dairy Products": "#4CAF50",
    "Meat/Poultry":   "#F44336",
    "Grains/Cereals": "#FF9800",
    "Confections":    "#9C27B0",
    "Produce":        "#00BCD4",
    "Condiments":     "#795548",
    "Seafood":        "#607D8B",
}
colors = top15["CategoryName"].map(color_map)

bars = ax.barh(
    top15["SupplierName"],
    top15["total_order_revenue"],
    color=colors,
    edgecolor="white",
    linewidth=0.5,
    height=0.7
)

# Revenue labels on bars
for bar in bars:
    width = bar.get_width()
    ax.text(
        width + 500,
        bar.get_y() + bar.get_height() / 2,
        f"${width:,.0f}",
        va="center",
        ha="left",
        fontsize=9,
        color="#333333"
    )

# Formatting
ax.set_xlabel("Total Order Revenue (USD)", fontsize=11, labelpad=10)
ax.set_title("Top 15 Suppliers by Revenue — Northwind Database", fontsize=14, fontweight="bold", pad=15)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="y", labelsize=9)

# Legend for categories
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color_map[cat], label=cat) for cat in color_map if cat in top15["CategoryName"].values]
ax.legend(handles=legend_elements, loc="lower right", fontsize=9, framealpha=0.7)

plt.tight_layout()
plt.savefig("outputs/01_supplier_revenue_top15.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 1 saved.")

#%%
# ── Chart 2: Revenue by Category (aggregated) ───────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

category_totals = (
    supplier_ranking
    .groupby("CategoryName")["total_order_revenue"]
    .sum()
    .sort_values(ascending=True)
)

colors_cat = [color_map.get(cat, "#999999") for cat in category_totals.index]

bars = ax.barh(
    category_totals.index,
    category_totals.values,
    color=colors_cat,
    edgecolor="white",
    linewidth=0.5,
    height=0.6
)

for bar in bars:
    width = bar.get_width()
    ax.text(
        width + 500,
        bar.get_y() + bar.get_height() / 2,
        f"${width:,.0f}",
        va="center",
        ha="left",
        fontsize=9,
        color="#333333"
    )

ax.set_xlabel("Total Revenue (USD)", fontsize=11, labelpad=10)
ax.set_title("Total Revenue by Product Category — Northwind Database", fontsize=14, fontweight="bold", pad=15)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="y", labelsize=10)

plt.tight_layout()
plt.savefig("outputs/01_category_revenue.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 2 saved.")
#%%
# ── Chart 3: Overall vs Category Rank — Quadrant Analysis ───────────────────
fig, ax = plt.subplots(figsize=(12, 8))

# Calculate medians for quadrant lines
median_overall = supplier_ranking["revenue_rank"].median()
median_category = supplier_ranking["Category_rank"].median()

# Plot points colored by category
for cat, group in supplier_ranking.groupby("CategoryName"):
    ax.scatter(
        group["revenue_rank"],
        group["Category_rank"],
        label=cat,
        color=color_map.get(cat, "#999999"),
        s=100,
        alpha=0.85,
        edgecolors="white",
        linewidth=0.5,
        zorder=3
    )

# Draw quadrant lines
ax.axvline(x=median_overall, color="#cccccc", linestyle="--", linewidth=1, alpha=0.7, zorder=1)
ax.axhline(y=median_category, color="#cccccc", linestyle="--", linewidth=1, alpha=0.7, zorder=1)

# Quadrant labels
ax.text(median_overall * 0.3, median_category * 0.3 - 0.3,
        "★ Overall & Category\nLeaders",
        fontsize=9, color="#2ecc71", fontweight="bold", alpha=0.8)
ax.text(median_overall * 1.3, median_category * 0.3 - 0.3,
        "◆ Niche Category\nSpecialists",
        fontsize=9, color="#3498db", fontweight="bold", alpha=0.8)
ax.text(median_overall * 0.3, median_category * 1.4,
        "▲ Overall Leaders\nMid Category",
        fontsize=9, color="#e67e22", fontweight="bold", alpha=0.8)
ax.text(median_overall * 1.3, median_category * 1.4,
        "▼ Underperformers",
        fontsize=9, color="#e74c3c", fontweight="bold", alpha=0.8)

# Annotate top 5 overall
for _, row in supplier_ranking[supplier_ranking["revenue_rank"] <= 5].iterrows():
    ax.annotate(
        row["SupplierName"].split()[0],
        (row["revenue_rank"], row["Category_rank"]),
        textcoords="offset points",
        xytext=(6, 4),
        fontsize=8,
        color="#333333"
    )

ax.set_xlabel("Overall Revenue Rank", fontsize=11, labelpad=10)
ax.set_ylabel("Category Revenue Rank", fontsize=11, labelpad=10)
ax.set_title("Overall vs Category Rank by Supplier — Northwind Database",
             fontsize=14, fontweight="bold", pad=15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(fontsize=9, framealpha=0.7, loc="upper left")

plt.tight_layout()
plt.savefig("outputs/01_rank_quadrant.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 3 saved.")








# %%
# Establish Database Connection
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=Northwind;"
    "Trusted_Connection=yes;"
)

print("Connection Succesful")

# Import sales_trends query from SQL files in dir
base_dir = os.path.dirname(os.path.abspath(__file__))
sql_path = os.path.join(base_dir, "02_sales_trends.sql")

with open(sql_path, "r") as file:
    sales_trends = file.read()

sales_trends = pd.read_sql(sales_trends, conn)
conn.close()

#%%
print(sales_trends.head(10))
print(f"\nShape: {sales_trends.shape}")
print(sales_trends.columns.tolist())
# %%
sales_trends["SaleMonth"] = pd.to_datetime(sales_trends['SaleMonth'])
sales_trends =sales_trends.sort_values('SaleMonth')

print(sales_trends.head(5))
print(sales_trends.dtypes)

# %%
fig, ax = plt.subplots(figsize=(14, 6))

median_overall = sales_trends["MonthlyRevenue"].median()
months = sales_trends["SaleMonth"]
revenue = sales_trends['MonthlyRevenue']

# Line + markers
ax.plot(months, revenue, 
        color='#2E74B5', 
        marker='o', 
        markersize=6, 
        linewidth=2.5, 
        label='Monthly Revenue',
        zorder=3)

# Median line
ax.axhline(y=median_overall, 
           color="#27AE60", 
           linestyle="--", 
           linewidth=1.5, 
           alpha=0.8, 
           zorder=1, 
           label=f'Median ${median_overall:,.0f}')

# Subtle vertical grid — helps trace each point to its month
ax.grid(axis='x', linestyle=':', linewidth=0.5, alpha=0.5, color='gray')
ax.grid(axis='y', linestyle=':', linewidth=0.5, alpha=0.3, color='gray')

# Every month on X axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))

# Y axis currency
ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, p: f'${x:,.0f}'
))

# Peak annotation
peak_idx = sales_trends['MonthlyRevenue'].idxmax()
peak_row = sales_trends.loc[peak_idx]
ax.annotate(f"Peak\n${peak_row['MonthlyRevenue']:,.0f}",
            xy=(peak_row['SaleMonth'], peak_row['MonthlyRevenue']),
            xytext=(-40, 15),
            textcoords='offset points',
            fontsize=8,
            fontweight='bold',
            color='#2E74B5',
            arrowprops=dict(arrowstyle='->', color='#2E74B5', lw=1.2))

# Low annotation
low_idx = sales_trends['MonthlyRevenue'].idxmin()
low_row = sales_trends.loc[low_idx]
ax.annotate(f"Low\n${low_row['MonthlyRevenue']:,.0f}",
            xy=(low_row['SaleMonth'], low_row['MonthlyRevenue']),
            xytext=(10, -30),
            textcoords='offset points',
            fontsize=8,
            fontweight='bold',
            color='#C0392B',
            arrowprops=dict(arrowstyle='->', color='#C0392B', lw=1.2))

ax.set_xlabel("Month", fontsize=11, labelpad=10)
ax.set_ylabel("Net Revenue", fontsize=11, labelpad=10)
ax.set_title("Monthly Revenue Trend — Northwind Database",
             fontsize=14, fontweight="bold", pad=15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(fontsize=9, framealpha=0.7, loc="upper left")

ax.text(months.iloc[-1], median_overall + 1500, 
        f'Median ${median_overall:,.0f}', 
        fontsize=8, color='#27AE60', va='bottom')
ax.fill_between(months, revenue, alpha=0.08, color='#2E74B5')

plt.tight_layout()
plt.savefig("outputs/02_Monthly_Revenue.png", dpi=150, bbox_inches="tight")
plt.show()
# %%

print(sales_trends[['SaleMonth', 'MoMGrowthPct']].to_string())
print(f"\nPositive months: {(sales_trends['MoMGrowthPct'] > 0).sum()}")
print(f"Negative months: {(sales_trends['MoMGrowthPct'] < 0).sum()}")
print(f"Biggest growth: {sales_trends['MoMGrowthPct'].max():.1f}%")
print(f"Biggest drop: {sales_trends['MoMGrowthPct'].min():.1f}%")

# %%

fig, ax = plt.subplots(figsize=(14, 6))

months = sales_trends["SaleMonth"]
growth = sales_trends["MoMGrowthPct"]

colors = ['#27AE60' if x > 0 else '#C0392B'
                  for x in sales_trends["MoMGrowthPct"]]

ax.bar(months,
       growth,
       color= colors,
       width=20)

ax.axhline(y=0, color='black', linewidth=1, zorder=2)

# Every month on X axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))

# Subtle vertical grid — helps trace each point to its month
ax.grid(axis='x', linestyle=':', linewidth=0.5, alpha=0.5, color='gray')
ax.grid(axis='y', linestyle=':', linewidth=0.5, alpha=0.3, color='gray')

ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, p: f'{x:.1f}%'
))
ax.set_xlabel("Month", fontsize=11, labelpad=10)
ax.set_ylabel("MoM Growth %", fontsize=11, labelpad=10)
ax.set_title("Month-over-Month Revenue Growth — Northwind Database",
             fontsize=14, fontweight="bold", pad=15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

legend_elements = [
    Patch(facecolor='#27AE60', label='Growth'),
    Patch(facecolor='#C0392B', label='Contraction')
]

ax.legend(handles=legend_elements, fontsize=9, 
          framealpha=0.7, loc="upper right")


for bar, value in zip(ax.patches, growth):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + (1 if value > 0 else -2.5),
        f'{value:.1f}%',
        ha='center',
        va='bottom' if value > 0 else 'top',
        fontsize=7,
        color='black'
    )

plt.tight_layout()
plt.savefig("outputs/03_MoM_Growth.png", dpi=150, bbox_inches="tight")
plt.show()

# %%
print(sales_trends["MonthlyRevenue"])