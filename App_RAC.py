
# _______________________________________________________________
# FICHIER : App_RAC.py
# DESCRIPTION : INTERFACE GRAPHIQUE - Laboratoire Python (Netflix)
# Auteur : Miguel Andrade
# DATE : 28 d'avril 2026
# ________________________________________________________________

import tkinter as tk
from tkinter import messagebox
from datetime import date
from models import charger_donnees, Employe, Client

# -- Chargement des données ---
employes, clients, films = charger_donnees()

# ______________________________________________________________________
# INFOBULLE
# ______________________________________________________________________


class Infobulle:
    """ Infobulle informative qui permet d'afficher des details contextuels comme les acteurs ou la durée d'un film. """
    def __init__(self, widget, texte):
        # Composant visuel graphique auquel l'infobulle est rattachée
        self.widget = widget
        # Le contenu textuel dynamique ç afficher dans l'infobulle
        self.texte = texte
        # Variable de contrôle pour suivre l'existence de la fenêtre contextuelle en mémoire
        self.bulle = None
        # -- Liaison d'événements --
        # Déclenche l'affichage lorsque le curseur entre sur le widget
        self.widget.bind("<Enter>", self.afficher)
        # Masque l'infobulle dès que le curseur quitte la zone du widget
        self.widget.bind("<Leave>", self.cacher)

    def afficher(self, event):
        """ Crée et positionne dynamiquement une mini-fen^tre contextuelle près du curseur. """
        # Calcule des coordonnées géométriques de l'écran pour positionner la bulle de façon ergonomique
        x = self.widget.winfo_rootx() + 50
        y = self.widget.winfo_rooty() + 20
        # Création d'une fen^tre éphémère rattachée au widget parent
        self.bulle = tk.Toplevel(self.widget)
        # supprime les bordures standard du système d'exploitation pour donner l'aspect minimaliste d'une bulle
        self.bulle.wm_overrideredirect(True)
        # application du positionnement calculé
        self.bulle.wm_geometry(f"+{x}+{y}")
        # Configuration visuelle
        tk.Label(self.bulle, text=self.texte, background="Yellow", relief="solid").pack()

    def cacher(self, event):
        """ Détruit l'infobulle de façon sécurisée pour libérer les resources système  """
        # Vérifie si l'infobulle existe bel et bien avant d'agir
        if self.bulle:
            # ferme et détruit le composant graphique de la mémoire vive
            self.bulle.destroy()
            # Réinitialise l'état pour permettre une future réapparition au prochain survol
            self.bulle = None

# _______________________________________________________________________
#  Fenêtre : MODIFIER CLIENT
# _______________________________________________________________________


class FenetreModifierClient(tk.Toplevel):
    """ Fenêtre pour modifier un client sélectionné. Les champs sont pré-remplis avec les données actuelles"""
    def __init__(self, parent, client):
        # Apelle le constructeur de Toplevel pour initialiser la fenêtre secondaire
        super().__init__(parent)
        # Conserve la référence (FenetrePrincipale) pour synchroniser l'affichage
        self.parent = parent
        # stocke la référence de l'objet client
        self.client = client
        # Titre de la fenêtre
        self.title("Modifier Client")
        # Dimensions de la fenêtre
        self.geometry("400x400")

        # En-tête pour guider l'employé dans l'action de modification
        tk.Label(self, text="Modifier un client", font=("Arial", 14, "bold")).pack(pady=10)

        # -- Champs Pre-remplis ---
        tk.Label(self, text="Nom:").pack()
        self.nom_entry = tk.Entry(self)
        # Extrait et injecte le nom du client
        self.nom_entry.insert(0, client.get_nom())
        self.nom_entry.pack(pady=3)

        tk.Label(self, text="Prenom:").pack()
        self.prenom_entry = tk.Entry(self)
        # Extrait et injecte le prenom du client
        self.prenom_entry.insert(0, client.get_prenom())
        self.prenom_entry.pack(pady=3)

        tk.Label(self, text="Courriel:").pack()
        self.courriel_entry = tk.Entry(self)
        # Extrait et injecte le courriel du client
        self.courriel_entry.insert(0, client.get_courriel())
        self.courriel_entry.pack(pady=3)

        # Bouton pour valider et appliquer les modifications en memoire
        tk.Button(self, text="Sauvegarder", command=self.sauvegarder).pack(pady=15)

    def sauvegarder(self):
        """ Valide les modifications apportées et met à jour l'objet client. """
        # Récupération et nettoyage des espaces blancs inutiles
        nom = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()
        courriel = self.courriel_entry.get().strip()

        # validation des champs vides
        if not nom or not prenom or not courriel:
            messagebox.showerror("Erreur", "Vous devez remplir tous le champs!")
            return

        # Validation du format courriel
        if "@" not in courriel or "." not in courriel:
            messagebox.showerror("Erreur", "Format du courriel invalide!")
            return

        # -- Vérification du courriel  unique ---
        for c in clients:
            if c.get_courriel() == courriel.lower() and c != self.client:
                messagebox.showerror("Erreur", "Ce courriel existe déjà")
                return

        # -- Mise à jour de l'objet ---
        # Modifie le nom dans l'instance d'objet
        self.client.set_nom(nom)
        # Modifie le prenom dans l'instance d'objet
        self.client.set_prenom(prenom)
        # Modifie le courriel en minuscules pour maintenir la cohérence
        self.client.set_courriel(courriel.lower())

        # -- Synchronisation et retourne visuel ---
        # Demande à la fen^tre principale de rafraichir sa Listbox
        self.parent.actualiser_liste_clients()
        # Notification de réussite
        messagebox.showinfo("Succès", "Client modifié avec succès!")
        # Ferme et détruit la fenêtre de modification.
        self.destroy()
# _________________________________________________________________________
# Fenêtre : CRÉER CLIENT
# _________________________________________________________________________


class FenetreCreerClient(tk.Toplevel):
    """ Espace utilisé pour la création d'un nouveau client.
    Permet valider le courriel et le mot de passe avant sauvegarde. """
    def __init__(self, parent):
        # Apelle le constructeur parent pour créer la fenêtre secondaire
        super().__init__(parent)
        # Garde la référence pour rafraichir la liste des clients après ajout
        self.parent = parent
        # Titre de la fenêtre de saisie
        self.title("Création d'un client")
        # Dimensionnement adapté au formulaire
        self.geometry("400x400")

        # En-tête du formulaire pour une meilleure expérience utilisateur
        tk.Label(self, text="Informations du client", font=("Arial", 14, "bold")).pack(pady=10)

        # -- Champs demandés pour le project ---
        tk.Label(self, text="Nom:").pack()
        # Champ de texte pour le nom
        self.nom_entry = tk.Entry(self)
        self.nom_entry.pack(pady=3)

        tk.Label(self, text="Prénom:").pack()
        # Champ de texte pour le prenom
        self.prenom_entry = tk.Entry(self)
        self.prenom_entry.pack(pady=3)

        tk.Label(self, text="Courriel:").pack()
        # Champ utilisé pour l'identifiant unique
        self.courriel_entry = tk.Entry(self)
        self.courriel_entry.pack(pady=3)

        tk.Label(self, text="Mot de passe (8+ car):").pack()
        # Masquage des caractères pour la confidentialité
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=3)

        tk.Label(self, text="Sexe (M/F/Autre):").pack()
        # Champ pour l'attribut sexe hérité de Personne
        self.sexe_entry = tk.Entry(self)
        self.sexe_entry.pack(pady=3)

        # Bouton déclenchant la logique de validation
        tk.Button(self, text="Sauvegarder", command=self.sauvegarder).pack(pady=15)

    def sauvegarder(self):
        """ Valide les données selon les règles d'affaires avant l'instanciation. """
        # Nettoyage des espaces blancs pour éviter les entrées vides accidentelles
        nom = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()
        courriel = self.courriel_entry.get().strip()
        password = self.password_entry.get().strip()
        sexe = self.sexe_entry.get().strip()

        # -- Vérifications de présence ---
        if not nom or not prenom or not courriel or not password:
            messagebox.showerror("Erreur", "Completez l'information correctement. Tous les camps sont obligatoires!!")
            return

        # -- Validation du format de courriel ---
        if "@" not in courriel or "." not in courriel:
            messagebox.showerror("Erreur", "Le format du courriel est invalide !")
            return

        # -- Validation de la longueur du mot de passe ---
        if len(password) < 8:
            messagebox.showerror("Erreur", "Le mot de passe doit avoir 8 caractères minimum !")
            return

        #
        for c in clients:
            if c.get_courriel() == courriel.lower():
                messagebox.showerror("Erreur", "Ce Courriel est déjà utilisée.")
                return

        # --  Créer client ---
        # Crée un nouvel objet Client
        nouveau = Client(nom, prenom, sexe, date.today(), courriel, password)
        # Ajout à la collection globale de données
        clients.append(nouveau)
        # mise ç jour immédiate de l'interface
        self.parent.actualiser_liste_clients()
        messagebox.showinfo("Succès", f"Client {prenom} {nom} Créé avec succès!")
        # ferme la fenêtre de création après le succès
        self.destroy()

# _________________________________________________
# Fenêtre : PRINCIPALE
# _________________________________________________


class FenetrePrincipale(tk.Toplevel):
    """  Fenêtre principale pour établir la connexion initiale. Affiche la liste des clients et des films.
     Permet de créer, modifier et supprimer des clients."""
    def __init__(self, parent, employe):
        # Initialise la fenêtre secondaire (Enfant du login)
        super().__init__(parent)
        # Garde une référence à la fen^tre de Login pour la déconnexion
        self.parent = parent
        # Stocke l'objet employé pour constater les droits d'accès plus tard
        self.employe = employe
        # Titre dynamique incluant le prenom de l'employé connecté
        self.title(f"Streaming RAC - {employe.get_prenom()}")
        # Taille de la fenêtre principale
        self.geometry("800x600")

        # -- Menu ---
        # Barre de menu haut de la fenêtre
        menubar = tk.Menu(self)
        menu_fichier = tk.Menu(menubar, tearoff=0)
        # Option pour se déconnecter et revenir au Login
        menu_fichier.add_command(label="Déconnecter", command=self.deconnecter)
        # Ligne de séparation visuelle
        menu_fichier.add_separator()
        # Fermeture complète de l'application
        menu_fichier.add_command(label="Quitter", command=self.quit)
        # Ajout du menu à la barre
        menubar.add_cascade(label="Menu", menu=menu_fichier)
        # Application de la barre de menu à la fenêtre
        self.config(menu=menubar)

        # -- Titre ---
        # Affiche le nom et le niveau d'accès (TOTAL ou LECTURE) de l'employé
        tk.Label(self, text=f"Bienvenue {employe.get_prenom()}! " f"({employe.get_type_acces()})", font=("Arial", 14, "bold")).pack(pady=10)

        # -- Liste de clients ---
        # Permet capter tous les clients enregistrés
        tk.Label(self, text="Clients:", font=("Arial", 14, "bold")).pack()
        self.liste_clients = tk.Listbox(self, width=60, height=8)
        self.liste_clients.pack(pady=5)
        # Remplit la liste avec les clients enregistrés
        for client in clients:
            self.liste_clients.insert(tk.END, str(client))

        # -- Liste de films ---
        # Affiche tous les films disponibles
        tk.Label(self, text="Films:", font=("Arial", 12, "bold")).pack()
        self.liste_films = tk.Listbox(self, width=60, height=8)
        self.liste_films.pack(pady=5)
        # Parcours de la liste globale
        for film in films:
            self.liste_films.insert(tk.END, str(film))
        # En faisant double clic sur un film, affiche ses acteurs (Exigence. Voir les acteurs via infobulle ou autre)
        self.liste_films.bind("<Double-Button-1>", self.afficher_acteurs)

        # -- Boutons ---
        # Cadre por organiser les boutons horizontalement
        frame_boutons = tk.Frame(self)
        frame_boutons.pack(pady=10)
        # Bouton pour créer un niveau client
        tk.Button(frame_boutons, text="Nouveau Client", command=self.nouveau_client).pack(side=tk.LEFT, padx=5)
        # Bouton pour modifier un niveau client sélectionné
        tk.Button(frame_boutons, text="Modifier client", command=self.modifier_client).pack(side=tk.LEFT, padx=5)
        # Bouton pour supprimer un niveau client sélectionné
        tk.Button(frame_boutons, text="Supprimer client", command=self.supprimer_client).pack(side=tk.LEFT, padx=5)
        # Bouton pour se déconnecter
        tk.Button(frame_boutons, text="Déconnexion", command=self.deconnecter).pack(side=tk.LEFT, padx=5)

    def verifier_droits_ecriture(self) -> bool:
        """ Vérifie le niveau d'accès de la session en cours. Rejette  """
        if self.employe.est_lecture_seule():
            messagebox.showerror("Accès Refusé", "Action Interdite: votre profil est 'ACCÈS_LECTURE.'")
            return False
        return True

    def actualiser_liste_clients(self):
        """ Efface la liste visuelle et la remplit à nouveau avec les données mises à jour. """
        # Effectue un balayage de la Listbox, pour éviter les doublons visuels
        self.liste_clients.delete(0, tk.END)
        for client in clients:
            self.liste_clients.insert(tk.END, str(client))

    def nouveau_client(self):
        """ Permet la création d'un nouveau client.
        Bloque l'accès si l'utilisateur est en lecture. """
        if self.verifier_droits_ecriture():
            FenetreCreerClient(self)

    def modifier_client(self):
        """ Ouvre la fenêtre de modification pour le client sélectionné.
        Bloque l'accès si l'utilisateur est en lecture."""
        if not self.verifier_droits_ecriture():
            return
        # Reconnaît qu'un client est sélectionné dans la liste
        selection = self.liste_clients.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez un client!")
            return
        # Récupère l'index et ouvre la fenêtre de modification
        index = selection[0]
        FenetreModifierClient(self, clients[index])

    def supprimer_client(self):
        """ Supprime le client sélectionné après confirmation. Validation de sécurité et confirmation explicite. """
        if not self.verifier_droits_ecriture():
            return
        selection = self.liste_clients.curselection()
        # Empêche le programme de planter si rien n'est sélectionné
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez un client à supprimer!")
            return

        index = selection[0]
        client = clients[index]

        # -- Confirmation ---
        # Demande une confirmation avant de supprimer
        confirmer = messagebox.askyesno("Confirmation", f"Supprimer {client.get_prenom()}{client.get_nom()}?")

        if confirmer:
            # Supprime de la liste en memoire et de l'affichage
            clients.pop(index)
            self.liste_clients.delete(index)
            messagebox.showinfo("Succès", "Client supprimé!")

    def deconnecter(self):
        """ Ferme la fenêtre principale et affiche à nouveau le login. """
        # rend la fenêtre de Login visible à nouveau
        self.parent.deiconify()
        # Détruit l'instance actuelle de la fenêtre principale
        self.destroy()

    def afficher_acteurs(self, event):
        """ Affiche les acteurs du film sélectionné au doble clic."""
        selection = self.liste_films.curselection()
        if selection:
            index = selection[0]
            film = films[index]
            acteurs = film.get_acteurs_str()
            messagebox.showinfo("Acteurs", f"Film: {film.get_nom()}\n\n" f"Acteurs: {acteurs}")

# ________________________________________________________________
# Fenêtre : LOGIN
# ________________________________________________________________


class FenetreLogin(tk.Tk):
    """ Espace que permet la connexion des employées. Vérifie le code de l'utilisateur et le mot de passe.
     Donne l'accès selon son niveau : TOTAL ou LECTURE."""
    def __init__(self):
        # Permet initialiser la fenêtre principal Tkinter.
        super().__init__()

        # Titre principal qui apparait dans la barre de la fenêtre.
        self.title("Streaming RAC")

        # Dimensionne la taille fixe de la fenêtre (Larguer x hauteur)
        self.geometry("400x300")

        # Empêche l'utilisateur de redimensionner la taille de la fenêtre.
        self.resizable(False, False)

        # -- Titre ---
        # Affiche le nombre de l'application en gras.
        tk.Label(self, text="Streaming RAC", font=("Arial", 20, "bold")).pack(pady=20)

        # -- Champ: Code utilisateur ---
        # Étiquette le champ de saisie pour le code
        tk.Label(self, text="Code utilisateur:").pack()
        self.code_entry = tk.Entry(self)
        self.code_entry.pack(pady=5)

        # -- Champ : Mot de passe ---
        # show="*" facilite masquer les caractères saisis pour sécurité
        tk.Label(self, text="Mot de passe:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # -- Button connexion ---
        # En faisant clic, appelle la méthode connecter()
        tk.Button(self, text="Se connecter", command=self.connecter).pack(pady=20)

    def connecter(self):
        """" Constate l'information d'accès de l'employé.
        Si l'information est valide ouvre la fenêtre principale.
        Si l'information est incorrecte affiche un message d'erreur. """

        # Récupère le texte saisi par l'utilisateur
        code = self.code_entry.get()
        password = self.password_entry.get()

        # Validation de présence, évite de parcourir la liste si les champs sont vides
        if not code or not password:
            messagebox.showwarning("Champs vides", "Veuillez saisir votre code et votre mot de passe.")
            return

        # Parcourt la liste des employés pour examiner.
        for employe in employes:
            if employe.valider_connexion(code, password):
                # Cache la fenêtre login
                self.withdraw()
                # Ouvre la fenêtre principale
                FenetrePrincipale(self, employe)
                return
        # Si aucun employé corresponde s'affiche un message d'erreur
        messagebox.showerror("Erreur d'authentification ", "Code utilisateur ou mot de passe invalide!")


# -- Lancement de l'application ---
if __name__ == "__main__":
    app = FenetreLogin()
    app.mainloop()





