from abc import ABC, abstractmethod
from datetime import date

class Personne(ABC):
    """ Classe abstraite pour le sous-classe Client, Acteur, Employée. Ne peut être instanciée directement (ABC). Contient les informations de base: nom, prenom, sexe """
    def __init__(self, nom: str, prenom: str, sexe: str):
        self._nom = nom.strip()
        self._prenom = prenom.strip()
        self._sexe = sexe.strip()

    def get_nom(self) -> str: return self._nom   # Retourne le nom de famille
    def get_prenom(self) -> str: return self._prenom  # Retourne le prénom
    def get_sexe(self) -> str: return self._sexe  # Retourne le sexe

    @abstractmethod
    def __str__(self) -> str:
        pass


class CarteCredit:
    """  Conserve l'information de paiement du client. Les données confidentiels sont toujours masquées."""
    def __int__(self, numero_carte: str, date_expiration: date, code_secret: str):
        self.__numero_carte = numero_carte.strip()
        self.__date_expiration = date_expiration
        self.__code_secret = code_secret
    def get_numero_masque(self) -> str:
        return f"**** **** **** {self.__numero_carte[-4:]}"

    def est_expiree(self) -> bool:
        return self.__date_expiration < date.today()

    def __str__(self) -> str:
        statut = "EXPIRÉE" if self.est_expiree() else "Valide"
        return f"Carte: {self.get_numero_masque()} | {statut}"


class Client(Personne):
    """ Client abonnée au service de streaming. Hérite de Personne. """
    def __init__(self, nom: str, prenom: str, sexe: str, date_inscription: date, courriel: str, password: str):
        super().__init__(nom, prenom, sexe)
        self.__date_inscription = date_inscription
        self.__courriel = courriel.strip().lower()
        self.__password = password
        self.__cartes = []

    def get_courriel(self) -> str: return self.__courriel
    def get_date_inscription(self) -> date: return self.__date_inscription


    def ajouter_carte(self, carte: CarteCredit):
        self.__cartes.append(carte)

    def get_cartes(self) -> list: return list(self.__cartes)

    def __str__(self) -> str:
            return f"Client: {self._prenom} {self._nom} | Courriel: {self.__courriel}"


class Employe(Personne):
    """  Pour les employés qui utilisent régulièrement le système de gestion. Deux niveaux d'accès seront disponibles : TOTAL ou LECTURE. """
    ACCES_TOTAL = "TOTAL"
    ACCES_LECTURE = "LECTURE"

    def __int__(self, nom: str, prenom: str, sexe: str, date_embauche: date, code_utilisateur: str, password: str,
                type_acces: str):
        super().__init__(nom, prenom, sexe)
        self.__date_embauche = date_embauche
        self.__code_utilisateur = code_utilisateur.strip()
        self.__password = password
        self.__type_acces = type_acces
    def get_code_utilisateur(self) -> str: return self.__code_utilisateur
    def get_type_acces(self) -> str: return self.__type_acces
    def get_date_embauche(self) -> date: return self.__date_embauche

    def valider_connexion(self, code: str, password: str) -> bool: return ( code.strip() == self.__code_utilisateur and password == self.__password)
    def est_lecture_seule(self) -> bool: return self.__type_acces == self.ACCES_LECTURE
    def __str__(self) -> str: return f"Employe: {self._prenom} {self._nom} | Acces: {self.__type_acces}"


class Acteur(Personne):
    """   Acteur extraordinaire ayant participé à de nombreux films de genres variés. Hérite de Personne.  """
    def __init__(self, nom: str, prenom: str, sexe: str, nom_personnage: str, debut_emploi: date, fin_emploi: date, salaire: float):
        super().__init__(nom, prenom, sexe)
        self.__nom_personnage = nom_personnage
        self.__debut_emploi = debut_emploi
        self.__fin_emploi = fin_emploi
        self.__salaire = salaire

    def get_nom_personnage(self) -> str: return self.__nom_personnage
    def get_debut_emploi(self) -> date: return self.__debut_emploi
    def get_fin_emploi(self) -> date: return self.__fin_emploi
    def get_salaire(self) -> float: return self.__salaire

    def __str__(self) -> str: return f"Acteur : {self._prenom} {self._nom} | " f"Personnage: {self.__nom_personnage}"

