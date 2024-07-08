import random
import string

class CompteBancaire:
    def __init__(self, solde_initial):
        self.numero_compte = self.generer_numero_compte()
        self.solde = solde_initial
        self.carte_associee = None

    def generer_numero_compte(self):
        return ''.join(random.choices(string.digits, k=10))

    def lier_carte(self, carte):
        self.carte_associee = carte

class CarteBancaire:
    def __init__(self, titulaire, date_expiration, cvv):
        self.numero_carte = self.generer_numero_carte()
        self.titulaire = titulaire
        self.date_expiration = date_expiration
        self.cvv = cvv
        self.compte_associe = None

    def generer_numero_carte(self):
        return ''.join(random.choices(string.digits, k=16))

    def lier_compte(self, compte):
        self.compte_associe = compte
