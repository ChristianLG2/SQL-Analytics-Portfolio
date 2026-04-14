#%%
#Load libraries
import os
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

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


# %%
