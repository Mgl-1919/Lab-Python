
# _______________________________________________________________
# FICHIER : App_RAC.py
# DESCRIPTION : INTERFACE GRAPHIQUE - Laboratoire Python (Netflix)
# Auteur : Miguel Andrade
# DATE : 28 d'avril 2026
# ________________________________________________________________

import tkinter as tk
from tkinter import messagebox
from models import charger_donnees, Employe, Client

# -- Chargement des données ---
employes, clients, films = charger_donnees()

# _________________________________________________
# Fenêtre : PRINCIPALE
# _________________________________________________

class FenetrePrincipale(tk.Toplevel):
    """  Fenêtre principale pour afficher la connexion initiale """
    def __init__(self, employe):
        super().__init__()
        self.employe = employe
        self.title(f"Streaming RAC - {employe.get_prenom()}")
        self.geometry("800x600")

        # -- Titre ---
        tk.Label(self, text=f"Bienvenue {employe.get_prenom()}! " f"({employe.get_type_acces()})", font=("Arial", 14, "bold")).pack(pady=10)

        # -- Liste de clients ---
        tk.Label(self, text="Clients:", font=("Arail", 14, "bold")).pack()
        self.liste_clients = tk.Listbox(self, width=60, height=8)
        self.liste_clients.pack(pady=5)
        for client in clients:
            self.liste_clients.insert(tk.END, str(client))

        # -- Liste de films ---
        tk.Label(self, text="Films:", font=("Arial", 12, "bold")).pack()
        self.liste_films = tk.Listbox(self, width=60, height=8)
        self.liste_films.pack(pady=5)
        for film in films:
            self.liste_films.insert(tk.END, str(film))

        # -- Boutons ---
        frame_boutons = tk.Frame(self)
        frame_boutons.pack(pady=10)

        tk.Button(frame_boutons, text="Nouveau client", command=self.nouveau_client).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_boutons, text="Déconnexion", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def nouveau_client(self):
        messagebox.showinfo("Information", "Fenêtre création client - À venir!!")

# ________________________________________________________________
# Fenêtre : LOGIN
# ________________________________________________________________

class FenetreLogin(tk.Tk):
    """ Espace que permet la connexion des employées """
    def __init__(self):
        super().__init__()
        self.title("Streaming RAC")
        self.geometry("400x300")
        self.resizable(False, False)

        # -- Titre ---
        tk.Label(self, text="Streaming RAC", font=("Arial", 20, "bold")).pack(pady=20)

        tk.Label(self, text="Code utilisateur:").pack()
        self.code_entry = tk.Entry(self)
        self.code_entry.pack(pady=5)

        tk.Label(self, text="Mot de passe:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Se connecter", command=self.connecter).pack(pady=20)
    def connecter(self):
        code = self.code_entry.get()
        password = self.password_entry.get()

        for employe in employes:
            if employe.valider_connexion(code, password):
                self.withdraw()  # pour chache le login
                FenetrePrincipale(employe)
                return
        messagebox.showerror("Erreur", "Code ou mot de passe invalide!")

# -- Lancement de l'application ---
if __name__ == "__main__":
    app = FenetreLogin()
    app.mainloop()


# _________________________________________________________________________
# 