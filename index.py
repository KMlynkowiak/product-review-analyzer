import requests
import pandas as pd
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Twój klucz API
api_key = 'e638c28875b9437383fdf00768c5fb51'  

# Adres URL API 
competition_id = '2000'  
url = f'https://api.football-data.org/v4/competitions/{competition_id}/matches'

# Nagłówki z kluczem API
headers = {
    'X-Auth-Token': api_key
}

# Wysyłanie zapytania GET
response = requests.get(url, headers=headers)

# Sprawdzenie statusu odpowiedzi
if response.status_code == 200:
    data = response.json()  
    print("Dane o meczach pobrane pomyślnie")

    # Wyciąganie interesujących danych o meczach
    matches = data['matches']  # Lista meczów
    matches_data = []
    
    # Dodanie nazwy turnieju oraz ID turnieju
    competition_name = data['competition']['name']
    competition_id = data['competition']['id']

    for match in matches:
        try:
            home_score = match['score']['fullTime'].get('homeTeam', 'Mecz jeszcze się nie odbył')
            away_score = match['score']['fullTime'].get('awayTeam', 'Mecz jeszcze się nie odbył')
        except KeyError:
            home_score, away_score = 'Mecz jeszcze się nie odbył', 'Mecz jeszcze się nie odbył'

        # Przekształcenie daty na format YYYY MM DD
        iso_date = match['utcDate']
        date_obj = datetime.fromisoformat(iso_date.replace("Z", "+00:00")) 
        formatted_date = date_obj.strftime("%Y %m %d")

        # Wyciągnięcie zwycięzcy
        winner = match['score']['winner']
        if winner == 'HOME_TEAM':
            winner_team = match['homeTeam']['name']
        elif winner == 'AWAY_TEAM':
            winner_team = match['awayTeam']['name']
        else:
            winner_team = 'Remis'

        matches_data.append({
            'home_team': match['homeTeam']['name'],
            'away_team': match['awayTeam']['name'],
            'date': formatted_date,  # Zmieniona data na format YYYY MM DD
            'winner': winner_team  # Zwycięzca spotkania
        })

    # Tworzenie DataFrame
    df = pd.DataFrame(matches_data)

    # Wyświetlanie danych
    print(df)

    # Zapis danych do SQLite
    conn = sqlite3.connect('football_data.db')
    df.to_sql('matches', conn, if_exists='replace', index=False)
    conn.close()

    print("Dane o meczach zapisane do bazy SQLite.")

    # Ile razy wygral poszczegolny kraj
    df_no_draws = df[df['winner'] != 'Remis']
    winner_counts = df_no_draws['winner'].value_counts()

    print("\nLiczba wygranych drużyn (bez remisów):")
    print(winner_counts)

    # Najwięcej zwycięstw 
    if not winner_counts.empty:
        top_winner = winner_counts.idxmax()
        top_wins = winner_counts.max()
        print(f"\nZwycięzca turnieju (najwięcej wygranych meczy, bez remisów): {top_winner} z liczbą {top_wins} zwycięstw.")

        # TOP 3 drużyny
        top_3 = winner_counts.head(3)
        print("\nTOP 3 drużyny (bez remisów):")
        for i, (team, wins) in enumerate(top_3.items(), start=1):
            print(f"{i}. {team}: {wins} zwycięstw")
    else:
        print("\nBrak danych o zwycięzcach (wszystko to remisy).")

    # Wykres wygranych
    plt.figure(figsize=(10,6))
    winner_counts.plot(kind='bar', color='skyblue')

    plt.title('Liczba wygranych meczy przez drużyny (bez remisów)')
    plt.xlabel('Drużyna')
    plt.ylabel('Liczba wygranych meczy')

    # Skala co 1 
    ax = plt.gca()
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

else:
    print(f"Błąd pobierania danych o meczach. Kod odpowiedzi: {response.status_code}")
