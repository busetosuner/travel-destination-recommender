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

QUESTIONS = [
    {
        "key": "has_visa",
        "question": "Geçerli bir Schengen vizeniz veya giriş hakkı sağlayan geçerli bir vizeniz var mı?",
        "options": [YES_OPTION, NO_OPTION],
        "type": "yes_no",
    },
    {
        "key": "budget",
        "question": "Tatiliniz için ayırdığınız bütçe nedir?",
        "options": BUDGET_OPTIONS,
    },
    {
        "key": "travel_season",
        "question": "Hangi dönemde seyahat etmeyi planlıyorsunuz?",
        "options": SEASON_OPTIONS,
    },
    {
        "key": "climate",
        "question": "Nasıl bir hava tercih edersiniz?",
        "options": CLIMATE_OPTIONS,
    },
    {
        "key": "travel_style",
        "question": "Size en uygun tatil tarzı hangisidir?",
        "options": TRAVEL_STYLE_OPTIONS,
    },
    {
        "key": "travel_duration",
        "question": "Kaç günlük bir tatil planlıyorsunuz?",
        "options": DURATION_OPTIONS,
    },
    {
        "key": "beaches",
        "question": "Deniz tatili sizin için ne kadar önemli?",
        "options": IMPORTANCE_OPTIONS,
    },
    {
        "key": "culture",
        "question": "Tarihi ve kültürel geziler sizin için ne kadar önemli?",
        "options": IMPORTANCE_OPTIONS,
    },
    {
        "key": "nature",
        "question": "Doğa ile iç içe olmak sizin için ne kadar önemli?",
        "options": IMPORTANCE_OPTIONS,
    },
    {
        "key": "cuisine",
        "question": "Yerel yemekleri deneyimlemek sizin için ne kadar önemli?",
        "options": IMPORTANCE_OPTIONS,
    },
    {
        "key": "nightlife",
        "question": "Gece hayatı sizin için ne kadar önemli?",
        "options": IMPORTANCE_OPTIONS,
    },
    {
        "key": "safety",
        "question": "Güvenlik sizin için ne kadar önemli?",
        "options": IMPORTANCE_OPTIONS,
    },
    {
        "key": "urban",
        "question": "Canlı ve hareketli şehir ortamı sizin için ne kadar önemli?",
        "options": IMPORTANCE_OPTIONS,
    },
    {
        "key": "seclusion",
        "question": "Sakin ve kalabalıktan uzak ortam sizin için ne kadar önemli?",
        "options": IMPORTANCE_OPTIONS,
    },
    {
        "key": "adventure",
        "question": "Macera ve açık hava aktiviteleri sizin için ne kadar önemli?",
        "options": IMPORTANCE_OPTIONS,
    },
]