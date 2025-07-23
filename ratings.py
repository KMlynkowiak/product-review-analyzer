# ratings.py
import pandas as pd
import numpy as np

# Średnia ocen z kolumny 'reviews.rating'
def calculate_mean_rating(df):
    if 'reviews.rating' in df.columns:
        numeric_ratings = pd.to_numeric(df['reviews.rating'], errors='coerce')
        if numeric_ratings.notna().sum() > 0:
            return round(numeric_ratings.mean(), 2)
    return None

# Alternatywa: ocenianie na podstawie sentymentu
def estimate_rating_from_sentiment(df):
    # Zakładamy: -1 → 1 gwiazdka, 0 → 3, +1 → 5
    ratings = (df['sentiment_score'] + 1) * 2 + 1
    return round(ratings.mean(), 2)
