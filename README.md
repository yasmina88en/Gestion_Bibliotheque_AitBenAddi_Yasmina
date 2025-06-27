 ## 📚 Projet de Gestion de Bibliothèque

**Développé par : Yasmina Ait Ben Addi**  
**Technologies : Python 3, Tkinter / CustomTkinter, Matplotlib**

---

 ## 🎯 Objectif du projet

Créer une application permettant de gérer une bibliothèque (livres, membres, emprunts) avec :
- Une interface **CLI (ligne de commande)**
- Une interface **graphique moderne (Tkinter / CustomTkinter)**
- Une **persistance des données**
- Une **visualisation des statistiques** (graphiques générés)

---

 ## 🚀 Fonctionnalités

- 📚 **Livres**
  - Ajouter / Supprimer des livres
  - Visualiser tous les livres
  - Gérer la disponibilité (emprunté ou non)

- 👥 **Membres**
  - Inscrire / Supprimer un membre
  - Voir les livres empruntés

- 🔁 **Emprunt / Retour**
  - Emprunter un livre
  - Rendre un livre

- 📈 **Statistiques visuelles**
  - Répartition des genres
  - Auteurs les plus lus
  - Activité des emprunts dans le temps

- ✅ **Gestion des erreurs via des exceptions personnalisées**

---

## 🗂️ Arborescence du projet

📁 Gestion_Bibliotheque_AitBenAddi_Yasmina/  
│  
├── 📁 .venv/  
│  
├── 📁 assets/  
│   ├── activite_emprunts.png  
│   ├── stats_auteurs.png  
│   ├── stats_genres.png  
│   └── presentation.mp4  
│  
├── 📁 data/  
│   ├── livres.txt  
│   ├── membres.txt  
│   └── historique.csv  
│  
├── 📁 docs/  
│   └── Rapport (2).pdf  
│  
├── 📁 src/  
│   ├── bibliotheque.py  
│   ├── exceptions.py  
│   ├── interface.py  
│   ├── main.py  
│   └── visualisations.py  
│  
├── README.md  
└── requirements.txt

## 🖥️ Lancer le projet

### ▶️ Lancer la version Interface Graphique

```bash
python src/interface.py 
```


### ▶️ Lancer la version Ligne de Commande (CLI)
```bash 
python src/main.py 
```

## 📥 Installation
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





