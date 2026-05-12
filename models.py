# _________________________________________________________________________________
#  FICHIER : models.py
#  DESCRIPTION : Création du diagramme des classes et utilisation des principes orientés objet.
#  Auteur : Miguel Andrade
#  DATE : 28 d'avril 2026
# __________________________________________________________________________________

from abc import ABC, abstractmethod
from datetime import date
import re


class Personne(ABC):
    """ Classe abstraite (ABC) agissant comme superclasse pour Client, Acteur et Employée.
    Ne peut être instanciée directement.
    Contient les informations de basse : nom, prenom, sexe """
    def __init__(self, nom: str, prenom: str, sexe: str) -> object:
        # Le .strip() enlève automatiquement les espaces inutiles tapées par erreurs
        self._nom = nom.strip()
        self._prenom = prenom.strip()
        self._sexe = sexe.strip()

    # -- Fonctions pour récupérer les informations de manière propre ---
    def get_nom(self) -> str: return self._nom   # Retourne le nom de famille
    def get_prenom(self) -> str: return self._prenom  # Retourne le prénom
    def get_sexe(self) -> str: return self._sexe  # Retourne le sexe

    # -- Fonctions pour modifier les informations en toute sécurité ---
    def set_nom(self, nom: str):
        # Permet de changer le nom
        self._nom = nom.strip()

    def set_prenom(self, prenom: str):
        self._prenom = prenom.strip()

    def set_sexe(self, sexe: str):
        self._sexe = sexe.strip()

    @abstractmethod
    def __str__(self) -> str:
        """ Cette fonction obligera chaque enfant (Client, Employé, etc.) à définir comment s'afficher en texte."""
        pass


class CarteCredit:
    """  Conserve l'information de paiement du client. Les données confidentielles sont toujours masquées."""
    def __init__(self, numero_carte: str, date_expiration: date, code_secret: str):
        self.__numero_carte = numero_carte.strip()
        self.__date_expiration = date_expiration
        self.__code_secret = code_secret

    def get_numero_masque(self) -> str:
        """ Cache le numéro de la carte crédit pour des raisons de sécurité. Ne montre que les 4 dernières chiffres. """
        return f"**** **** **** {self.__numero_carte[-4:]}"

    def est_expiree(self) -> bool:
        """ Vérifie si la carte crédit est encore utilisable en la comparant avec la date actuelle."""
        # Retorne Vrai si la carte est expire
        return self.__date_expiration < date.today()

    def __str__(self) -> str:
        """ Affiche un résumé simple de la carte crédit à l'écran avec son statut. """
        statut = "EXPIRÉE" if self.est_expiree() else "Valide"
        return f"Carte: {self.get_numero_masque()} | {statut}"


class Client(Personne):
    """ Client abonné au service de streaming. Hérite de Personne. """
    def __init__(self, nom: str, prenom: str, sexe: str, date_inscription: date, courriel: str, password: str):
        # Envoie le nom, prénom et sexe à la classe de base Personne
        super().__init__(nom, prenom, sexe)
        # Garde la date d'inscription du client
        self.__date_inscription = date_inscription
        # Enregistre le courriel en lettres minuscules pour éviter les doublons
        self.__courriel = courriel.strip().lower()
        # Conserve le mot de passe du client
        self.__password = password
        # Liste vide qui contiendra les cartes de crédit du client
        self.__cartes = []

    # -- Fonctions de vérification rapides (staticmethod) ---
    @staticmethod
    def valider_courriel(courriel: str) -> bool:
        """  Vérifie le format du courriel avec regex."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return bool(re.match(pattern, courriel))

    @staticmethod
    def valider_password(password: str) -> bool:
        """ Vérifie que le mot de passe a 8 caractères minimum."""
        return len(password) >= 8

    # -- Fonctions pour lire et modifier les données spécifiques du client ---

    def get_courriel(self) -> str: return self.__courriel
    def get_date_inscription(self)  -> date: return self.__date_inscription

    def set_courriel(self, courriel: str):
        self.__courriel = courriel.strip().lower()

    # -- Gestion des Cartes ---
    def ajouter_carte(self, carte: CarteCredit):
        """ Ajout une nouvelle carte de crédit à la liste du client. """
        self.__cartes.append(carte)

    def get_cartes(self) -> list:
        """ Donne la liste des cartes associées au client. """
        return list(self.__cartes)

    def __str__(self) -> str:
        # Façon standard d'afficher un client dans la liste de la fenêtre principale
        return (f"Client: {self._prenom} {self._nom} | "
                f"Courriel: {self.__courriel}")


class Employe(Personne):
    """  Pour les employés qui utilisent régulièrement le système de gestion.
    Deux niveaux d'accès seront disponibles : TOTAL ou LECTURE. """
    ACCES_TOTAL = "TOTAL"
    ACCES_LECTURE = "LECTURE"
    def __init__(self, nom: str, prenom: str, sexe: str, date_embauche: date,
                 code_utilisateur: str, password: str, type_acces: str):
        # Transmet les informations de base à la classe Personne
        super().__init__(nom, prenom, sexe)
        self.__date_embauche = date_embauche
        self.__code_utilisateur = code_utilisateur.strip()
        self.__password = password
        # Détermine le profil de privilèges (TOTAL ou LECTURE)
        self.__type_acces = type_acces

    def get_code_utilisateur(self) -> str: return self.__code_utilisateur
    def get_type_acces(self) -> str: return self.__type_acces
    def get_date_embauche(self) -> date: return self.__date_embauche

    def valider_connexion(self, code: str, password: str) -> bool:
        # Compare si le code et le mot de passe tapés sont corrects
        return (code.strip() == self.__code_utilisateur and password == self.__password)

    def est_lecture_seule(self) -> bool:
        """ Vérifie si l'employé a un profil limité (ACCÈS_LECTURE)"""
        return self.__type_acces == self.ACCES_LECTURE

    def __str__(self) -> str:

        return f"Employe: {self._prenom} {self._nom} | Acces: {self.__type_acces}"


class Acteur(Personne):
    """   Acteur extraordinaire ayant participé à de nombreux films de genres variés. Hérite de Personne.  """
    def __init__(self, nom: str, prenom: str, sexe: str, nom_personnage: str, debut_emploi: date, fin_emploi: date, salaire: float):
        super().__init__(nom, prenom, sexe)
        # Nom du rôle fictif au sein du film
        self.__nom_personnage = nom_personnage
        # Date de début de son contrat
        self.__debut_emploi = debut_emploi
        # Date de fin de son contrat
        self.__fin_emploi = fin_emploi
        # Salaire de l'acteur (information privée)
        self.__salaire = salaire

    # -- Fonctions pour lire les details du contrat de l'acteur ---
    def get_nom_personnage(self) -> str: return self.__nom_personnage
    def get_debut_emploi(self) -> date: return self.__debut_emploi
    def get_fin_emploi(self) -> date: return self.__fin_emploi
    def get_salaire(self) -> float: return self.__salaire

    def __str__(self) -> str: return f"Acteur : {self._prenom} {self._nom} | " f"Personnage: {self.__nom_personnage}"


class Categorie:
    """ Catégorie de films, parmi ceux-ci se distinguent: Drame, Comédie, Action etc. """
    def __init__(self, nom: str, description: str):
        self.__nom = nom.strip()
        self.__description = description.strip()

    def get_nom(self) -> str: return self.__nom
    def get_description(self) -> str: return self.__description

    def __str__(self) -> str: return f"Catégorie: {self.__nom} - {self.__description}"


class Film:
    """ Ici on peut trouver les Catégories des films disponibles sur la plateforme de streaming,
    même plusieurs acteurs. """

    def __init__(self, nom: str, duree: int, description: str):
        self.__nom = nom.strip()
        # Durée du film stockée en minutes (Nombre entier)
        self.__duree = duree
        self.__description = description.strip()
        # Liste contenant les genres associés au film
        self.__categories = []
        # Liste contenant les acteurs qui jouent dans ce film
        self.__acteurs = []

    # -- Fonctions pour lier des éléments au film ---
    def ajouter_categorie(self, categorie: Categorie):
        self.__categories.append(categorie)

    def ajouter_acteur(self, acteur: Acteur):
        self.__acteurs.append(acteur)

    # -- Fonctions pour lire les informations du film ---
    def get_nom(self) -> str: return self.__nom
    def get_duree(self) -> int: return self.__duree
    def get_description(self) -> str: return self.__description
    def get_categories(self) -> list: return list(self.__categories)
    def get_acteurs(self) -> list: return list(self.__acteurs)

    def get_categories_str(self) -> str:
        """ Rassemble les noms de toutes les catégories du film pour les afficher proprement séparés. """
        return ", ".join(c.get_nom() for c in self.__categories)

    def get_acteurs_str(self) -> str:
        """ Crée une liste textuelle des acteurs. Utilisé pour la boîte de message lors d'un double-clic. """
        return ", ".join(f"{a.get_prenom()} {a.get_nom()}" for a in self.__acteurs)

    def __str__(self) -> str:
        """ Façon d'afficher le film complet (Titre, durée et genres) dans l'interface visuelle. """
        return f"Film: {self.__nom} | Durée: {self.__duree} min | {self.get_categories_str()}"

    # ___________________________
    # Données de démonstration


def charger_donnees():

    """ Creé et retourne des données de démonstration qui vérifient que l'application fonctionne."""
    # -- Employés ---
    employes = [
    Employe("Stevenson", "Danne", "F", date(2019, 3, 17), "admin23", "Admin1234", Employe.ACCES_TOTAL),
    Employe("Smith", "Paul", "M", date(2020, 11, 28), "lesion12", "Patates12345", Employe.ACCES_LECTURE),
    ]

    # -- Catégories ---
    action = Categorie("Action", "Catalogue des films d'action")
    comedie = Categorie("Comédie", "Répertoire des films drôles et divertissants")
    drame = Categorie("Drame", "Collection des films dramatiques")
    fiction = Categorie("Fiction ", " Collection des films de science - fiction ")
    horreur = Categorie("Terreur", " Films terrifiants et glaçants ")

    # -- Acteurs ---
    acteur1 = Acteur("McConaughey", "Matthew", "M", "Cooper", date(2013, 1, 1), date(2015, 12, 31), 3000000.0)
    acteur2 = Acteur("Cruise", "Tom ", "M", "Ethan", date(2023, 1, 1), date(2025, 12, 31), 5500000.0)
    acteur3 = Acteur("Isaac", "Oscar", "M", "Victor", date(2024, 2, 2), date(2025, 12, 11), 10000000.0 )
    acteur4 = Acteur("Ferdane", "Marie-Sophie", "F", "Alexandra", date(2016, 2, 3), date(2018, 2, 4), 2500000.0)
    # -- Films ---
    film1 = Film("Interstellar", 169, "Une histoire futuriste")
    film1.ajouter_categorie(drame)
    film1.ajouter_acteur(acteur1)

    film2 = Film("Mission Impossible", 170, "Une séquence d'espionnage")
    film2.ajouter_categorie(action)
    film2.ajouter_acteur(acteur2)

    film3 = Film("Frankestein", 132, "Un film d'horreur gothique américain")
    film3.ajouter_categorie(horreur)
    film3.ajouter_acteur(acteur3)

    film4 = Film("Je ne suis pas un homme facile", 98, "Comédie romantique et drôle.")
    film4.ajouter_categorie(comedie)
    film4.ajouter_acteur(acteur4)

    films = [film1, film2, film3, film4]

    # -- Clients ---
    client1 = Client("Marx", "Line", "F", date(2025, 2, 11), "marlix12@tmail.com", "Soleil12")
    client1.ajouter_carte(CarteCredit("4534453445344534", date(2028, 3, 14), "606"))

    client2 = Client("Dallas", "Jhon", "M", date(2024, 1, 4), "team67@xmail.com", "Passer34")
    clients = [client1, client2]

    return employes, clients, films

