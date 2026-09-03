"""
HR Analytics & Employee Attrition Analysis
------------------------------------------
Exploratory analysis + attrition rate breakdowns by key factors.
Exports summary tables and charts for Power BI / portfolio.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE = Path(__file__).parent.parent
DATA = BASE / "data"
CHARTS = Path(__file__).parent / "charts"
CHARTS.mkdir(exist_ok=True)
SUMMARIES = DATA / "summaries"
SUMMARIES.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (11, 6)

# ----------------------------------------------------------
# 1. LOAD DATA
# ----------------------------------------------------------
df = pd.read_csv(DATA / "employee_data.csv")
print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)
print(f"Shape: {df.shape}")
print(f"\nColumns:\n{df.dtypes}")
print(f"\nMissing values: {df.isnull().sum().sum()}")
print(f"\nAttrition value counts:\n{df['Attrition'].value_counts()}")

# ----------------------------------------------------------
# 2. OVERALL KPIs
# ----------------------------------------------------------
total_emp = len(df)
attrition_count = (df["Attrition"] == "Yes").sum()
attrition_rate = attrition_count / total_emp * 100
avg_income = df["MonthlyIncome"].mean()
avg_tenure = df["YearsAtCompany"].mean()
avg_age = df["Age"].mean()

print("\n" + "=" * 60)
print("OVERALL KPIs")
print("=" * 60)
print(f"Total Employees     : {total_emp}")
print(f"Employees Left      : {attrition_count}")
print(f"Attrition Rate      : {attrition_rate:.2f}%")
print(f"Avg Monthly Income  : ${avg_income:,.0f}")
print(f"Avg Tenure (Years)  : {avg_tenure:.1f}")
print(f"Avg Age             : {avg_age:.1f}")

# ----------------------------------------------------------
# 3. ATTRITION BY KEY DIMENSIONS
# ----------------------------------------------------------
def attrition_by(col):
    t = pd.crosstab(df[col], df["Attrition"], normalize="index") * 100
    t["Count"] = df[col].value_counts()
    return t.round(2)

print("\n" + "=" * 60)
print("ATTRITION BY DEPARTMENT")
print("=" * 60)
print(attrition_by("Department").sort_values("Yes", ascending=False))

print("\n" + "=" * 60)
print("ATTRITION BY OVERTIME")
print("=" * 60)
print(attrition_by("OverTime"))

print("\n" + "=" * 60)
print("ATTRITION BY JOB SATISFACTION")
print("=" * 60)
print(attrition_by("JobSatisfaction"))

print("\n" + "=" * 60)
print("ATTRITION BY WORK-LIFE BALANCE")
print("=" * 60)
print(attrition_by("WorkLifeBalance"))

# ----------------------------------------------------------
# 4. FEATURE ENGINEERING FOR SUMMARY
# ----------------------------------------------------------
df["TenureBand"] = pd.cut(
    df["YearsAtCompany"],
    bins=[-1, 0, 2, 5, 10, 100],
    labels=["0 years", "1-2 years", "3-5 years", "6-10 years", "10+ years"]
)
df["IncomeBand"] = pd.cut(
    df["MonthlyIncome"],
    bins=[0, 4000, 6000, 9000, 20000],
    labels=["Low (<4k)", "Medium (4-6k)", "High (6-9k)", "Very High (9k+)"]
)
df["PromotionStatus"] = pd.cut(
    df["YearsSinceLastPromotion"],
    bins=[-1, 0, 3, 100],
    labels=["Recently Promoted", "1-3 years ago", "4+ years ago"]
)

# ----------------------------------------------------------
# 5. VISUALIZATIONS
# ----------------------------------------------------------
# 5.1 Overall Attrition Pie
fig, ax = plt.subplots()
df["Attrition"].value_counts().plot.pie(autopct="%1.1f%%", colors=["#4CAF50", "#F44336"], ax=ax, startangle=90)
ax.set_ylabel("")
ax.set_title("Overall Attrition Rate")
plt.tight_layout()
plt.savefig(CHARTS / "01_overall_attrition.png", dpi=150)
plt.close()

# 5.2 Attrition by Department
dept_attr = df.groupby("Department")["Attrition"].apply(lambda x: (x == "Yes").mean() * 100).sort_values(ascending=False)
fig, ax = plt.subplots()
dept_attr.plot(kind="bar", color="steelblue", ax=ax)
ax.set_title("Attrition Rate by Department (%)")
ax.set_ylabel("Attrition Rate (%)")
ax.tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.savefig(CHARTS / "02_attrition_by_department.png", dpi=150)
plt.close()

# 5.3 Attrition by OverTime
fig, ax = plt.subplots()
sns.countplot(data=df, x="OverTime", hue="Attrition", ax=ax, palette={"Yes": "#F44336", "No": "#4CAF50"})
ax.set_title("Attrition by OverTime")
plt.tight_layout()
plt.savefig(CHARTS / "03_attrition_by_overtime.png", dpi=150)
plt.close()

# 5.4 Attrition by Job Satisfaction
fig, ax = plt.subplots()
sns.countplot(data=df, x="JobSatisfaction", hue="Attrition", ax=ax, palette={"Yes": "#F44336", "No": "#4CAF50"})
ax.set_title("Attrition by Job Satisfaction (1=Low, 4=High)")
plt.tight_layout()
plt.savefig(CHARTS / "04_attrition_by_job_satisfaction.png", dpi=150)
plt.close()

# 5.5 Attrition by Work-Life Balance
fig, ax = plt.subplots()
sns.countplot(data=df, x="WorkLifeBalance", hue="Attrition", ax=ax, palette={"Yes": "#F44336", "No": "#4CAF50"})
ax.set_title("Attrition by Work-Life Balance (1=Bad, 4=Best)")
plt.tight_layout()
plt.savefig(CHARTS / "05_attrition_by_worklife.png", dpi=150)
plt.close()

# 5.6 Monthly Income distribution by Attrition
fig, ax = plt.subplots()
sns.boxplot(data=df, x="Attrition", y="MonthlyIncome", ax=ax, palette={"Yes": "#F44336", "No": "#4CAF50"})
ax.set_title("Monthly Income by Attrition Status")
plt.tight_layout()
plt.savefig(CHARTS / "06_income_by_attrition.png", dpi=150)
plt.close()

# 5.7 Tenure Band vs Attrition
fig, ax = plt.subplots()
tenure_attr = pd.crosstab(df["TenureBand"], df["Attrition"], normalize="index") * 100
tenure_attr["Yes"].plot(kind="bar", color="#F44336", ax=ax)
ax.set_title("Attrition Rate by Tenure Band (%)")
ax.set_ylabel("Attrition Rate (%)")
ax.tick_params(axis="x", rotation=20)
plt.tight_layout()
plt.savefig(CHARTS / "07_attrition_by_tenure.png", dpi=150)
plt.close()

# 5.8 Age distribution by Attrition
fig, ax = plt.subplots()
sns.histplot(data=df, x="Age", hue="Attrition", kde=True, ax=ax, palette={"Yes": "#F44336", "No": "#4CAF50"})
ax.set_title("Age Distribution by Attrition")
plt.tight_layout()
plt.savefig(CHARTS / "08_age_by_attrition.png", dpi=150)
plt.close()

print(f"\nCharts saved to: {CHARTS}")

# ----------------------------------------------------------
# 6. EXPORT SUMMARIES
# ----------------------------------------------------------
# Department summary
dept_summary = df.groupby("Department").agg(
    Employees=("EmployeeID", "count"),
    Attrition_Count=("Attrition", lambda x: (x == "Yes").sum()),
    Attrition_Rate=("Attrition", lambda x: (x == "Yes").mean() * 100),
    Avg_Income=("MonthlyIncome", "mean"),
    Avg_Tenure=("YearsAtCompany", "mean"),
    Avg_JobSatisfaction=("JobSatisfaction", "mean")
).round(2).sort_values("Attrition_Rate", ascending=False)
dept_summary.to_csv(SUMMARIES / "department_summary.csv")

# Overall KPIs
kpi = pd.DataFrame([{
    "Total_Employees": total_emp,
    "Employees_Left": attrition_count,
    "Attrition_Rate_Pct": round(attrition_rate, 2),
    "Avg_Monthly_Income": round(avg_income, 0),
    "Avg_Tenure_Years": round(avg_tenure, 1),
    "Avg_Age": round(avg_age, 1)
}])
kpi.to_csv(SUMMARIES / "overall_kpis.csv", index=False)

# Full enriched data for Power BI
df.to_csv(SUMMARIES / "employee_data_enriched.csv", index=False)

print(f"Summaries exported to: {SUMMARIES}")
print("\n✅ HR Attrition Analysis complete.")
print("   Next: Load employee_data.csv (or enriched version) into Power BI.")
