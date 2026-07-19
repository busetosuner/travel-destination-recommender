"""
Travel Recommendation System
----------------------------

This module contains all criterion-level scoring functions.

Responsibilities:
- Budget scoring
- Climate scoring
- Travel season scoring
- Travel style scoring
- Preference scoring
- Duration scoring

Each scoring function returns a standardized ScoreResult object.

This module does not perform:
- Hard constraint filtering
- Final ranking
- Compatibility score calculation

These responsibilities belong to recommendation_engine.py.
"""

# STABLE MODULE V1

from typing import Optional, Dict, Any, Tuple
import pandas as pd

ScoreResult = Dict[str, Any]

# -----------------------------
# Constants
# -----------------------------

NO_PREFERENCE = "Fark etmez"

BUDGET_LEVEL_MATRIX = {
    "Düşük": {
        "Budget": 12,
        "Mid-range": 7,
        "Luxury": 1,
    },
    "Orta": {
        "Budget": 10,
        "Mid-range": 12,
        "Luxury": 6,
    },
    "Yüksek": {
        "Budget": 5,
        "Mid-range": 9,
        "Luxury": 12,
    },
}

COST_INDEX_MATRIX = {
    "Düşük": {
        "Low Cost": 8,
        "Mid Cost": 4,
        "High Cost": 1,
    },
    "Orta": {
        "Low Cost": 6,
        "Mid Cost": 8,
        "High Cost": 4,
    },
    "Yüksek": {
        "Low Cost": 3,
        "Mid Cost": 6,
        "High Cost": 8,
    },
}

IMPORTANCE_MULTIPLIERS = {
    "Çok önemli": 1.00,
    "Önemli": 0.75,
    "Orta": 0.50,
    "Az önemli": 0.25,
}

TRAVEL_STYLE_MAPPING = {
    "Deniz & Relax": {
        "beaches": 5,
        "wellness": 3,
        "seclusion": 2,
    },
    "Kültürel Gezi": {
        "culture": 5,
        "urban": 3,
        "cuisine": 2,
    },
    "Doğa & Macera": {
        "nature": 5,
        "adventure": 3,
        "seclusion": 2,
    },
    "Şehir & Eğlence": {
        "urban": 5,
        "nightlife": 3,
        "cuisine": 2,
    },
}




DURATION_MATRIX = {
    "Weekend Trip": {
        "Weekend Trip": 5,
        "Short Trip": 3,
        "One Week": 1,
        "Long Vacation": 0,
    },
    "Short Trip": {
        "Weekend Trip": 3,
        "Short Trip": 5,
        "One Week": 3,
        "Long Vacation": 1,
    },
    "One Week": {
        "Weekend Trip": 1,
        "Short Trip": 3,
        "One Week": 5,
        "Long Vacation": 3,
    },
    "Long Vacation": {
        "Weekend Trip": 0,
        "Short Trip": 1,
        "One Week": 3,
        "Long Vacation": 5,
    },
}

MAX_FEATURE_VALUE = 5

SEASON_KEYWORDS = {
    "İlkbahar": "Spring",
    "Yaz": "Summer",
    "Sonbahar": "Autumn",
    "Kış": "Winter",
}

CLIMATE_SEGMENTS = {
    "cool": {
        "max_temp": 15
    },
    "mild": {
        "min_temp": 15,
        "max_temp": 25
    },
    "hot": {
        "min_temp": 25
    },
}

CLIMATE_SCORE_MATRIX = {
    "Serin": {
        "cool": 15,
        "mild": 8,
        "hot": 2,
    },
    "Ilık": {
        "cool": 8,
        "mild": 15,
        "hot": 8,
    },
    "Sıcak": {
        "cool": 2,
        "mild": 8,
        "hot": 15,
    },
}


REASON_TEMPLATES = {
    "budget": "Seçtiğiniz bütçe aralığı ile uyumludur.",
    "travel_season": "Tercih ettiğiniz seyahat dönemi için önerilmektedir.",
    "climate": "Tercih ettiğiniz hava koşullarını karşılamaktadır.",
    "travel_style": "Genel tatil tarzınıza uygundur.",

    "beaches": "Deniz tatili beklentinizi karşılamaktadır.",
    "culture": "Kültürel gezi beklentinize uygundur.",
    "nature": "Doğa odaklı tatil tercihinizi desteklemektedir.",
    "cuisine": "Yerel mutfak beklentinizi karşılamaktadır.",
    "nightlife": "Gece hayatı beklentinize uygundur.",
    "safety": "Güvenlik beklentinizi karşılamaktadır.",
    "urban": "Canlı şehir hayatı tercihinize uygundur.",
    "seclusion": "Sakin ve huzurlu ortam beklentinizi karşılamaktadır.",
    "adventure": "Macera ve açık hava aktiviteleri beklentinize uygundur.",

    "travel_duration": "Planladığınız tatil süresi için uygun bir destinasyondur.",
}

def build_score_result(
    criterion: str,
    score: float,
    max_score: float,
    reason: Optional[str] = None,
    active: bool = True
) -> ScoreResult:
    return {
        "criterion": criterion,
        "score": score,
        "max_score": max_score,
        "reason": reason,
        "active": active,
    }
    
def get_cost_segment(cost_index: float, low_threshold: float, high_threshold: float) -> str:
    if cost_index <= low_threshold:
        return "Low Cost"

    if cost_index >= high_threshold:
        return "High Cost"

    return "Mid Cost"


def calculate_budget_score(
    user_budget: str,
    city_budget: Optional[str],
    cost_index: Optional[float] = None,
    low_cost_threshold: Optional[float] = None,
    high_cost_threshold: Optional[float] = None
) -> ScoreResult:
    criterion = "budget"

    if user_budget == NO_PREFERENCE:
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )

    total_score = 0
    active_max_score = 0

    if city_budget is not None:
        budget_level_score = BUDGET_LEVEL_MATRIX[user_budget][city_budget]
        total_score += budget_level_score
        active_max_score += 12

    if (
        cost_index is not None
        and low_cost_threshold is not None
        and high_cost_threshold is not None
    ):
        cost_segment = get_cost_segment(
            cost_index=cost_index,
            low_threshold=low_cost_threshold,
            high_threshold=high_cost_threshold
        )
        cost_index_score = COST_INDEX_MATRIX[user_budget][cost_segment]
        total_score += cost_index_score
        active_max_score += 8

    if active_max_score == 0:
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )

    return build_score_result(
        criterion=criterion,
        score=round(total_score, 2),
        max_score=active_max_score,
        reason=REASON_TEMPLATES[criterion],
        active=True
    )



def calculate_travel_season_score(
    user_season: str,
    best_time_to_visit: Optional[str]
) -> ScoreResult:
    criterion = "travel_season"

    if user_season == NO_PREFERENCE:
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )

    if best_time_to_visit is None:
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )

    season_keyword = SEASON_KEYWORDS[user_season]

    if season_keyword.lower() in str(best_time_to_visit).lower():
        score = 15
    else:
        score = 0

    return build_score_result(
        criterion=criterion,
        score=score,
        max_score=15,
        reason=REASON_TEMPLATES[criterion],
        active=True
    )
    
    
def get_climate_segment(seasonal_avg_temp: float) -> str:
    if seasonal_avg_temp <= 15:
        return "cool"

    if seasonal_avg_temp >= 25:
        return "hot"

    return "mild"


def calculate_climate_score(
    user_climate: str,
    seasonal_avg_temp: Optional[float]
) -> ScoreResult:
    criterion = "climate"

    if user_climate == NO_PREFERENCE:
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )

    if seasonal_avg_temp is None:
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )

    climate_segment = get_climate_segment(seasonal_avg_temp)
    score = CLIMATE_SCORE_MATRIX[user_climate][climate_segment]

    return build_score_result(
        criterion=criterion,
        score=score,
        max_score=15,
        reason=REASON_TEMPLATES[criterion],
        active=True
    )



def calculate_travel_style_score(
    user_style: str,
    city_features: Dict[str, Optional[float]]
) -> ScoreResult:
    criterion = "travel_style"

    if user_style == NO_PREFERENCE:
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )

    style_features = TRAVEL_STYLE_MAPPING[user_style]

    total_score = 0
    active_max_score = 0

    for feature_name, feature_weight in style_features.items():
        feature_value = city_features.get(feature_name)

        if feature_value is None:
            continue

        feature_score = (feature_value / MAX_FEATURE_VALUE) * feature_weight

        total_score += feature_score
        active_max_score += feature_weight

    if active_max_score == 0:
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )

    return build_score_result(
        criterion=criterion,
        score=round(total_score, 2),
        max_score=active_max_score,
        reason=REASON_TEMPLATES[criterion],
        active=True
    )



def calculate_preference_score(
    criterion: str,
    user_importance: str,
    feature_value: Optional[float],
    max_score: float
) -> ScoreResult:
    reason = REASON_TEMPLATES[criterion]

    if user_importance == NO_PREFERENCE:
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )

    if feature_value is None:
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )
        
    feature_value = pd.to_numeric(feature_value, errors="coerce")

    if pd.isna(feature_value):
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )

    normalized_feature = feature_value / MAX_FEATURE_VALUE
    multiplier = IMPORTANCE_MULTIPLIERS[user_importance]
    score = round(normalized_feature * multiplier * max_score,2)

    return build_score_result(
        criterion=criterion,
        score=score,
        max_score=max_score,
        reason=reason,
        active=True
    )


def calculate_duration_score(
    user_duration: str,
    city_duration_category: Optional[str]
) -> ScoreResult:
    criterion = "travel_duration"

    if user_duration == NO_PREFERENCE:
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )

    if city_duration_category is None:
        return build_score_result(
            criterion=criterion,
            score=0,
            max_score=0,
            reason=None,
            active=False
        )

    score = DURATION_MATRIX[user_duration][city_duration_category]
    reason = REASON_TEMPLATES[criterion]

    return build_score_result(
        criterion=criterion,
        score=score,
        max_score=5,
        reason=reason,
        active=True
    )