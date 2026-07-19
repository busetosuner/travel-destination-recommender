import time

import pandas as pd

from src.data_preprocessing import prepare_dataset_for_recommendation
from src.recommendation_engine import generate_recommendations
from src.terminal_ui import collect_user_answers


def get_sample_user_answers() -> dict:
    """Temporary sample answers for debugging."""
    return {
        "has_visa": True,
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
        "adventure": "Fark etmez",
    }


def show_loading_messages() -> None:
    print("\nCevaplarınız analiz ediliyor...")
    time.sleep(0.7)
    print("Size en uygun destinasyonlar hesaplanıyor...")
    time.sleep(0.7)


def print_recommendations(recommendations: list) -> None:
    print("\nTOP RECOMMENDATIONS\n")

    for index, rec in enumerate(recommendations, start=1):
        print("=" * 60)
        print(f"{index}. {rec['city']}, {rec['country']}")
        print(f"Compatibility Score: {rec['compatibility_score']}%")
        print(f"Total Score: {rec['total_score']} / {rec['active_max_score']}")
        print("\nCriterion Scores:")

        for criterion, result in rec["criterion_results"].items():
            if result["active"]:
                print(f"  - {criterion}: {result['score']} / {result['max_score']}")

        top_reasons = sorted(
            [
                result
                for result in rec["criterion_results"].values()
                if result["active"] and result["reason"] is not None
            ],
            key=lambda result: result["score"],
            reverse=True,
        )[:5]

        print("\nWhy recommended:")
        for reason_result in top_reasons:
            print(f"  ✓ {reason_result['reason']}")

    print("=" * 60)


def main():
    master_dataset = pd.read_csv("data/processed/master_dataset_v1.csv")
    country_reference = pd.read_excel("data/reference/country_reference_data.xlsx")

    # user_answers = get_sample_user_answers()
    user_answers = collect_user_answers()

    prepared_dataset = prepare_dataset_for_recommendation(
        master_dataset=master_dataset,
        country_reference=country_reference,
        user_season=user_answers["travel_season"],
    )

    show_loading_messages()

    recommendations = generate_recommendations(
        user_answers=user_answers,
        master_dataset=prepared_dataset,
        top_n=5,
    )

    print_recommendations(recommendations)


if __name__ == "__main__":
    main()