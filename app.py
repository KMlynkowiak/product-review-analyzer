# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter
import os

# ładowanie danych
@st.cache_data
def load_data():
    return pd.read_csv("output_preview.csv")

df = load_data()

st.title("📦 Podsumowanie opinii o produkcie")

product_input = st.text_input("Wpisz nazwę produktu:", "")
if st.button("OK") and product_input.strip() != "":
    # Filtruj opinie po nazwie (częściowe dopasowanie)
    matches = df[df['name'].str.contains(product_input, case=False, na=False)]

    if matches.empty:
        st.warning("Brak opinii dla podanej nazwy produktu.")
    else:
        st.success(f"Znaleziono {len(matches)} opinii")

        # Średnia ocena
        rating = matches['reviews.rating'].dropna().mean()
        if pd.isna(rating):
            rating = (matches['sentiment_score'] + 1) * 2 + 1
            rating = rating.mean()
        st.markdown(f"### ⭐ Średnia ocena: {round(rating, 2)}/5")

        # Sentiment zbiorczy
        sentiment = matches['sentiment'].value_counts().idxmax()
        st.markdown(f"### 😊 Dominujący sentyment: **{sentiment}**")

        # Najczęstsze słowa
        all_words = " ".join(matches['clean_text']).split()
        common_words = Counter(all_words).most_common(5)
        top_words = ", ".join([word for word, _ in common_words])
        st.markdown(f"### 🔤 Najczęstsze słowa: {top_words}")

        # Skrócone opinie
        st.markdown("### ✍️ Przykładowe opinie:")
        for txt in matches['translated_text'].head(3):
            st.write(f"- {txt.strip()}")

        # WordCloud
        wc_path = None
        for file in os.listdir("wordclouds"):
            if product_input.lower()[:5] in file.lower():
                wc_path = os.path.join("wordclouds", file)
                break

        if wc_path and os.path.exists(wc_path):
            st.markdown("### ☁️ WordCloud:")
            image = Image.open(wc_path)
            st.image(image, use_column_width=True)
        else:
            st.info("Brak WordClouda dla tego produktu.")
