# wordcloud_utils.py

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

def generate_wordcloud(text, product_name, output_dir="wordclouds"):
    os.makedirs(output_dir, exist_ok=True)
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    output_path = os.path.join(output_dir, f"{product_name[:50].replace(' ', '_')}.png")
    wc.to_file(output_path)
    return output_path
