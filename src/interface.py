import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from bibliotheque import Bibliotheque
from visualisations import stats_genres, stats_auteurs, stats_activite_emprunts, ASSETS_DIR

# Configuration de base de CustomTkinter
ctk.set_appearance_mode("light")  # light mode pour couleurs joyeuses
ctk.set_default_color_theme("blue")  # thème bleu classique

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestion Bibliothèque - Interface Graphique")
        self.geometry("1000x600")
        self.minsize(900, 550)

        self.biblio = Bibliotheque()

        self.create_widgets()

    def create_widgets(self):
        # Onglets
        self.tabs = ctk.CTkTabview(self, width=980, height=550)
        self.tabs.pack(padx=10, pady=10, fill="both", expand=True)

        # Onglets principaux
        self.tabs.add("Livres")
        self.tabs.add("Membres")
        self.tabs.add("Emprunts")
        self.tabs.add("Statistiques")

        # --- Onglet Livres ---
        self.frame_livres = self.tabs.tab("Livres")
        self._setup_tab_livres()

        # --- Onglet Membres ---
        self.frame_membres = self.tabs.tab("Membres")
        self._setup_tab_membres()

        # --- Onglet Emprunts ---
        self.frame_emprunts = self.tabs.tab("Emprunts")
        self._setup_tab_emprunts()

        # --- Onglet Statistiques ---
        self.frame_stats = self.tabs.tab("Statistiques")
        self._setup_tab_stats()

    ### Onglet Livres ###
    def _setup_tab_livres(self):
        # Boutons ajouter / supprimer livres
        btn_frame = ctk.CTkFrame(self.frame_livres)
        btn_frame.pack(fill="x", padx=20, pady=10)

        self.btn_ajout_livre = ctk.CTkButton(
            btn_frame, text="Ajouter un livre", command=self.ajouter_livre, corner_radius=15,
            fg_color="#4CAF50", hover_color="#45A049", width=160, height=40, font=("Arial", 14, "bold")
        )
        self.btn_ajout_livre.pack(side="left", padx=10)

        self.btn_suppr_livre = ctk.CTkButton(
            btn_frame, text="Supprimer un livre", command=self.supprimer_livre, corner_radius=15,
            fg_color="#F44336", hover_color="#D32F2F", width=160, height=40, font=("Arial", 14, "bold")
        )
        self.btn_suppr_livre.pack(side="left", padx=10)

        # Tableau livres
        self.table_livres = ctk.CTkScrollableFrame(self.frame_livres)
        self.table_livres.pack(fill="both", expand=True, padx=20, pady=10)

        self._refresh_table_livres()

    def _refresh_table_livres(self):
        # Vider contenu précédent
        for widget in self.table_livres.winfo_children():
            widget.destroy()

        # Titres colonnes en gras avec trait noir solide
        headers = ["ISBN", "Titre", "Auteur", "Année", "Genre", "Statut"]
        header_frame = ctk.CTkFrame(self.table_livres, fg_color="transparent")
        header_frame.pack(fill="x")

        for idx, h in enumerate(headers):
            label = ctk.CTkLabel(header_frame, text=h, font=("Arial", 13, "bold"), width=130, anchor="w")
            label.grid(row=0, column=idx, padx=5, pady=(5,3))

        # Trait horizontal plein noir
        separator = ctk.CTkFrame(self.table_livres, height=2, fg_color="black")
        separator.pack(fill="x", padx=5, pady=(0, 10))

        # Affichage des livres
        for livre in self.biblio.lister_livres():
            row_frame = ctk.CTkFrame(self.table_livres, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            valeurs = [livre.isbn, livre.titre, livre.auteur, str(livre.annee), livre.genre, livre.statut]
            for idx, val in enumerate(valeurs):
                lbl = ctk.CTkLabel(row_frame, text=val, font=("Arial", 12), width=130, anchor="w")
                lbl.grid(row=0, column=idx, padx=5)

    def ajouter_livre(self):
        # Fenêtre popup pour ajouter un livre
        popup = ctk.CTkToplevel(self)
        popup.title("Ajouter un livre")
        popup.geometry("400x350")
        popup.grab_set()

        labels = ["ISBN", "Titre", "Auteur", "Année", "Genre"]
        entries = {}

        for i, text in enumerate(labels):
            ctk.CTkLabel(popup, text=text + ":", font=("Arial", 12)).pack(pady=(15 if i==0 else 5, 5))
            entry = ctk.CTkEntry(popup, width=300)
            entry.pack()
            entries[text] = entry

        def valider():
            try:
                isbn = entries["ISBN"].get().strip()
                titre = entries["Titre"].get().strip()
                auteur = entries["Auteur"].get().strip()
                annee = int(entries["Année"].get().strip())
                genre = entries["Genre"].get().strip()
                if not (isbn and titre and auteur and genre):
                    raise ValueError("Tous les champs doivent être remplis.")
                self.biblio.ajouter_livre(isbn, titre, auteur, annee, genre)
                self._refresh_table_livres()
                popup.destroy()
                messagebox.showinfo("Succès", "Livre ajouté avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter le livre : {e}")

        btn_valider = ctk.CTkButton(popup, text="Valider", command=valider, width=120, corner_radius=15,
                                    fg_color="#2196F3", hover_color="#1976D2", font=("Arial", 13, "bold"))
        btn_valider.pack(pady=20)

    def supprimer_livre(self):
        # Fenêtre popup pour supprimer un livre (par ISBN)
        popup = ctk.CTkToplevel(self)
        popup.title("Supprimer un livre")
        popup.geometry("350x200")
        popup.grab_set()

        ctk.CTkLabel(popup, text="ISBN du livre à supprimer:", font=("Arial", 12)).pack(pady=20)
        entry_isbn = ctk.CTkEntry(popup, width=250)
        entry_isbn.pack()

        def valider():
            isbn = entry_isbn.get().strip()
            if not isbn:
                messagebox.showerror("Erreur", "Veuillez entrer un ISBN valide.")
                return
            try:
                self.biblio.supprimer_livre(isbn)
                self._refresh_table_livres()
                popup.destroy()
                messagebox.showinfo("Succès", f"Livre ISBN {isbn} supprimé.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer le livre : {e}")

        btn_valider = ctk.CTkButton(popup, text="Supprimer", command=valider, width=120, corner_radius=15,
                                    fg_color="#F44336", hover_color="#D32F2F", font=("Arial", 13, "bold"))
        btn_valider.pack(pady=20)

    ### Onglet Membres ###
    def _setup_tab_membres(self):
        btn_frame = ctk.CTkFrame(self.frame_membres)
        btn_frame.pack(fill="x", padx=20, pady=10)

        self.btn_ajout_membre = ctk.CTkButton(
            btn_frame, text="Ajouter un membre", command=self.ajouter_membre, corner_radius=15,
            fg_color="#4CAF50", hover_color="#45A049", width=160, height=40, font=("Arial", 14, "bold")
        )
        self.btn_ajout_membre.pack(side="left", padx=10)

        self.btn_suppr_membre = ctk.CTkButton(
            btn_frame, text="Supprimer un membre", command=self.supprimer_membre, corner_radius=15,
            fg_color="#F44336", hover_color="#D32F2F", width=160, height=40, font=("Arial", 14, "bold")
        )
        self.btn_suppr_membre.pack(side="left", padx=10)

        self.table_membres = ctk.CTkScrollableFrame(self.frame_membres)
        self.table_membres.pack(fill="both", expand=True, padx=20, pady=10)

        self._refresh_table_membres()

    def _refresh_table_membres(self):
        for widget in self.table_membres.winfo_children():
            widget.destroy()

        headers = ["ID", "Nom", "Livres empruntés"]
        header_frame = ctk.CTkFrame(self.table_membres, fg_color="transparent")
        header_frame.pack(fill="x")

        for idx, h in enumerate(headers):
            label = ctk.CTkLabel(header_frame, text=h, font=("Arial", 13, "bold"), width=200 if idx==2 else 130, anchor="w")
            label.grid(row=0, column=idx, padx=5, pady=(5,3))

        separator = ctk.CTkFrame(self.table_membres, height=2, fg_color="black")
        separator.pack(fill="x", padx=5, pady=(0, 10))

        for membre in self.biblio.lister_membres():
            row_frame = ctk.CTkFrame(self.table_membres, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            livres_empruntes = ", ".join(membre.livres_empruntes) if membre.livres_empruntes else "Aucun"
            valeurs = [str(membre.ID), membre.nom, livres_empruntes]
            for idx, val in enumerate(valeurs):
                width = 200 if idx == 2 else 130
                lbl = ctk.CTkLabel(row_frame, text=val, font=("Arial", 12), width=width, anchor="w")
                lbl.grid(row=0, column=idx, padx=5)

    def ajouter_membre(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Ajouter un membre")
        popup.geometry("350x250")
        popup.grab_set()

        ctk.CTkLabel(popup, text="ID:", font=("Arial", 12)).pack(pady=(20,5))
        entry_id = ctk.CTkEntry(popup, width=300)
        entry_id.pack()

        ctk.CTkLabel(popup, text="Nom:", font=("Arial", 12)).pack(pady=5)
        entry_nom = ctk.CTkEntry(popup, width=300)
        entry_nom.pack()

        def valider():
            try:
                ID = int(entry_id.get().strip())
                nom = entry_nom.get().strip()
                if not nom:
                    raise ValueError("Le nom ne peut pas être vide.")
                self.biblio.inscrire_membre(ID, nom)
                self._refresh_table_membres()
                popup.destroy()
                messagebox.showinfo("Succès", "Membre ajouté avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter le membre : {e}")

        btn_valider = ctk.CTkButton(popup, text="Valider", command=valider, width=120, corner_radius=15,
                                    fg_color="#2196F3", hover_color="#1976D2", font=("Arial", 13, "bold"))
        btn_valider.pack(pady=20)

    def supprimer_membre(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Supprimer un membre")
        popup.geometry("350x200")
        popup.grab_set()

        ctk.CTkLabel(popup, text="ID du membre à supprimer:", font=("Arial", 12)).pack(pady=20)
        entry_id = ctk.CTkEntry(popup, width=250)
        entry_id.pack()

        def valider():
            try:
                ID = int(entry_id.get().strip())
                self.biblio.supprimer_membre(ID)
                self._refresh_table_membres()
                popup.destroy()
                messagebox.showinfo("Succès", f"Membre ID {ID} supprimé.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer le membre : {e}")

        btn_valider = ctk.CTkButton(popup, text="Supprimer", command=valider, width=120, corner_radius=15,
                                    fg_color="#F44336", hover_color="#D32F2F", font=("Arial", 13, "bold"))
        btn_valider.pack(pady=20)

    ### Onglet Emprunts ###
    def _setup_tab_emprunts(self):
        frame = self.frame_emprunts
        padding_x = 30
        padding_y = 15

        lbl1 = ctk.CTkLabel(frame, text="Emprunter un livre", font=("Arial", 16, "bold"))
        lbl1.pack(pady=(20, 5))

        # Formulaire emprunt
        form_frame = ctk.CTkFrame(frame)
        form_frame.pack(pady=10)

        ctk.CTkLabel(form_frame, text="ISBN:", width=100).grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky="e")
        self.entry_isbn_emprunt = ctk.CTkEntry(form_frame, width=200)
        self.entry_isbn_emprunt.grid(row=0, column=1, pady=padding_y, sticky="w")

        ctk.CTkLabel(form_frame, text="ID Membre:", width=100).grid(row=1, column=0, padx=padding_x, pady=padding_y, sticky="e")
        self.entry_id_emprunt = ctk.CTkEntry(form_frame, width=200)
        self.entry_id_emprunt.grid(row=1, column=1, pady=padding_y, sticky="w")

        btn_emprunter = ctk.CTkButton(frame, text="Emprunter", width=160, corner_radius=15,
                                      fg_color="#2196F3", hover_color="#1976D2", font=("Arial", 14, "bold"),
                                      command=self.action_emprunter)
        btn_emprunter.pack(pady=15)

        lbl2 = ctk.CTkLabel(frame, text="Rendre un livre", font=("Arial", 16, "bold"))
        lbl2.pack(pady=(40, 5))

        # Formulaire retour
        form_frame2 = ctk.CTkFrame(frame)
        form_frame2.pack(pady=10)

        ctk.CTkLabel(form_frame2, text="ISBN:", width=100).grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky="e")
        self.entry_isbn_retour = ctk.CTkEntry(form_frame2, width=200)
        self.entry_isbn_retour.grid(row=0, column=1, pady=padding_y, sticky="w")

        ctk.CTkLabel(form_frame2, text="ID Membre:", width=100).grid(row=1, column=0, padx=padding_x, pady=padding_y, sticky="e")
        self.entry_id_retour = ctk.CTkEntry(form_frame2, width=200)
        self.entry_id_retour.grid(row=1, column=1, pady=padding_y, sticky="w")

        btn_rendre = ctk.CTkButton(frame, text="Rendre", width=160, corner_radius=15,
                                   fg_color="#4CAF50", hover_color="#45A049", font=("Arial", 14, "bold"),
                                   command=self.action_rendre)
        btn_rendre.pack(pady=15)

    def action_emprunter(self):
        isbn = self.entry_isbn_emprunt.get().strip()
        ID = self.entry_id_emprunt.get().strip()
        try:
            if not isbn or not ID:
                raise ValueError("ISBN et ID membre requis.")
            self.biblio.emprunter_livre(isbn, ID)
            self._refresh_table_livres()
            self._refresh_table_membres()
            messagebox.showinfo("Succès", f"Le livre ISBN {isbn} a été emprunté par le membre {ID}.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'emprunter le livre : {e}")

    def action_rendre(self):
        isbn = self.entry_isbn_retour.get().strip()
        ID = self.entry_id_retour.get().strip()
        try:
            if not isbn or not ID:
                raise ValueError("ISBN et ID membre requis.")
            self.biblio.rendre_livre(isbn, ID)
            self._refresh_table_livres()
            self._refresh_table_membres()
            messagebox.showinfo("Succès", f"Le livre ISBN {isbn} a été rendu par le membre {ID}.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de rendre le livre : {e}")

    ### Onglet Statistiques ###
    def _setup_tab_stats(self):
        self.stats_images_frame = ctk.CTkFrame(self.frame_stats)
        self.stats_images_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.img_genres_label = ctk.CTkLabel(self.stats_images_frame, text="")
        self.img_auteurs_label = ctk.CTkLabel(self.stats_images_frame, text="")
        self.img_activite_label = ctk.CTkLabel(self.stats_images_frame, text="")

        # Générer et afficher les stats au démarrage de l'onglet
        self.tabs.tab("Statistiques").bind("<<NotebookTabChanged>>", lambda e: self.show_stats())
        # Comme CustomTkinter n'a pas d'évènement direct, on appelle la fonction ici aussi
        self.show_stats()

    def show_stats(self):
        # Nettoyer
        for widget in self.stats_images_frame.winfo_children():
            widget.pack_forget()

        try:
            stats_genres()
            stats_auteurs()
            stats_activite_emprunts()

            self.img_genres = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS_DIR, 'stats_genres.png')).resize((550, 360)))
            self.img_auteurs = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS_DIR, 'stats_auteurs.png')).resize((550, 360)))
            self.img_activite = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS_DIR, 'activite_emprunts.png')).resize((550, 360)))

            self.img_genres_label.configure(image=self.img_genres)
            self.img_auteurs_label.configure(image=self.img_auteurs)
            self.img_activite_label.configure(image=self.img_activite)

            self.img_genres_label.pack(side="left", padx=15)
            self.img_auteurs_label.pack(side="left", padx=15)
            self.img_activite_label.pack(side="left", padx=15)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des statistiques : {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
