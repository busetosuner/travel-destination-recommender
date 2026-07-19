import pandas as pd

from src.recommendation_engine import calculate_city_score


def test_calculate_city_score_basic_case():
    city_row = pd.Series({
        "city": "Test City",
        "country": "Test Country",
        "short_description": "Test description",
        "budget_level": "Mid-range",
        "Cost_index": 55,
        "Best Time to Visit": "Spring, Summer",
        "seasonal_avg_temp": 28,
        "duration_category": "One Week",
        "beaches": 5,
        "wellness": 4,
        "seclusion": 3,
        "culture": 4,
        "urban": 4,
        "cuisine": 5,
        "nature": 3,
        "adventure": 2,
        "nightlife": 4,
        "safety": 5,
    })

    user_answers = {
        "budget": "Orta",
        "travel_season": "Yaz",
        "climate": "Sıcak",
        "travel_style": "Deniz & Relax",
        "travel_duration": "One Week",
        "beaches": "Çok önemli",
        "culture": "Önemli",
        "nature": "Orta",
        "cuisine": "Çok önemli",
        "nightlife": "Az önemli",
        "safety": "Çok önemli",
        "urban": "Az önemli",
        "seclusion": "Önemli",
        "adventure": "Orta",
    }

    result = calculate_city_score(
        city_row=city_row,
        user_answers=user_answers,
        low_cost_threshold=40,
        high_cost_threshold=70
    )

    assert result["city"] == "Test City"
    assert result["country"] == "Test Country"
    assert result["active_max_score"] > 0
    assert result["total_score"] > 0
    assert 0 <= result["compatibility_score"] <= 100
    assert "budget" in result["criterion_results"]
    assert "travel_style" in result["criterion_results"]
    assert "beaches" in result["criterion_results"]
    
    



from src.recommendation_engine import (
    calculate_city_score,
    apply_hard_constraints,
)   

def test_apply_hard_constraints_without_visa():
    dataset = pd.DataFrame({
        "city": ["Rome", "Belgrade", "London"],
        "visa_required": ["Yes", "No", "Yes"]
    })

    user_answers = {
        "has_visa": False
    }

    result = apply_hard_constraints(
        user_answers=user_answers,
        dataset=dataset
    )

    assert len(result) == 1
    assert result.iloc[0]["city"] == "Belgrade"


def test_apply_hard_constraints_with_visa():
    dataset = pd.DataFrame({
        "city": ["Rome", "Belgrade", "London"],
        "visa_required": ["Yes", "No", "Yes"]
    })

    user_answers = {
        "has_visa": True
    }

    result = apply_hard_constraints(
        user_answers=user_answers,
        dataset=dataset
    )

    assert len(result) == 3
    
    
    
from src.recommendation_engine import (
    calculate_city_score,
    apply_hard_constraints,
    rank_destinations,
)

def test_rank_destinations_basic():
    scored_cities = [
        {"city": "A", "compatibility_score": 91},
        {"city": "B", "compatibility_score": 84},
        {"city": "C", "compatibility_score": 97},
        {"city": "D", "compatibility_score": 76},
        {"city": "E", "compatibility_score": 88},
        {"city": "F", "compatibility_score": 82},
    ]

    result = rank_destinations(
        scored_cities=scored_cities,
        top_n=3
    )

    assert len(result) == 3
    assert result[0]["city"] == "C"
    assert result[1]["city"] == "A"
    assert result[2]["city"] == "E"
    
    
def test_rank_destinations_with_tie():
    scored_cities = [
        {"city": "A", "compatibility_score": 98},
        {"city": "B", "compatibility_score": 95},
        {"city": "C", "compatibility_score": 92},
        {"city": "D", "compatibility_score": 90},
        {"city": "E", "compatibility_score": 88},
        {"city": "F", "compatibility_score": 88},
        {"city": "G", "compatibility_score": 84},
    ]

    result = rank_destinations(
        scored_cities=scored_cities,
        top_n=5
    )

    assert len(result) == 6
    assert result[-1]["city"] == "F"