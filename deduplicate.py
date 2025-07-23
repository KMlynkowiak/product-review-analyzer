# deduplicate.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def remove_duplicates(df, text_column='clean_text', threshold=0.9):
    vectorizer = TfidfVectorizer().fit_transform(df[text_column])
    vectors = vectorizer.toarray()
    sim_matrix = cosine_similarity(vectors)

    to_remove = set()

    for i in range(len(sim_matrix)):
        for j in range(i + 1, len(sim_matrix)):
            if sim_matrix[i][j] > threshold:
                to_remove.add(j)

    df_dedup = df.drop(df.index[list(to_remove)]).reset_index(drop=True)
    print(f"Usunięto {len(to_remove)} duplikatów (próg: {threshold})")
    return df_dedup
