"""
Terminal UI for Travel Recommendation System.

This module collects user answers from the terminal
and returns them in the standard user_answers format.
"""

from typing import Optional

from src.constants import (
    YES_OPTION,
    NO_OPTION,
    IMPORTANCE_OPTIONS,
    BUDGET_OPTIONS,
    SEASON_OPTIONS,
    CLIMATE_OPTIONS,
    TRAVEL_STYLE_OPTIONS,
    DURATION_OPTIONS,
)


def ask_choice(
    question: str,
    options: list[str],
    step: Optional[int] = None,
    total_steps: Optional[int] = None
) -> str:
    if step is not None and total_steps is not None:
        print(f"\n[{step}/{total_steps}]")

    print("\n" + question)

    for index, option in enumerate(options, start=1):
        print(f"{index}) {option}")

    while True:
        choice = input("Seçiminiz: ").strip()

        if choice.isdigit():
            choice_index = int(choice)

            if 1 <= choice_index <= len(options):
                return options[choice_index - 1]

        print("Lütfen geçerli bir seçenek numarası giriniz.")


def collect_user_answers() -> dict:
    print("=" * 60)
    print("🌍 Travel Destination Recommendation System")
    print("=" * 60)

    name = input("\nLütfen isminizi giriniz: ").strip()

    while not name:
        print("İsim alanı boş bırakılamaz.")
        name = input("Lütfen isminizi giriniz: ").strip()

    print(f"\nMerhaba {name}! 👋")
    print("Sana en uygun Avrupa destinasyonlarını bulmak için birkaç kısa soru soracağım.")
    print("Emin olmadığın sorularda 'Fark etmez' seçeneğini kullanabilirsin.")

    questions = [
        {
            "key": "has_visa",
            "question": "Geçerli bir Schengen vizeniz veya giriş hakkı sağlayan geçerli bir vizeniz var mı?",
            "options": [YES_OPTION, NO_OPTION],
            "type": "yes_no"
        },
        {
            "key": "budget",
            "question": "Tatiliniz için ayırdığınız bütçe nedir?",
            "options": BUDGET_OPTIONS
        },
        {
            "key": "travel_season",
            "question": "Hangi dönemde seyahat etmeyi planlıyorsunuz?",
            "options": SEASON_OPTIONS
        },
        {
            "key": "climate",
            "question": "Nasıl bir hava tercih edersiniz?",
            "options": CLIMATE_OPTIONS
        },
        {
            "key": "travel_style",
            "question": "Size en uygun tatil tarzı hangisidir?",
            "options": TRAVEL_STYLE_OPTIONS
        },
        {
            "key": "travel_duration",
            "question": "Kaç günlük bir tatil planlıyorsunuz?",
            "options": DURATION_OPTIONS
        },
        {
            "key": "beaches",
            "question": "Deniz tatili sizin için ne kadar önemli?",
            "options": IMPORTANCE_OPTIONS
        },
        {
            "key": "culture",
            "question": "Tarihi ve kültürel geziler sizin için ne kadar önemli?",
            "options": IMPORTANCE_OPTIONS
        },
        {
            "key": "nature",
            "question": "Doğa ile iç içe olmak sizin için ne kadar önemli?",
            "options": IMPORTANCE_OPTIONS
        },
        {
            "key": "cuisine",
            "question": "Yerel yemekleri deneyimlemek sizin için ne kadar önemli?",
            "options": IMPORTANCE_OPTIONS
        },
        {
            "key": "nightlife",
            "question": "Gece hayatı sizin için ne kadar önemli?",
            "options": IMPORTANCE_OPTIONS
        },
        {
            "key": "safety",
            "question": "Güvenlik sizin için ne kadar önemli?",
            "options": IMPORTANCE_OPTIONS
        },
        {
            "key": "urban",
            "question": "Canlı ve hareketli şehir ortamı sizin için ne kadar önemli?",
            "options": IMPORTANCE_OPTIONS
        },
        {
            "key": "seclusion",
            "question": "Sakin ve kalabalıktan uzak ortam sizin için ne kadar önemli?",
            "options": IMPORTANCE_OPTIONS
        },
        {
            "key": "adventure",
            "question": "Macera ve açık hava aktiviteleri sizin için ne kadar önemli?",
            "options": IMPORTANCE_OPTIONS
        },
    ]

    user_answers = {}
    total_steps = len(questions)

    for step, item in enumerate(questions, start=1):
        answer = ask_choice(
            question=item["question"],
            options=item["options"],
            step=step,
            total_steps=total_steps
        )

        if item.get("type") == "yes_no":
            user_answers[item["key"]] = answer == YES_OPTION
        else:
            user_answers[item["key"]] = answer

    return user_answers