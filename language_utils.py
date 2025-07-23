# language_utils.py

from langdetect import detect
from deep_translator import GoogleTranslator

# Wykrywanie języka
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

# Tłumaczenie tekstu na angielski
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text  # jeśli nie da się przetłumaczyć
