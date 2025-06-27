import os
import csv
from datetime import datetime
from exceptions import (
    LivreIndisponibleError,
    QuotaEmpruntDepasseError,
    MembreInexistantError,
    LivreInexistantError
)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class Livre:
    def __init__(self, isbn, titre, auteur, annee, genre, statut='disponible'):
        self.isbn = isbn
        self.titre = titre
        self.auteur = auteur
        self.annee = int(annee)
        self.genre = genre
        self.statut = statut  # 'disponible' ou 'emprunté'

    def emprunter(self):
        if self.statut == 'emprunté':
            raise LivreIndisponibleError(f"Le livre '{self.titre}' est déjà emprunté.")
        self.statut = 'emprunté'

    def rendre(self):
        self.statut = 'disponible'

    def to_line(self):
        """Sérialisation en format texte pour livres.txt"""
        return f"{self.isbn};{self.titre};{self.auteur};{self.annee};{self.genre};{self.statut}\n"

class Membre:
    def __init__(self, ID, nom, livres_empruntes=None):
        self.ID = int(ID)
        self.nom = nom
        # Liste d'ISBN de livres empruntés
        self.livres_empruntes = livres_empruntes or []

    def emprunter(self, livre: Livre, max_quota=3):
        if len(self.livres_empruntes) >= max_quota:
            raise QuotaEmpruntDepasseError(f"Le membre {self.nom} a atteint son quota.")
        livre.emprunter()
        self.livres_empruntes.append(livre.isbn)

    def rendre(self, livre: Livre):
        if livre.isbn in self.livres_empruntes:
            livre.rendre()
            self.livres_empruntes.remove(livre.isbn)

    def to_line(self):
        """Sérialisation en format texte pour membres.txt"""
        livres = ','.join(self.livres_empruntes)
        return f"{self.ID};{self.nom};{livres}\n"

class Bibliotheque:
    def __init__(self):
        self.livres = {}   # isbn -> Livre
        self.membres = {}  # id -> Membre
        self.historique_file = os.path.join(DATA_DIR, 'historique.csv')
        self._load_data()

    def _load_data(self):
        """Charge livres.txt, membres.txt et historique.csv"""
        # Chargement des livres
        with open(os.path.join(DATA_DIR, 'livres.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                isbn, titre, auteur, annee, genre, statut = line.strip().split(';')
                self.livres[isbn] = Livre(isbn, titre, auteur, annee, genre, statut)
        # Chargement des membres
        with open(os.path.join(DATA_DIR, 'membres.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                id_m, nom, livres = line.strip().split(';')
                livres_list = livres.split(',') if livres else []
                self.membres[int(id_m)] = Membre(id_m, nom, livres_list)
        # Pas besoin de charger historique en mémoire

    def _save_all(self):
        """Enregistre les livres et les membres dans leurs fichiers respectifs"""
        with open(os.path.join(DATA_DIR, 'livres.txt'), 'w', encoding='utf-8') as f:
            for livre in self.livres.values():
                f.write(livre.to_line())
        with open(os.path.join(DATA_DIR, 'membres.txt'), 'w', encoding='utf-8') as f:
            for membre in self.membres.values():
                f.write(membre.to_line())

    def _log_action(self, isbn, ID, action):
        """Ajoute une ligne à historique.csv"""
        date = datetime.now().strftime('%Y-%m-%d')
        with open(self.historique_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([date, isbn, ID, action])

    def ajouter_livre(self, isbn, titre, auteur, annee, genre):
        """Ajoute un nouveau livre"""
        if isbn in self.livres:
            raise Exception(f"Le livre ISBN={isbn} existe déjà.")
        self.livres[isbn] = Livre(isbn, titre, auteur, annee, genre)

    def supprimer_livre(self, isbn):
        """Supprime un livre existant"""
        if isbn not in self.livres:
            raise LivreInexistantError(f"ISBN {isbn} introuvable.")
        del self.livres[isbn]

    def inscrire_membre(self, ID, nom):
        """Enregistre un nouveau membre"""
        if int(ID) in self.membres:
            raise Exception(f"Le membre ID={ID} existe déjà.")
        self.membres[int(ID)] = Membre(ID, nom)

    def supprimer_membre(self, ID):
        """Supprime un membre existant"""
        mid = int(ID)
        if mid not in self.membres:
            raise MembreInexistantError(f"Membre ID={mid} introuvable.")
        del self.membres[mid]

    def emprunter_livre(self, isbn, ID):
        """Gestion d'emprunt"""
        if isbn not in self.livres:
            raise LivreInexistantError(f"ISBN {isbn} introuvable.")
        if int(ID) not in self.membres:
            raise MembreInexistantError(f"Membre ID={ID} introuvable.")
        membre = self.membres[int(ID)]
        livre = self.livres[isbn]
        membre.emprunter(livre)
        self._log_action(isbn, ID, 'emprunt')

    def rendre_livre(self, isbn, ID):
        """Gestion de retour"""
        if isbn not in self.livres:
            raise LivreInexistantError(f"ISBN {isbn} introuvable.")
        if int(ID) not in self.membres:
            raise MembreInexistantError(f"Membre ID={ID} introuvable.")
        membre = self.membres[int(ID)]
        livre = self.livres[isbn]
        membre.rendre(livre)
        self._log_action(isbn, ID, 'retour')

    def lister_livres(self):
        """Retourne la liste de tous les livres"""
        return list(self.livres.values())

    def lister_membres(self):
        """Retourne la liste de tous les membres"""
        return list(self.membres.values())

    def sauvegarder(self):
        """Enregistre tout et quitte"""
        self._save_all()