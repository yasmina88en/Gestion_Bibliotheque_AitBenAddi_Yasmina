class LivreIndisponibleError(Exception):
    def __init__(self, titre):
        super().__init__(f"Le livre '{titre}' est déjà emprunté.")

class QuotaEmpruntDepasseError(Exception):
    def __init__(self, nom):
        super().__init__(f"{nom} a dépassé le quota maximal de livres empruntés.")

class MembreInexistantError(Exception):
    def __init__(self, ID):
        super().__init__(f"Membre avec ID {ID} introuvable.")

class LivreInexistantError(Exception):
    def __init__(self, isbn):
        super().__init__(f"Livre avec ISBN {isbn} introuvable.")
