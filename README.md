# 🌍 AI Travel Destination Recommendation System

An AI-powered travel destination recommendation system developed as a Master's Graduation Project.

The application analyzes users' travel preferences and recommends the most suitable European destinations using a weighted recommendation algorithm and personalized scoring model in Turkish.

---

## ✨ Features

- 🧳 Interactive travel preference questionnaire
- 🤖 Personalized destination recommendation engine
- 🎯 Weighted scoring algorithm
- 🚫 Hard constraint filtering (e.g., visa requirement)
- 📊 Compatibility score for each recommendation
- 💬 Explainable recommendations ("Why this destination?")
- 👤 Personalized travel profile summary
- 🖼️ Dynamic destination images using the Pexels API
- 🌍 Modern Streamlit user interface
- ⚡ Interactive recommendation loading animation

---

## 🛠️ Technologies

- Python
- Streamlit
- Pandas
- NumPy
- Pexels API
- Requests

---

## 📂 Project Structure

```
travel-destination-recommender/
│
├── app.py
├── assets/
├── data/
├── src/
│   ├── recommendation_engine.py
│   ├── scoring.py
│   ├── preprocessing.py
│   ├── ui_questions.py
│   ├── constants.py
│   └── ...
│
└── requirements.txt
```

---

## ⚙️ Recommendation Process

The recommendation engine follows four main steps:

1. Collect user travel preferences.
2. Apply hard constraints (e.g., visa availability).
3. Calculate weighted compatibility scores for every destination.
4. Recommend the Top 5 destinations with explanations.

---

## 📸 Screenshots

> Screenshots of the application will be added here.

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/travel-destination-recommender.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 🎓 Academic Purpose

This project was developed as part of a Master's Graduation Project in Artificial Intelligence and Recommendation Systems. 

---

## 👨‍💻 Author

**Buse Tosuner**

Master's Student – Information Systems & Technology Management

Istanbul Technical University
