from src.scoring import (
    calculate_travel_style_score,
    NO_PREFERENCE
)


def test_travel_style_beach_relax():
    result = calculate_travel_style_score(
        user_style="Deniz & Relax",
        city_features={
            "beaches": 5,
            "wellness": 4,
            "seclusion": 3
        }
    )

    assert result["active"] is True
    assert result["score"] == 8.6
    assert result["max_score"] == 10
    assert result["criterion"] == "travel_style"


def test_travel_style_no_preference():
    result = calculate_travel_style_score(
        user_style=NO_PREFERENCE,
        city_features={
            "beaches": 5,
            "wellness": 4,
            "seclusion": 3
        }
    )

    assert result["active"] is False
    assert result["score"] == 0
    assert result["max_score"] == 0


def test_travel_style_missing_feature():
    result = calculate_travel_style_score(
        user_style="Deniz & Relax",
        city_features={
            "beaches": 5,
            "wellness": None,
            "seclusion": 3
        }
    )

    # beaches: (5/5)*5 = 5
    # seclusion: (3/5)*2 = 1.2
    # active max: 5 + 2 = 7
    assert result["active"] is True
    assert result["score"] == 6.2
    assert result["max_score"] == 7
    
    
    

from src.scoring import (
    calculate_travel_style_score,
    calculate_travel_season_score,
    NO_PREFERENCE
)

def test_travel_season_match():
    result = calculate_travel_season_score(
        user_season="Yaz",
        best_time_to_visit="Spring, Summer"
    )

    assert result["active"] is True
    assert result["score"] == 15
    assert result["max_score"] == 15
    assert result["criterion"] == "travel_season"


def test_travel_season_no_match():
    result = calculate_travel_season_score(
        user_season="Kış",
        best_time_to_visit="Spring, Summer"
    )

    assert result["active"] is True
    assert result["score"] == 0
    assert result["max_score"] == 15


def test_travel_season_no_preference():
    result = calculate_travel_season_score(
        user_season=NO_PREFERENCE,
        best_time_to_visit="Spring, Summer"
    )

    assert result["active"] is False
    assert result["score"] == 0
    assert result["max_score"] == 0
    
    
    

from src.scoring import (
    calculate_travel_style_score,
    calculate_travel_season_score,
    calculate_climate_score,
    NO_PREFERENCE
)

def test_climate_mild_match():
    result = calculate_climate_score(
        user_climate="Ilık",
        seasonal_avg_temp=20
    )

    assert result["active"] is True
    assert result["score"] == 15
    assert result["max_score"] == 15
    assert result["criterion"] == "climate"


def test_climate_cool_match():
    result = calculate_climate_score(
        user_climate="Serin",
        seasonal_avg_temp=10
    )

    assert result["active"] is True
    assert result["score"] == 15
    assert result["max_score"] == 15
    assert result["criterion"] == "climate"


def test_climate_hot_match():
    result = calculate_climate_score(
        user_climate="Sıcak",
        seasonal_avg_temp=28
    )

    assert result["active"] is True
    assert result["score"] == 15
    assert result["max_score"] == 15
    assert result["criterion"] == "climate"


def test_climate_no_preference():
    result = calculate_climate_score(
        user_climate=NO_PREFERENCE,
        seasonal_avg_temp=20
    )

    assert result["active"] is False
    assert result["score"] == 0
    assert result["max_score"] == 0


def test_climate_missing_temperature():
    result = calculate_climate_score(
        user_climate="Ilık",
        seasonal_avg_temp=None
    )

    assert result["active"] is False
    assert result["score"] == 0
    assert result["max_score"] == 0
    
    
from src.scoring import (
    calculate_preference_score,
    calculate_duration_score,
    calculate_travel_style_score,
    calculate_travel_season_score,
    calculate_climate_score,
    calculate_budget_score,
    NO_PREFERENCE
)   

def test_budget_full_match():
    result = calculate_budget_score(
        user_budget="Orta",
        city_budget="Mid-range",
        cost_index=55,
        low_cost_threshold=40,
        high_cost_threshold=70
    )

    assert result["active"] is True
    assert result["score"] == 20
    assert result["max_score"] == 20
    assert result["criterion"] == "budget"


def test_budget_level_only():
    result = calculate_budget_score(
        user_budget="Orta",
        city_budget="Mid-range",
        cost_index=None
    )

    assert result["active"] is True
    assert result["score"] == 12
    assert result["max_score"] == 12


def test_cost_index_only():
    result = calculate_budget_score(
        user_budget="Orta",
        city_budget=None,
        cost_index=55,
        low_cost_threshold=40,
        high_cost_threshold=70
    )

    assert result["active"] is True
    assert result["score"] == 8
    assert result["max_score"] == 8


def test_budget_no_preference():
    result = calculate_budget_score(
        user_budget=NO_PREFERENCE,
        city_budget="Budget",
        cost_index=25,
        low_cost_threshold=40,
        high_cost_threshold=70
    )

    assert result["active"] is False
    assert result["score"] == 0
    assert result["max_score"] == 0


def test_budget_missing_data():
    result = calculate_budget_score(
        user_budget="Orta",
        city_budget=None,
        cost_index=None
    )

    assert result["active"] is False
    assert result["score"] == 0
    assert result["max_score"] == 0
    
    
    
def test_preference_score_very_important():
    result = calculate_preference_score(
        criterion="beaches",
        user_importance="Çok önemli",
        feature_value=4,
        max_score=8
    )

    assert result["active"] is True
    assert result["score"] == 6.4
    assert result["max_score"] == 8
    assert result["criterion"] == "beaches"


def test_preference_score_medium_importance():
    result = calculate_preference_score(
        criterion="culture",
        user_importance="Orta",
        feature_value=5,
        max_score=8
    )

    assert result["active"] is True
    assert result["score"] == 4.0
    assert result["max_score"] == 8
    assert result["criterion"] == "culture"


def test_preference_score_no_preference():
    result = calculate_preference_score(
        criterion="nature",
        user_importance=NO_PREFERENCE,
        feature_value=5,
        max_score=8
    )

    assert result["active"] is False
    assert result["score"] == 0
    assert result["max_score"] == 0


def test_preference_score_missing_feature():
    result = calculate_preference_score(
        criterion="cuisine",
        user_importance="Çok önemli",
        feature_value=None,
        max_score=7
    )

    assert result["active"] is False
    assert result["score"] == 0
    assert result["max_score"] == 0


def test_duration_exact_match():
    result = calculate_duration_score(
        user_duration="One Week",
        city_duration_category="One Week"
    )

    assert result["active"] is True
    assert result["score"] == 5
    assert result["max_score"] == 5
    assert result["criterion"] == "travel_duration"


def test_duration_near_match():
    result = calculate_duration_score(
        user_duration="Short Trip",
        city_duration_category="One Week"
    )

    assert result["active"] is True
    assert result["score"] == 3
    assert result["max_score"] == 5


def test_duration_no_preference():
    result = calculate_duration_score(
        user_duration=NO_PREFERENCE,
        city_duration_category="One Week"
    )

    assert result["active"] is False
    assert result["score"] == 0
    assert result["max_score"] == 0


def test_duration_missing_data():
    result = calculate_duration_score(
        user_duration="One Week",
        city_duration_category=None
    )

    assert result["active"] is False
    assert result["score"] == 0
    assert result["max_score"] == 0