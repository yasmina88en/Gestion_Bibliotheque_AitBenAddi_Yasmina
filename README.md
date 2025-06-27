 ##  Projet de Gestion de Bibliothèque

**Développé par : Yasmina Ait Ben Addi**  
**Technologies : Python 3, Tkinter / CustomTkinter, Matplotlib**

---

 ##  Objectif du projet

Créer une application permettant de gérer une bibliothèque (livres, membres, emprunts) avec :
- Une interface **CLI (ligne de commande)**
- Une interface **graphique moderne (Tkinter / CustomTkinter)**
- Une **persistance des données**
- Une **visualisation des statistiques** (graphiques générés)

---

 ##  Fonctionnalités

-  **Livres**
  - Ajouter / Supprimer des livres
  - Visualiser tous les livres
  - Gérer la disponibilité (emprunté ou non)

-  **Membres**
  - Inscrire / Supprimer un membre
  - Voir les livres empruntés

-  **Emprunt / Retour**
  - Emprunter un livre
  - Rendre un livre

-  **Statistiques visuelles**
  - Répartition des genres
  - Auteurs les plus lus
  - Activité des emprunts dans le temps

-  **Gestion des erreurs via des exceptions personnalisées**

---

## Arborescence du projet

 Gestion_Bibliotheque_AitBenAddi_Yasmina/  
│  
├──  .venv/  
│  
├──  assets/  
│   ├── activite_emprunts.png  
│   ├── stats_auteurs.png  
│   ├── stats_genres.png  
│   └── presentation.mp4  
│  
├──  data/  
│   ├── livres.txt  
│   ├── membres.txt  
│   └── historique.csv  
│  
├──  docs/  
│   └── Rapport (2).pdf  
│  
├──  src/  
│   ├── bibliotheque.py  
│   ├── exceptions.py  
│   ├── interface.py  
│   ├── main.py  
│   └── visualisations.py  
│  
├── README.md  
└── requirements.txt

## Lancer le projet

###  Lancer la version Interface Graphique

```bash
python src/interface.py 
```


###  Lancer la version Ligne de Commande (CLI)
```bash 
python src/main.py 
```

##  Installation
### Prérequis
- Python 3.10 ou plus
- les bibliothèques suivantes:
- matplotlib
- tkinter
- pip installé

### Installer les dépendances
```bash
pip install -r requirements.txt
```
##  Exemples d'utilisation

# Exemple 1 : Ajouter un livre via CLI
choisis l'option : 1 - Ajouter un livre
Saisis :
ISBN : 1011
Titre : Les Misérables
Auteur : Victor Hugo
Année : 1862
Genre : Roman


 # Exemple 2 – Emprunter un livre
Choisis l'option : 3 - Emprunter un livre
Entres l’ISBN du livre (ex. 1002) et l’ID du membre (ex. 1)

Un message s’affiche :

Livre emprunté avec succès !

# Exemple 3 – Afficher les statistiques
Lance l'interface graphique et clique sur l’onglet Statistiques :

Les graphiques suivants apparaissent :

- Répartition par genre

- Auteurs les plus lus

- Activité des emprunts



