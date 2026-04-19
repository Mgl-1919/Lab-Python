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