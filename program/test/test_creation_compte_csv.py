import csv
import random
import string

class CompteBancaire:
    comptes_existant_ids = set()
    cartes_existant_ids = set()

    def __init__(self, user_name, user_family_name):
        self.identifiant = self.generer_compte_unique()
        self.user_name = user_name
        self.user_family_name = user_family_name
        self.solde = round(random.uniform(100, 10000), 2)
        self.a_carte = random.choice([True, False])
        if (self.a_carte):
            self.generer_carte()

    def generer_compte_unique(self):
        identifiant = ''.join(random.choices(string.digits, k=10))
        while identifiant in CompteBancaire.comptes_existant_ids:
            identifiant = ''.join(random.choices(string.digits, k=10))
        CompteBancaire.comptes_existant_ids.add(identifiant)
        return identifiant

    def generer_carte_unique(self):
        carte_identifiant = ''.join(random.choices(string.digits, k=16))
        while carte_identifiant in CompteBancaire.cartes_existant_ids:
            carte_identifiant = ''.join(random.choices(string.digits, k=16))
        CompteBancaire.cartes_existant_ids.add(carte_identifiant)
        return carte_identifiant

    def generer_carte(self):
        self.carte_identifiant = self.generer_carte_unique()
        jour = random.randint(1, 28)
        mois = random.randint(1, 12)
        self.expiration_date = f"{jour:02}/{mois:02}"
        self.CVV = f"{random.randint(101, 999):03}"

    def to_dict(self):
        return {
            "Identifiant": self.identifiant,
            "Nom": self.user_family_name,
            "Prénom": self.user_name,
            "Solde": self.solde,
            "Carte Présente": "Oui" if self.a_carte else "Non",
            "Carte Identifiant": self.carte_identifiant if self.a_carte else "",
            "Date d'Expiration": self.expiration_date if self.a_carte else "",
            "CVV": self.CVV if self.a_carte else ""
        }

def creer_comptes_depuis_fichier(nom_fichier, nom_fichier_sortie):
    comptes = []
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                nom = row['Nom']
                prenom = row['Prenom']
                compte = CompteBancaire(prenom, nom)
                comptes.append(compte)
                
        with open(nom_fichier_sortie, 'w',  newline='') as csvfile:
            fieldnames = ["Identifiant", "Nom", "Prénom", "Solde", "Carte Présente", "Carte Identifiant", "Date d'Expiration", "CVV"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for compte in comptes:
                writer.writerow(compte.to_dict())
                
    except FileNotFoundError:
        print(f"Erreur: le fichier '{nom_fichier}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")

# Chemin vers le fichier clients.csv
nom_fichier = r'program\clients.csv'
nom_fichier_sortie = r'program\comptes_crees.csv'
creer_comptes_depuis_fichier(nom_fichier, nom_fichier_sortie)
