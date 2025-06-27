import csv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
HISTO_FILE = os.path.join(DATA_DIR, 'historique.csv')

# Obtenir le chemin absolu du dossier racine
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# Créer le dossier assets s'il n'existe pas
os.makedirs(ASSETS_DIR, exist_ok=True)



def stats_genres():
    genres = {}

        # Charger tous les livres et compter les genres directement
    with open(os.path.join(DATA_DIR, 'livres.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(';')
            if len(parts) >= 5:
                genre = parts[4]
                genres[genre] = genres.get(genre, 0) + 1

        # Génération du graphique
    if genres:
        plt.figure()
        plt.pie(genres.values(), labels=genres.keys(), autopct='%1.1f%%')
        plt.title("Répartition des livres par genre (tous les livres)")
        plt.tight_layout()
        plt.savefig(os.path.join(ASSETS_DIR, 'stats_genres.png'))
        plt.close()
        print("Graphique généré : stats_genres.png")
    else:
        print("Aucun genre trouvé dans les livres.")


def stats_auteurs():
    auteurs = {}
    livres = {}

    # Charger tous les livres dans un dictionnaire ISBN -> auteur
    with open(os.path.join(DATA_DIR, 'livres.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            isbn, _, auteur, _, _, _ = line.strip().split(';')
            livres[isbn] = auteur

    # Lire l'historique pour compter les emprunts par auteur
    with open(HISTO_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for date, isbn, _, action in reader:
            if action == 'emprunt' and isbn in livres:
                auteur = livres[isbn]
                auteurs[auteur] = auteurs.get(auteur, 0) + 1

    # Génération du graphique
    if auteurs:
        top_auteurs = dict(sorted(auteurs.items(), key=lambda x: x[1], reverse=True)[:10])
        plt.figure()
        plt.bar(top_auteurs.keys(), top_auteurs.values(), color='skyblue')
        plt.xticks(rotation=45)
        plt.title("Top 10 des auteurs les plus empruntés")
        plt.tight_layout()
        plt.savefig(os.path.join(ASSETS_DIR, 'stats_auteurs.png'))
        plt.close()


def stats_activite_emprunts():
    # Courbe temporelle des emprunts sur les 30 derniers jours
    activite = {}
    aujourd_hui = datetime.now().date()
    debut = aujourd_hui - timedelta(days=30)

    with open(HISTO_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if len(row) < 4:
                continue
            date_str, _, _, action = row
            if action != 'emprunt':
                continue
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if debut <= date <= aujourd_hui:
                activite[date] = activite.get(date, 0) + 1

    dates = sorted(activite.keys())
    valeurs = [activite[d] for d in dates]
    plt.figure()
    plt.plot(dates, valeurs, marker='o')
    plt.title("Activité des emprunts (30 derniers jours)")
    plt.xlabel("Date")
    plt.ylabel("Nombre d'emprunts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, 'activite_emprunts.png'))
    plt.close()