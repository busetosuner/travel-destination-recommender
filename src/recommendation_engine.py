"""
Recommendation Engine

This module coordinates the complete recommendation pipeline.

Responsibilities:
- Apply hard constraints
- Calculate all criterion scores
- Calculate compatibility score
- Rank destinations
- Return Top-N recommendations

This module does not implement individual scoring logic.
Scoring is delegated to scoring.py.
"""

import pandas as pd

from src.scoring import (
    calculate_budget_score,
    calculate_travel_season_score,
    calculate_climate_score,
    calculate_travel_style_score,
    calculate_preference_score,
    calculate_duration_score,
)


PREFERENCE_CRITERIA = {
    "beaches": 8,
    "culture": 8,
    "nature": 8,
    "cuisine": 7,
    "nightlife": 7,
    "safety": 8,
    "urban": 6,
    "seclusion": 6,
    "adventure": 6,
}


def apply_hard_constraints(
    user_answers: dict,
    dataset: pd.DataFrame
) -> pd.DataFrame:
    if user_answers.get("has_visa") is True:
        return dataset.copy()

    filtered_dataset = dataset[
        dataset["visa_required"] != "Yes"
    ].copy()

    return filtered_dataset




def add_score_result(
    criterion_results: dict,
    result: dict
) -> tuple[float, float]:
    criterion_results[result["criterion"]] = result

    if not result["active"]:
        return 0, 0

    return result["score"], result["max_score"]


def calculate_city_score(
    city_row: pd.Series,
    user_answers: dict,
    low_cost_threshold: float,
    high_cost_threshold: float
) -> dict:
    criterion_results = {}

    total_score = 0
    active_max_score = 0

    # Scoring results will be added here.
    
    budget_result = calculate_budget_score(
        user_budget=user_answers["budget"],
        city_budget=city_row.get("budget_level"),
        cost_index=city_row.get("Cost_index"),
        low_cost_threshold=low_cost_threshold,
        high_cost_threshold=high_cost_threshold
    )


    score, max_score = add_score_result(
    criterion_results=criterion_results,
    result=budget_result)

    total_score += score
    active_max_score += max_score
    
    
    
    season_result = calculate_travel_season_score(
        user_season=user_answers["travel_season"],
        best_time_to_visit=city_row.get("Best Time to Visit")
    )

    score, max_score = add_score_result(
        criterion_results=criterion_results,
        result=season_result
    )

    total_score += score
    active_max_score += max_score

    climate_result = calculate_climate_score(
        user_climate=user_answers["climate"],
        seasonal_avg_temp=city_row.get("seasonal_avg_temp")
    )

    score, max_score = add_score_result(
        criterion_results=criterion_results,
        result=climate_result
    )

    total_score += score
    active_max_score += max_score

    travel_style_result = calculate_travel_style_score(
        user_style=user_answers["travel_style"],
        city_features={
            "beaches": city_row.get("beaches"),
            "wellness": city_row.get("wellness"),
            "seclusion": city_row.get("seclusion"),
            "culture": city_row.get("culture"),
            "urban": city_row.get("urban"),
            "cuisine": city_row.get("cuisine"),
            "nature": city_row.get("nature"),
            "adventure": city_row.get("adventure"),
            "nightlife": city_row.get("nightlife"),
        }
    )

    score, max_score = add_score_result(
        criterion_results=criterion_results,
        result=travel_style_result
    )

    total_score += score
    active_max_score += max_score

    duration_result = calculate_duration_score(
        user_duration=user_answers["travel_duration"],
        city_duration_category=city_row.get("duration_category")
    )

    score, max_score = add_score_result(
        criterion_results=criterion_results,
        result=duration_result
    )

    total_score += score
    active_max_score += max_score



    for criterion, max_score_value in PREFERENCE_CRITERIA.items():
        preference_result = calculate_preference_score(
            criterion=criterion,
            user_importance=user_answers[criterion],
            feature_value=city_row.get(criterion),
            max_score=max_score_value
        )

        score, max_score = add_score_result(
            criterion_results=criterion_results,
            result=preference_result
        )

        total_score += score
        active_max_score += max_score


    compatibility_score = calculate_compatibility_score(
        total_score=total_score,
        active_max_score=active_max_score
    )



    return {
        "city": city_row.get("city"),
        "country": city_row.get("country"),
        "description": city_row.get("short_description"),
        "total_score": total_score,
        "active_max_score": active_max_score,
        "compatibility_score": compatibility_score,
        "criterion_results": criterion_results,
        "latitude": city_row.get("latitude"),
        "longitude": city_row.get("longitude"),
        
    }



def calculate_compatibility_score(
    total_score: float,
    active_max_score: float
) -> float:
    if active_max_score == 0:
        return 0

    return round((total_score / active_max_score) * 100, 2)



def rank_destinations(
    scored_cities: list,
    top_n: int = 5
) -> list:
    if not scored_cities:
        return []

    sorted_cities = sorted(
        scored_cities,
        key=lambda city: city["compatibility_score"],
        reverse=True
    )

    if len(sorted_cities) <= top_n:
        return sorted_cities

    top_cities = sorted_cities[:top_n]
    cutoff_score = top_cities[-1]["compatibility_score"]

    tied_cities = [
        city for city in sorted_cities[top_n:]
        if city["compatibility_score"] == cutoff_score
    ]

    return top_cities + tied_cities




def generate_recommendations(
    user_answers: dict,
    master_dataset: pd.DataFrame,
    top_n: int = 5
) -> list:
    candidate_dataset = apply_hard_constraints(
        user_answers=user_answers,
        dataset=master_dataset
    )

    cost_index_values = candidate_dataset["Cost_index"].dropna()

    low_cost_threshold = cost_index_values.quantile(0.25)
    high_cost_threshold = cost_index_values.quantile(0.75)

    scored_cities = []

    for _, city_row in candidate_dataset.iterrows():
        city_score = calculate_city_score(
            city_row=city_row,
            user_answers=user_answers,
            low_cost_threshold=low_cost_threshold,
            high_cost_threshold=high_cost_threshold
        )

        scored_cities.append(city_score)

    recommendations = rank_destinations(
        scored_cities=scored_cities,
        top_n=top_n
    )

    return recommendations