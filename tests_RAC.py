# ______________________________________________________________
# FICHIER : Tests_RAC.py
# DESCRIPTION : Essais unitaires - Lab Python
# AUTEUR : Miguel Andrade
# DATE : 28 d'avril 2026
# _______________________________________________________________

import unittest
from datetime import date
from models import Personne, Client, Employe, CarteCredit, Film, Categorie, Acteur

# _______________________________________________________________
# TESTS : Client


class TestClient(unittest.TestCase):
    """ Tests unitaires pour la classe Client. """

    def setUp(self):
        """ Crée un client de test avant chaque test."""
        self.client = Client("Andrade", "Miguel", "M", date(2023, 1, 10), "enmen80@fivemail.com", "Moliword11")

    def test_courriel_valide(self):
        """ Vérifie qu'un courriel valide est acepté."""
        self.assertTrue(Client.valider_courriel("test@fivemail.com"))

    def test_courriel_invalide(self):
        """Vérifie qu'un courriel invalide est rejeté."""
        self.assertFalse(Client.valider_courriel("enmen80@"))

    def test_password_valide(self):
        """ Vérifie qu'un mot de passe de 8 caractères est acepté. """
        self.assertTrue(Client.valider_password("12345678"))

    def test_password_invalide(self):
        """ Vérifie qu'un mot de passe court est rejeté. """
        self.assertFalse(Client.valider_password("abc"))

    def test_get_nom(self):
        """ Vérifie que get_nom retourne le bon nom. """
        self.assertEqual(self.client.get_nom(), "Andrade")

    def test_get_courriel(self):
        """ Vérifie que get_courriel retourne le bon courriel."""
        self.assertEqual(self.client.get_courriel(), "enmen80@fivemail.com")

    def test_ajouter_carte(self):
        """ Vérifie qu'on peut ajouter une carte de crédit."""
        carte = CarteCredit("4534453445344534", date(2028, 3, 14), "606")
        self.client.ajouter_carte(carte)
        self.assertEqual(len(self.client.get_cartes()), 1)

# ___________________________________________________________________________
# TESTS : Employe


class TestEmploye(unittest.TestCase):
    """ Test unitaire pour la classe Employe.  """

    def setUp(self):
        """ Crée un employé de test avant chaque test."""
        self.employe = Employe("Stevenson", "Dane", "F", date(2019, 3, 17), "admin23", "Admin1234", Employe.ACCES_TOTAL)

    def test_connexion_valide(self):
        """ Vérifie que'une connexion invalide est acceptée."""
        self.assertTrue(self.employe.valider_connexion("admin23", "Admin1234"))

    def test_connexion_invalide(self):
        """ Vérifie que'une connexion invalide est rejetée."""
        self.assertFalse(self.employe.valider_connexion("admin23", "dernierpassword"))

    def test_acces_total(self):
        """ Vérifie que l'employe n'est pas lecture seule. """
        self.assertFalse(self.employe.est_lecture_seule())

    def test_acces_lecture(self):
        """ Vérifie qu'un employe lecture seule est detecté."""
        emp_lecture = Employe("Smith", "Paul", "M", date(2020, 11, 28), "lesion12", "Lecture12345", Employe.ACCES_LECTURE)
        self.assertTrue(emp_lecture.est_lecture_seule())

# ____________________________________________________________________________________
# TEST : Film


class TestFilm(unittest.TestCase):
    """ Tests unitaires pour la classe Film."""

    def setUp(self):
        """ Créée un film de test avant chaque test."""
        self.film = Film("Interstellar", 169, "Une histoire futuriste")
        self.categorie = Categorie("Drame", "Collection des films dramatiques")
        self.acteur = Acteur("McConaughey", "Matthew", "M", "Cooper", date(2013, 1, 1), date(2015, 12, 31), 3000000.0)

    def test_ajouter_categorie(self):
        """ Vérifie qu'on peut ajouter une catégorie."""
        self.film.ajouter_categorie(self.categorie)
        self.assertEqual(len(self.film.get_categories()), 1)

    def test_ajouter_acteur(self):
        """ Vérifie qu'on peut ajouter un acteur."""
        self.film.ajouter_acteur(self.acteur)
        self.assertEqual(len(self.film.get_acteurs()), 1)

    def test_get_nom(self):
        """ Vérifie que get_nom retourne le bon titre."""
        self.assertEqual(self.film.get_nom(), "Interstellar")

    def test_get_duree(self):
        """ Vérifie que la duration du film est correct."""
        self.assertEqual(self.film.get_duree(), 169)

# _____________________________________________________________________________________
# TESTS : CarteCredit


class TestCarteCredit(unittest.TestCase):
    """ Tests unitaires pour la classe Carte Credit."""

    def test_carte_valide(self):
        """ Vérifie qu'une carte non expirée est valide."""
        carte = CarteCredit("4534453445344534", date(2028, 3, 14), "606")
        self.assertFalse(carte.est_expiree())

    def test_carte_expire(self):
        """ Vérifie qu'une carte expirée est détectée."""
        carte = CarteCredit("4534453445344534", date(2021, 1, 2), "606")
        self.assertTrue(carte.est_expiree())

    def test_numero_masque(self):
        """ Vérifie que le numéro est bien masqué."""
        carte = CarteCredit("4534453445344534", date(2028, 3, 14), "606")
        self.assertIn("4534", carte.get_numero_masque())


# -- Lancement des tests ---


if __name__ == "__main__":
    unittest.main(verbosity=2)

