# cleaning.py

import nltk
import spacy
from nltk.corpus import stopwords
import re

# Ładowanie zasobów 
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm")

# Funkcja czyszcząca tekst opinii
def clean_opinion(text):
    if not isinstance(text, str):
        return ""
    # Małe litery i usunięcie znaków specjalnych
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    # Usuwanie stopwords
    tokens = [word for word in text.split() if word not in stop_words]
    # Lematyzacja
    doc = nlp(" ".join(tokens))
    lemmatized = [token.lemma_ for token in doc]
    return " ".join(lemmatized)
