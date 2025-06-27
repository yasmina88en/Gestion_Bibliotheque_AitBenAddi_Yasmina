from bibliotheque import Bibliotheque
from visualisations import stats_genres, stats_auteurs, stats_activite_emprunts, ASSETS_DIR
import os

print("Répertoire courant:", os.getcwd())
print("Dossier assets existe ?", os.path.isdir(ASSETS_DIR))


def menu():
    biblio = Bibliotheque()
    while True:
        print("\n=== GESTION BIBLIOTHÈQUE ===")
        print("1. Ajouter un livre")
        print("2. Inscrire un membre")
        print("3. Emprunter un livre")
        print("4. Rendre un livre")
        print("5. Lister tous les livres")
        print("6. Afficher les statistiques")
        print("7. Sauvegarder et quitter")
        print("8. Supprimer un livre")
        print("9. Supprimer un membre")
        choix = input("Choix : ")

        try:
            if choix == '1':
                isbn = input("ISBN : ")
                titre = input("Titre : ")
                auteur = input("Auteur : ")
                annee = input("Année : ")
                genre = input("Genre : ")
                biblio.ajouter_livre(isbn, titre, auteur, annee, genre)
                print("Livre ajouté.")

            elif choix == '2':
                mid = input("ID nouveau membre : ")
                nom = input("Nom du membre : ")
                biblio.inscrire_membre(mid, nom)
                print("Membre inscrit.")

            elif choix == '3':
                isbn = input("ISBN à emprunter : ")
                mid = input("ID du membre : ")
                biblio.emprunter_livre(isbn, mid)
                print("Emprunt enregistré.")

            elif choix == '4':
                isbn = input("ISBN à rendre : ")
                mid = input("ID du membre : ")
                biblio.rendre_livre(isbn, mid)
                print("Retour enregistré.")

            elif choix == '5':
                for livre in biblio.lister_livres():
                    print(f"{livre.isbn} - {livre.titre} ({livre.statut})")

            elif choix == '6':
                print("Génération des graphiques…")
                stats_genres()
                stats_auteurs()
                stats_activite_emprunts()
                print("Statistiques sauvées dans assets/.")

            elif choix == '7':
                biblio.sauvegarder()
                print("Données sauvegardées. Au revoir !")
                break

            elif choix == '8':
                isbn = input("ISBN du livre à supprimer : ")
                biblio.supprimer_livre(isbn)
                print("Livre supprimé.")

            elif choix == '9':
                mid = input("ID du membre à supprimer : ")
                biblio.supprimer_membre(mid)
                print("Membre supprimé.")

            else:
                print("Choix invalide.")

        except Exception as e:
            print(f"Erreur : {e}")


if __name__ == '__main__':
    menu()
