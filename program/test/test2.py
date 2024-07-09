import csv
import random
import string

class CompteBancaire:
    def __init__(self, user_name, user_family_name):
        self.identifiant = self.generer_compte()
        self.user_name = user_name
        self.user_family_name = user_family_name
        self.generer_carte()
    
    def generer_compte(self):
        return ''.join(random.choices(string.digits, k=10))

    def generer_carte(self):
        self.carte_identifiant = ''.join(random.choices(string.digits, k=16))
        jour = random.randint(1, 28)
        mois = random.randint(1, 12)
        self.expiration_date = f"{jour:02}/{mois:02}"
        self.CVV = f"{random.randint(101, 999):03}"

def creer_comptes_depuis_fichier(nom_fichier):
    comptes = []
    with open(nom_fichier, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            nom = row['Nom']
            prenom = row['Prenom']
            compte = CompteBancaire(nom, prenom)
            comptes.append(compte)
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
