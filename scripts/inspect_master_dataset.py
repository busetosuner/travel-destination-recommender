import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
master_path = BASE_DIR / "master_dataset_v1.csv"

master = pd.read_csv(master_path)

print("=" * 80)
print("MASTER DATASET OVERVIEW")
print("=" * 80)
print("Shape:", master.shape)

print("\nColumns:")
for col in master.columns:
    print("-", col)

print("\nFirst 5 rows:")
print(master.head())

# Ana algoritma kolonları
core_columns = [
    "budget_level",
    "culture",
    "adventure",
    "nature",
    "beaches",
    "nightlife",
    "cuisine",
    "wellness",
    "urban",
    "seclusion",
    "avg_temp_monthly",
    "ideal_durations",
]

print("\n" + "=" * 80)
print("CORE COLUMN MISSING VALUES")
print("=" * 80)
print(master[core_columns].isnull().sum())

# Destek kolonları
support_columns = [
    "Category",
    "Safety",
    "Cost of Living",
    "Cost_index",
    "Description",
    "Best Time to Visit",
]

print("\n" + "=" * 80)
print("SUPPORT COLUMN MISSING VALUES")
print("=" * 80)
print(master[support_columns].isnull().sum())

print("\n" + "=" * 80)
print("CITIES WITH SAFETY INFO")
print("=" * 80)
print(master.loc[master["Safety"].notna(), ["city", "country", "Safety"]].head(30))

print("\n" + "=" * 80)
print("CITIES WITH COST INDEX")
print("=" * 80)
print(master.loc[master["Cost_index"].notna(), ["city", "country", "Cost_index"]].head(30))

print("\n" + "=" * 80)
print("BUDGET LEVEL DISTRIBUTION")
print("=" * 80)
print(master["budget_level"].value_counts(dropna=False))

print("\n" + "=" * 80)
print("COUNTRY COUNTS")
print("=" * 80)
print(master["country"].value_counts().head(30))