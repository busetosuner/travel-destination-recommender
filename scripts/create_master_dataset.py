import pandas as pd
from pathlib import Path
import unicodedata

BASE_DIR = Path(__file__).parent

worldwide_path = BASE_DIR / "Worldwide_Travel_Cities.csv"
destinations_path = BASE_DIR / "europe_destinations.csv"
living_cost_path = BASE_DIR / "eur_cities.csv"

# 1. Read files
worldwide = pd.read_csv(worldwide_path, sep=";")
destinations = pd.read_csv(destinations_path, sep=";", encoding="latin1")
living_cost = pd.read_csv(living_cost_path, sep=";")

# 2. Normalize city names
def normalize_text(value):
    if pd.isna(value):
        return ""

    value = str(value).lower().strip()
    value = unicodedata.normalize("NFKD", value)
    value = "".join([c for c in value if not unicodedata.combining(c)])

    return value

# 3. Main dataset: Worldwide Europe
worldwide_europe = worldwide[
    worldwide["region"].astype(str).str.lower().str.strip() == "europe"
].copy()

worldwide_europe["city_key"] = worldwide_europe["city"].apply(normalize_text)

worldwide_selected = worldwide_europe[
    [
        "city_key",
        "city",
        "country",
        "short_description",
        "latitude",
        "longitude",
        "avg_temp_monthly",
        "ideal_durations",
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
    ]
].copy()

# 4. Europe destinations selected columns
destinations["city_key"] = destinations["Destination"].apply(normalize_text)

destinations_selected = destinations[
    [
        "city_key",
        "Category",
        "Approximate Annual Tourists",
        "Famous Foods",
        "Best Time to Visit",
        "Cost of Living",
        "Safety",
        "Cultural Significance",
        "Description",
    ]
].copy()

# duplicated city keys varsa ilkini al
destinations_selected = destinations_selected.drop_duplicates(subset=["city_key"])

# 5. Living cost selected columns
living_cost["city_key"] = living_cost["City"].apply(normalize_text)

living_cost_selected = living_cost[
    [
        "city_key",
        "Cost_index",
        "Meal, Inexpensive Restaurant",
        "One-way Ticket (Local Transport)",
        "Monthly Pass (Regular Price)",
        "Taxi Start (Normal Tariff)",
        "Apartment (1 bedroom) in City Centre",
        "Average Monthly Net Salary (After Tax)",
    ]
].copy()

living_cost_selected = living_cost_selected.drop_duplicates(subset=["city_key"])

# 6. Merge
master = worldwide_selected.merge(
    destinations_selected,
    on="city_key",
    how="left"
)

master = master.merge(
    living_cost_selected,
    on="city_key",
    how="left"
)

# 7. Save
output_path = BASE_DIR / "master_dataset_v1.csv"
master.to_csv(output_path, index=False, encoding="utf-8-sig")

# 8. Summary
print("Master dataset created successfully.")
print("Output file:", output_path)
print("Shape:", master.shape)

print("\nMissing values in added columns:")
added_columns = [
    "Category",
    "Safety",
    "Cost of Living",
    "Cost_index",
    "Description",
]
print(master[added_columns].isnull().sum())