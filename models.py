from abc import ABC, abstractmethod
from datetime import date

class Personne(ABC):
    def __init__(self, nom: str, prenom: str, sexe: str):
        self._nom = nom.strip()
        self._prenom = prenom.strip()
        self._sexe = sexe.strip()

    def get_nom(self) -> str: return self._nom
    def get_prenom(self) -> str: return self._prenom
    def get_sexe(self) -> str: return self._sexe

    @abstractmethod
    def __str__(self) -> str:
        pass


class CarteCredit:
    """  Conserve l'information de paiement du client. Les données confidentiels sont toujours masquées.
    """
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

