from operator import index
import time
from numpy import rec
import pandas as pd
import streamlit as st
import base64
from src.image_service import get_city_image
from src.flag_utils import get_country_flag
from pathlib import Path
import random
import time
import requests

from src.constants import YES_OPTION
from src.ui_questions import QUESTIONS
from src.data_preprocessing import prepare_dataset_for_recommendation
from src.recommendation_engine import generate_recommendations

FALLBACK_IMAGE_PATH = Path("assets/background.png")


def load_css():
    with open("assets/background.png", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    with open("assets/style.css") as f:
        css = f.read()

    css = css.replace(
        "BACKGROUND_IMAGE",
        f"data:image/png;base64,{encoded_image}"
    )

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )
    
    

def initialize_state():
    if "started" not in st.session_state:
        st.session_state.started = False
    if "current_step" not in st.session_state:
        st.session_state.current_step = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "show_results" not in st.session_state:
        st.session_state.show_results = False
    if "loading_results" not in st.session_state:
        st.session_state.loading_results = False
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None


@st.cache_data
def load_data():
    master_dataset = pd.read_csv("data/processed/master_dataset_v1.csv")
    country_reference = pd.read_excel("data/reference/country_reference_data.xlsx")
    return master_dataset, country_reference


def show_welcome():
    st.markdown(
        """
        <div class="glass-card">
            <h1>🌍 Akıllı Seyahat<br>Öneri Sistemi</h1>
            <p>
                Avrupa'daki size en uygun destinasyonu<br>
                yapay zeka destekli öneri sistemi ile keşfedin.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("Başlamaya Hazır Mısınız? 🚀", use_container_width=True):
        st.session_state.started = True
        st.rerun()

def show_question():
    current_step = st.session_state.current_step
    total_steps = len(QUESTIONS)
    question_item = QUESTIONS[current_step]

    st.markdown('<div class="question-page-title">✈️ Seyahat Tercihlerinizi Belirleyelim</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.progress((current_step + 1) / total_steps)
        st.caption(f"Adım {current_step + 1} / {total_steps}")

        st.subheader(question_item["question"])

        previous_answer = st.session_state.answers.get(question_item["key"])
        options = question_item["options"]

        if previous_answer in options:
            index = options.index(previous_answer)
        else:
            index = None

        answer = st.radio(
            "Seçiminiz:",
            options,
            index=index,
            key=f"question_{current_step}"
        )

        col1, col2 = st.columns(2)

        with col1:
            if current_step > 0:
                if st.button("← Geri", use_container_width=True):
                    st.session_state.current_step -= 1
                    st.rerun()

        with col2:
            button_label = "Sonuçları Göster ✨" if current_step == total_steps - 1 else "Devam Et →"

            if st.button(button_label, use_container_width=True):
                if answer is None:
                    st.warning("Lütfen bir seçim yapınız.")
                    return

                if question_item.get("type") == "yes_no":
                    st.session_state.answers[question_item["key"]] = answer == YES_OPTION
                else:
                    st.session_state.answers[question_item["key"]] = answer

                if current_step == total_steps - 1:
                    st.session_state.loading_results = True
                else:
                    st.session_state.current_step += 1

                st.rerun()

def get_top_reasons(recommendation, limit=5):
    reasons = sorted(
        [
            result
            for result in recommendation["criterion_results"].values()
            if result["active"] and result["reason"] is not None
        ],
        key=lambda result: result["score"],
        reverse=True
    )

    return reasons[:limit]

@st.cache_data(show_spinner=False)
def download_image(image_url):
    """
    Görseli URL üzerinden indirerek Streamlit'e doğrudan
    gösterilebilecek byte verisine dönüştürür.
    """
    if not image_url:
        return None

    try:
        response = requests.get(
            image_url,
            timeout=8
        )
        response.raise_for_status()
        return response.content

    except requests.RequestException:
        return None


def show_loading():
    st.markdown(
        """
        <h1 style="text-align: center;">
            🔍 Tercihleriniz Analiz Ediliyor
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            text-align: center;
            font-size: 18px;
            margin-bottom: 20px;
        ">
            Yüzlerce destinasyon arasından size en uygun seçenekler
            değerlendiriliyor.
        </p>
        """,
        unsafe_allow_html=True
    )

    image_placeholder = st.empty()
    city_placeholder = st.empty()
    message_placeholder = st.empty()
    progress_bar = st.progress(0)

    loading_cities = [
        {
            "city": "Barcelona",
            "country": "Spain",
            "display_city": "Barselona",
            "display_country": "İspanya",
        },
        {
            "city": "Prague",
            "country": "Czech Republic",
            "display_city": "Prag",
            "display_country": "Çekya",
        },
        {
            "city": "Porto",
            "country": "Portugal",
            "display_city": "Porto",
            "display_country": "Portekiz",
        },
        {
            "city": "Vienna",
            "country": "Austria",
            "display_city": "Viyana",
            "display_country": "Avusturya",
        },
        {
            "city": "Dubrovnik",
            "country": "Croatia",
            "display_city": "Dubrovnik",
            "display_country": "Hırvatistan",
        },
        {
            "city": "Santorini",
            "country": "Greece",
            "display_city": "Santorini",
            "display_country": "Yunanistan",
        },
    ]

    analysis_messages = [
        "📝 Seyahat tercihleriniz yorumlanıyor...",
        "🌍 Destinasyon havuzu taranıyor...",
        "🌤️ İklim ve seyahat dönemi karşılaştırılıyor...",
        "💰 Bütçe uyumluluğu hesaplanıyor...",
        "🎯 Tatil tarzınıza uygun seçenekler belirleniyor...",
        "🧠 En güçlü destinasyonlar sıralanıyor...",
    ]

    random.shuffle(loading_cities)

    # Görselleri animasyon başlamadan önce indir
    prepared_cities = []

    for city_data in loading_cities:
        image_url = get_city_image(
            city_data["city"],
            city_data["country"]
        )

        image_bytes = download_image(image_url)

        prepared_cities.append(
            {
                **city_data,
                "image_bytes": image_bytes,
            }
        )

    total_cities = len(prepared_cities)

    for index, city_data in enumerate(prepared_cities):
        image_bytes = city_data["image_bytes"]

        if image_bytes:
            image_placeholder.image(
                image_bytes,
                use_container_width=True
            )

        elif FALLBACK_IMAGE_PATH.exists():
            image_placeholder.image(
                str(FALLBACK_IMAGE_PATH),
                use_container_width=True
            )

        else:
            image_placeholder.info(
                "Destinasyon görseli hazırlanıyor..."
            )

        city_placeholder.markdown(
            f"""
            <h2 style="
                text-align: center;
                margin-top: 8px;
                margin-bottom: 4px;
            ">
                📍 {city_data["display_city"]},
                {city_data["display_country"]}
            </h2>
            """,
            unsafe_allow_html=True
        )

        current_message = analysis_messages[
            index % len(analysis_messages)
        ]

        message_placeholder.markdown(
            f"""
            <p style="
                text-align: center;
                font-size: 18px;
                margin-top: 4px;
            ">
                {current_message}
            </p>
            """,
            unsafe_allow_html=True
        )

        progress = int(
            ((index + 1) / total_cities) * 100
        )

        progress_bar.progress(progress)

        # Fotoğrafın kullanıcı tarafından görülebilmesi için
        # 0.35 saniyeden biraz daha uzun tutuyoruz.
        time.sleep(0.7)

    message_placeholder.markdown(
        """
        <h3 style="text-align: center;">
            ✨ Size özel öneriler hazır!
        </h3>
        """,
        unsafe_allow_html=True
    )

    time.sleep(0.7)

    st.session_state.loading_results = False
    st.session_state.show_results = True

    st.rerun()
    
    
    
def show_preference_profile():
    answers = st.session_state.answers
    profile = []

    # 1. Bütçe tercihi
    budget = answers.get("budget")

    budget_sentences = {
        "Düşük": (
            "💰 Ekonomik ve bütçe dostu destinasyonlar "
            "sizin için ön planda."
        ),
        "Orta": (
            "💳 Fiyat ve deneyim arasında dengeli seçenekleri "
            "tercih ediyorsunuz."
        ),
        "Yüksek": (
            "💎 Konfor ve deneyim kalitesini ön planda "
            "tutuyorsunuz."
        ),
    }

    if budget in budget_sentences:
        profile.append(budget_sentences[budget])

    # 2. Seyahat dönemi ve hava tercihi
    season = answers.get("travel_season")
    climate = answers.get("climate")

    season_labels = {
        "İlkbahar": "ilkbahar döneminde",
        "Yaz": "yaz döneminde",
        "Sonbahar": "sonbahar döneminde",
        "Kış": "kış döneminde",
    }

    climate_labels = {
        "Serin": "serin",
        "Ilık": "ılıman",
        "Sıcak": "sıcak",
    }

    season_text = season_labels.get(season)
    climate_text = climate_labels.get(climate)

    if season_text and climate_text:
        profile.append(
            f"🌤️ {season_text.capitalize()} {climate_text} hava "
            "koşullarında seyahat etmeyi tercih ediyorsunuz."
        )
    elif season_text:
        profile.append(
            f"🗓️ {season_text.capitalize()} seyahat etmeyi "
            "planlıyorsunuz."
        )
    elif climate_text:
        profile.append(
            f"🌡️ {climate_text.capitalize()} hava koşullarını "
            "tercih ediyorsunuz."
        )

    # 3. Genel tatil tarzı
    travel_style = answers.get("travel_style")

    style_sentences = {
        "Deniz & Relax": (
            "🏖️ Deniz, güneş ve dinlenme odaklı tatillerden "
            "hoşlanıyorsunuz."
        ),
        "Kültürel Gezi": (
            "🏛️ Tarihi ve kültürel destinasyonları keşfetmekten "
            "hoşlanıyorsunuz."
        ),
        "Doğa & Macera": (
            "🌲 Doğa ve macera odaklı deneyimler ilginizi çekiyor."
        ),
        "Şehir & Eğlence": (
            "🌆 Hareketli şehir yaşamı ve eğlence seçenekleri "
            "seyahat tarzınıza uyuyor."
        ),
    }

    if travel_style in style_sentences:
        profile.append(style_sentences[travel_style])

    # 4. Tatil süresi
    duration = answers.get("travel_duration")

    duration_sentences = {
        "Hafta Sonu Kaçamağı": (
            "🧳 Kısa hafta sonu kaçamaklarını tercih ediyorsunuz."
        ),
        "Kısa Tatil (3–5 Gün)": (
            "✈️ 3–5 günlük kısa tatiller size daha uygun."
        ),
        "Bir Haftalık Tatil": (
            "📅 Yaklaşık bir haftalık tatilleri tercih ediyorsunuz."
        ),
        "Uzun Tatil (10+ Gün)": (
            "🌍 Destinasyonu daha ayrıntılı keşfedebileceğiniz "
            "uzun tatilleri tercih ediyorsunuz."
        ),
    }

    if duration in duration_sentences:
        profile.append(duration_sentences[duration])

    # 5. En önemli ilgi alanlarını tek cümlede birleştir
    interest_labels = {
        "beaches": "deniz",
        "culture": "kültür",
        "nature": "doğa",
        "cuisine": "yerel mutfak",
        "nightlife": "gece hayatı",
        "safety": "güvenlik",
        "urban": "şehir yaşamı",
        "seclusion": "sakinlik",
        "adventure": "macera",
    }

    strong_interests = [
        label
        for key, label in interest_labels.items()
        if answers.get(key) == "Çok önemli"
    ]

    if strong_interests:
        selected_interests = strong_interests[:3]

        if len(selected_interests) == 1:
            interests_text = selected_interests[0]

        elif len(selected_interests) == 2:
            interests_text = (
                f"{selected_interests[0]} ve "
                f"{selected_interests[1]}"
            )

        else:
            interests_text = (
                f"{selected_interests[0]}, "
                f"{selected_interests[1]} ve "
                f"{selected_interests[2]}"
            )

        profile.append(
            f"🎯 Destinasyon seçiminde özellikle {interests_text} "
            "özelliklerine önem veriyorsunuz."
        )

    # Profil başlığı ve açıklaması
    st.markdown("## 👤 Seyahat Profiliniz")

    st.caption(
        "Verdiğiniz cevaplara göre öne çıkan seyahat tercihleriniz:"
    )

    # Kullanıcı tüm alanlarda Fark etmez seçmişse
    if not profile:
        st.markdown(
            "🌍 Belirli bir seyahat tarzıyla kendinizi "
            "sınırlandırmadığınız için farklı destinasyonlara açıksınız."
        )
        return

    # En fazla 5 kısa profil cümlesi göster
    for sentence in profile[:5]:
        st.markdown(f"- {sentence}")
    
def clean_coordinate(value):
    if value is None or pd.isna(value):
        return None

    text = str(value).strip().replace(",", ".")

    # Zaten normal sayıysa doğrudan kullan
    try:
        return float(text)
    except ValueError:
        pass

    # Örnek:
    # 35.308.495.199.999.900 -> 35.308495199999900
    # -9.381.700.000.000.000 -> -9.381700000000000
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

DURATION_VALUE_MAP = {
    "Hafta Sonu Kaçamağı": "Weekend Trip",
    "Kısa Tatil (3–5 Gün)": "Short Trip",
    "Bir Haftalık Tatil": "One Week",
    "Uzun Tatil (10+ Gün)": "Long Vacation",
    "Fark etmez": "Fark etmez",
}


def prepare_answers_for_recommendation(answers: dict) -> dict:
    """
    Kullanıcıya gösterilen Türkçe cevapları, öneri motorunun
    beklediği teknik değerlere dönüştürür.
    """
    normalized_answers = answers.copy()

    selected_duration = normalized_answers.get("travel_duration")

    normalized_answers["travel_duration"] = DURATION_VALUE_MAP.get(
        selected_duration,
        selected_duration
    )

    return normalized_answers



def show_results():
    master_dataset, country_reference = load_data()

    if st.session_state.recommendations is None:
        user_answers_for_engine = prepare_answers_for_recommendation(
            st.session_state.answers
        )

        prepared_dataset = prepare_dataset_for_recommendation(
            master_dataset=master_dataset,
            country_reference=country_reference,
            user_season=st.session_state.answers["travel_season"]
        )

        st.session_state.recommendations = generate_recommendations(
            user_answers=user_answers_for_engine,
            master_dataset=prepared_dataset,
            top_n=5
        )

    recommendations = st.session_state.recommendations
    
    if not recommendations:
        st.warning(
        "Seçtiğiniz tercihlere uygun bir destinasyon bulunamadı. "
        "Bazı tercihlerinizi esneterek tekrar deneyebilirsiniz."
    )

    if st.button(
        "Tercihlerimi Güncelle ↩️",
        use_container_width=True
    ):
        st.session_state.current_step = 0
        st.session_state.answers = {}
        st.session_state.show_results = False
        st.session_state.loading_results = False
        st.session_state.recommendations = None
        st.rerun()

        return

    st.title("🎉 Analiz Tamamlandı!")
    st.write(
        "Tercihlerinize göre yüzlerce destinasyon arasından "
        "sizin için en uygun 5 seçenek belirlendi."
    )

    show_preference_profile()


    
    st.markdown("---")
    st.markdown("## 🌍 Size Özel Destinasyon Önerileri")

    for index, rec in enumerate(recommendations, start=1):
        compatibility_score = int(round(rec["compatibility_score"]))

        if index == 1:
            recommendation_title = "🥇 Size En Uygun Destinasyon"
        else:
            recommendation_title = f"Alternatif Öneri #{index}"

        with st.container(border=True):
            st.markdown(f"### {recommendation_title}")

            image_column, info_column = st.columns([1.15, 1])

            with image_column:
                image_url = get_city_image(
                    rec["city"],
                    rec["country"]
                )

                if image_url:
                    st.image(
                        image_url,
                        use_container_width=True
                    )
                elif FALLBACK_IMAGE_PATH.exists():
                    st.image(
                        str(FALLBACK_IMAGE_PATH),
                        use_container_width=True,
                        caption="Temsili destinasyon görseli"
                    )
                else:
                    st.info("Bu destinasyon için görsel bulunamadı.")

            with info_column:
                st.markdown(
                    f"## {index}. {rec['city']}"
                )
                st.caption(rec["country"])

                st.markdown(
                    f"### ⭐ Uyumluluk Skoru: %{compatibility_score}"
                )
                st.progress(compatibility_score / 100)

            

            st.markdown("#### 🎯 Tercihlerinizle Eşleşen Özellikler")

            top_reasons = get_top_reasons(rec)

            for reason_result in top_reasons:
                st.markdown(
                    f"✓ {reason_result['reason']}"
                )
    

    if st.button(
        "Yeni Bir Analiz Yap 🔄",
        use_container_width=True
    ):
        st.session_state.started = False
        st.session_state.current_step = 0
        st.session_state.answers = {}
        st.session_state.show_results = False
        st.session_state.loading_results = False
        st.session_state.recommendations = None
        st.rerun()
        
        
        
        

def main():
    initialize_state()
    load_css()
    if not st.session_state.started:
        show_welcome()

    elif st.session_state.loading_results:
        show_loading()

    elif st.session_state.show_results:
        show_results()

    else:
        show_question()


if __name__ == "__main__":
    main()