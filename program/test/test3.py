import csv
import random
import string

class CompteBancaire:
    comptes_existant_ids = set()  # Ensemble pour stocker les identifiants de compte existants
    cartes_existant_ids = set()   # Ensemble pour stocker les identifiants de carte existants

    def __init__(self, user_name, user_family_name):
        self.identifiant = self.generer_compte_unique()
        self.user_name = user_name
        self.user_family_name = user_family_name
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

def creer_comptes_depuis_fichier(nom_fichier):
    comptes = []
    try:
        with open(nom_fichier, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            
            # Traitement des lignes pour créer les comptes
            csvfile.seek(0)  # Réinitialisation du curseur de fichier
            next(reader)  # Ignorer l'en-tête si nécessaire
            for row in reader:
                nom = row['Nom']
                prenom = row['Prenom']
                compte = CompteBancaire(nom, prenom)
                comptes.append(compte)
    except FileNotFoundError:
        print(f"Erreur: le fichier '{nom_fichier}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")
    
    return comptes

def main():
    nom_fichier = r'program\clients.csv'
    comptes_crees = creer_comptes_depuis_fichier(nom_fichier)
    
    # Affichage des identifiants des comptes créés
    for idx, compte in enumerate(comptes_crees, start=1):
        print(f"Compte {idx}:")
        print(f"  Nom: {compte.user_family_name}")
        print(f"  Prénom: {compte.user_name}")
        print(f"  Identifiant: {compte.identifiant}")
        print(f"  Carte Identifiant: {compte.carte_identifiant}")
        print(f"  Date d'expiration: {compte.expiration_date}")
        print(f"  CVV: {compte.CVV}")
        print()

if __name__ == "__main__":
    main()
