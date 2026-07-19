"""
Data preprocessing utilities for the recommendation engine.

Responsibilities:
- Rename columns used by the engine
- Merge country reference data
- Create seasonal average temperature
- Create travel duration category
"""

import ast
import pandas as pd


def parse_monthly_temperatures(value):
    if pd.isna(value):
        return {}

    if isinstance(value, dict):
        return value

    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return {}

def calculate_seasonal_avg_temp(monthly_temps, user_season):
    season_months = {
        "İlkbahar": ["3", "4", "5"],
        "Yaz": ["6", "7", "8"],
        "Sonbahar": ["9", "10", "11"],
        "Kış": ["12", "1", "2"],
    }

    months = season_months.get(user_season)

    if not months:
        return None

    values = []

    for month in months:
        month_data = monthly_temps.get(month)

        if isinstance(month_data, dict) and month_data.get("avg") is not None:
            values.append(month_data["avg"])

    if not values:
        return None

    return sum(values) / len(values)


def map_duration_category(value):
    if pd.isna(value):
        return None

    text = str(value).lower()

    if any(keyword in text for keyword in ["1-3", "2-3", "weekend"]):
        return "Weekend Trip"

    if any(keyword in text for keyword in ["3-5", "4-6", "short"]):
        return "Short Trip"

    if any(keyword in text for keyword in ["5-7", "7", "week"]):
        return "One Week"

    if any(keyword in text for keyword in ["10", "14", "long"]):
        return "Long Vacation"

    return None



def clean_coordinate_value(value):
    if value is None or pd.isna(value):
        return None

    text = str(value).strip().replace(",", ".")

    try:
        return float(text)
    except ValueError:
        pass

    sign = ""

    if text.startswith("-"):
        sign = "-"
        text = text[1:]

    parts = text.split(".")

    if len(parts) < 2:
        return None

    integer_part = parts[0]
    decimal_part = "".join(parts[1:])

    cleaned_text = f"{sign}{integer_part}.{decimal_part}"

    try:
        return float(cleaned_text)
    except ValueError:
        return None


def prepare_dataset_for_recommendation(
    master_dataset: pd.DataFrame,
    country_reference: pd.DataFrame,
    user_season: str
) -> pd.DataFrame:
    dataset = master_dataset.copy()

    dataset["latitude"] = dataset["latitude"].apply(
        clean_coordinate_value
    )

    dataset["longitude"] = dataset["longitude"].apply(
        clean_coordinate_value
    )

    dataset = dataset.rename(
        columns={
            "Safety": "safety"
        }
    )

    dataset["safety"] = dataset["safety"].apply(
        map_safety_score
    )

    dataset = dataset.merge(
        country_reference[["country", "visa_required"]],
        on="country",
        how="left"
    )

    dataset["monthly_temps_parsed"] = dataset["avg_temp_monthly"].apply(
        parse_monthly_temperatures
    )

    dataset["seasonal_avg_temp"] = dataset["monthly_temps_parsed"].apply(
        lambda temps: calculate_seasonal_avg_temp(
            monthly_temps=temps,
            user_season=user_season
        )
    )

    dataset["duration_category"] = dataset["ideal_durations"].apply(
        map_duration_category
    )

    return dataset


def map_safety_score(value):
    if pd.isna(value):
        return None

    text = str(value).lower()

    if "ongoing conflict" in text or "potential risks" in text:
        return 2

    if "pickpocket" in text:
        return 4

    if "generally safe" in text:
        return 5

    return None