import pandas as pd
from pathlib import Path

# ============================================================
# 1. File paths
# ============================================================

BASE_DIR = Path(__file__).parent

worldwide_path = BASE_DIR / "Worldwide_Travel_Cities.csv"
destinations_path = BASE_DIR / "europe_destinations.csv"
living_cost_path = BASE_DIR / "eur_cities.csv"


# ============================================================
# 2. Helper function to read CSV files safely
# ============================================================

def read_csv_safely(file_path, sep=","):
    try:
        return pd.read_csv(
            file_path,
            sep=sep,
            quotechar='"',
            engine="python",
            on_bad_lines="warn"
        )
    except Exception as e:
        print(f"\nError reading {file_path.name}:")
        print(e)
        print("\nTrying again by skipping problematic lines...\n")

        return pd.read_csv(
            file_path,
            sep=sep,
            quotechar='"',
            engine="python",
            on_bad_lines="skip"
        )


# ============================================================
# 3. Read datasets
# ============================================================

worldwide = read_csv_safely(worldwide_path, sep=",")
destinations = read_csv_safely(destinations_path, sep=";")
living_cost = read_csv_safely(living_cost_path, sep=",")


# ============================================================
# 4. Basic dataset information
# ============================================================

datasets = {
    "Worldwide Travel Cities": worldwide,
    "Europe Destinations": destinations,
    "Living Cost": living_cost
}

for name, df in datasets.items():
    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)

    print("Shape:", df.shape)

    print("\nColumns:")
    for col in df.columns:
        print("-", col)

    print("\nFirst 5 rows:")
    print(df.head())


# ============================================================
# 5. Europe filter for Worldwide Travel Cities
# ============================================================

print("\n" + "=" * 80)
print("Worldwide region values")
print("=" * 80)

if "region" in worldwide.columns:
    print(worldwide["region"].value_counts(dropna=False))

    worldwide_europe = worldwide[
        worldwide["region"].astype(str).str.lower().str.strip() == "europe"
    ].copy()

    print("\nWorldwide Europe shape:", worldwide_europe.shape)
else:
    print("No region column found in Worldwide Travel Cities.")
    worldwide_europe = worldwide.copy()


# ============================================================
# 6. Standardize city names for comparison
# ============================================================

def normalize_city_name(series):
    return (
        series
        .astype(str)
        .str.lower()
        .str.strip()
        .str.replace("ı", "i", regex=False)
        .str.replace("ğ", "g", regex=False)
        .str.replace("ü", "u", regex=False)
        .str.replace("ş", "s", regex=False)
        .str.replace("ö", "o", regex=False)
        .str.replace("ç", "c", regex=False)
    )


worldwide_city_col = "city"
destinations_city_col = "Destination"
living_cost_city_col = "City"

worldwide_cities = set(
    normalize_city_name(worldwide_europe[worldwide_city_col]).dropna()
)

destination_cities = set(
    normalize_city_name(destinations[destinations_city_col]).dropna()
)

living_cost_cities = set(
    normalize_city_name(living_cost[living_cost_city_col]).dropna()
)


# ============================================================
# 7. City count analysis
# ============================================================

print("\n" + "=" * 80)
print("City counts")
print("=" * 80)

print("Worldwide Europe cities:", len(worldwide_cities))
print("Europe Destinations cities:", len(destination_cities))
print("Living Cost cities:", len(living_cost_cities))


print("\n" + "=" * 80)
print("Common city counts")
print("=" * 80)

print("Worldwide ∩ Destinations:", len(worldwide_cities & destination_cities))
print("Worldwide ∩ Living Cost:", len(worldwide_cities & living_cost_cities))
print("Destinations ∩ Living Cost:", len(destination_cities & living_cost_cities))
print("All three:", len(worldwide_cities & destination_cities & living_cost_cities))


# ============================================================
# 8. Missing city examples
# ============================================================

print("\n" + "=" * 80)
print("Missing city examples")
print("=" * 80)

print("\nCities in Worldwide Europe but NOT in Destinations:")
print(sorted(list(worldwide_cities - destination_cities))[:50])

print("\nCities in Destinations but NOT in Worldwide Europe:")
print(sorted(list(destination_cities - worldwide_cities))[:50])

print("\nCities in Worldwide Europe but NOT in Living Cost:")
print(sorted(list(worldwide_cities - living_cost_cities))[:50])

print("\nCities in Living Cost but NOT in Worldwide Europe:")
print(sorted(list(living_cost_cities - worldwide_cities))[:50])


# ============================================================
# 9. Missing value summary
# ============================================================

print("\n" + "=" * 80)
print("Missing value summary")
print("=" * 80)

for name, df in datasets.items():
    print("\n" + name)
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        print("No missing values.")
    else:
        print(missing)