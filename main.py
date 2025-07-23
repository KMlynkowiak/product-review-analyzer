# main.py

import os
import zipfile
import subprocess
import glob
import pandas as pd
from cleaning import clean_opinion
from language_utils import detect_language, translate_to_english
from deduplicate import remove_duplicates
from sentiment import get_sentiment, get_sentiment_score
from ratings import calculate_mean_rating, estimate_rating_from_sentiment
from wordcloud_utils import generate_wordcloud





# Ścieżka do pliku kaggle.json
os.environ['KAGGLE_CONFIG_DIR'] = r'C:\Users\Kacpe\kaggle'

# Pobranie danych (jeśli nie masz jeszcze pliku ZIP)
subprocess.run(["kaggle", "datasets", "download", "-d", "datafiniti/consumer-reviews-of-amazon-products"])

# Wypakowanie pliku ZIP
with zipfile.ZipFile('consumer-reviews-of-amazon-products.zip', 'r') as zip_ref:
    zip_ref.extractall('amazon_reviews')

# Znalezienie pliku CSV
csv_files = glob.glob('amazon_reviews/*.csv')
print("Znalezione pliki CSV:", csv_files)

# Wczytanie pierwszego pliku
csv_path = csv_files[0]
df = pd.read_csv(csv_path, low_memory=False)
df = df.dropna(subset=["reviews.text"])

# Ograniczenie do 500 recenzji bo ładowało się pół godziny 
df = df.sample(500, random_state=42).reset_index(drop=True)  

# Wykrywanie języków
print("Wykrywanie języków...")
df['language'] = df['reviews.text'].apply(detect_language)

# Tłumaczenie na angielski (tylko gdy inny język niż PL/EN)
print("Tłumaczenie obcych języków...")
df['translated_text'] = df.apply(
    lambda row: row['reviews.text'] if row['language'] in ['en', 'pl']
    else translate_to_english(row['reviews.text']),
    axis=1
)

# Czyszczenie tekstu (stopwords + lematyzacja)
print("Czyszczenie opinii...")
df['clean_text'] = df['translated_text'].apply(clean_opinion)

# Usuwanie duplikatów (opinie bardzo podobne)
print("Usuwanie duplikatów...")
df = remove_duplicates(df)

# Analiza sentymentu
print("Analiza sentymentu...")
df['sentiment'] = df['translated_text'].apply(get_sentiment)
df['sentiment_score'] = df['translated_text'].apply(get_sentiment_score)
print("Liczenie średniej oceny...")

avg_rating = calculate_mean_rating(df)
if avg_rating is None:
    avg_rating = estimate_rating_from_sentiment(df)

print(f"📊 Średnia ocena: {avg_rating}/5")



# Przykład
print(df[['translated_text', 'sentiment', 'sentiment_score']].sample(5, random_state=42))


# Przykładowy podgląd
print(df[['reviews.text', 'language', 'translated_text', 'clean_text']].sample(5, random_state=42))

# WordCloud dla najpopularniejszego produktu
print("Generowanie WordCloud...")

most_common_product = df['name'].value_counts().idxmax()
text_for_wordcloud = " ".join(df[df['name'] == most_common_product]['clean_text'])

path = generate_wordcloud(text_for_wordcloud, most_common_product)
print(f"📸 WordCloud zapisany: {path}")

# Zapis do pliku CSV (dla Streamlit)
df.to_csv("output_preview.csv", index=False)
print("📄 Zapisano dane do output_preview.csv – gotowe do użycia w Streamlit.")
