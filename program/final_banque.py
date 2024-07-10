import tkinter as tk
from tkinter import ttk, messagebox
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
        self.solde = round(random.uniform(100, 10000), 2)  # Montant aléatoire pour le solde
        self.a_carte = random.choice([True, False])  # Choix aléatoire de la présence de carte
        if self.a_carte:
            self.generer_carte()

        # Affichage dans la console lors de la création du compte
        print(f"Création du compte pour {self.user_family_name} {self.user_name}.")
        print(f"  Identifiant: {self.identifiant}")
        print(f"  Solde: {self.solde} EUR")
        if self.a_carte:
            print(f"  Carte Identifiant: {self.carte_identifiant}")
            print(f"  Date d'expiration: {self.expiration_date}")
            print(f"  CVV: {self.CVV}")
        else:
            print("  Aucune carte associée.")
        print()

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

    def get_identifiant(self):
        return self.identifiant

    def get_user_name(self):
        return self.user_name

    def get_user_family_name(self):
        return self.user_family_name

    def get_solde(self):
        return self.solde

    def has_carte(self):
        return self.a_carte
    
    def get_carte(self):
        return self.carte_identifiant
    
    def get_expdate(self):
        return self.expiration_date
    
    def get_CVV(self):
        return self.CVV
    

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

def afficher_liste_comptes(comptes):
    # Création d'une nouvelle fenêtre pour afficher la liste des comptes
    fenetre_liste_comptes = tk.Toplevel()
    fenetre_liste_comptes.title("Liste des Comptes Bancaires")

    # Création du Treeview pour afficher les comptes
    tree = ttk.Treeview(fenetre_liste_comptes, columns=("Numéro de Compte", "Propriétaire du Compte", "Solde", "Carte"))
    tree.heading("#0", text="Numéro")
    tree.heading("Numéro de Compte", text="Numéro de Compte")
    tree.heading("Propriétaire du Compte", text="Propriétaire du Compte")
    tree.heading("Solde", text="Solde")
    tree.heading("Carte", text="Carte")

    # Ajout des données des comptes au Treeview
    for idx, compte in enumerate(comptes, start=1):
        carte_presente = "Oui" if compte.has_carte() else "Non"
        tree.insert("", tk.END, text=str(idx), values=(compte.get_identifiant(), f"{compte.get_user_family_name()} {compte.get_user_name()}", f"{compte.get_solde()} EUR", carte_presente))

    tree.pack(expand=True, fill="both")

def afficher_liste_cartes(comptes):
    # Création d'une nouvelle fenêtre pour afficher la liste des comptes
    fenetre_liste_cartes = tk.Toplevel()
    fenetre_liste_cartes.title("Liste des Cartes Bancaires")

    # Création du Treeview pour afficher les cartes
    tree = ttk.Treeview(fenetre_liste_cartes, columns=("Numero de Carte", "Propriétaire de la carte", "Date d'expiration", "CVV"))
    tree.heading("#0", text="Numero")
    tree.heading("Propriétaire de la carte", text="Propriétaire de la carte")
    tree.heading("Date d'expiration", text="Date d'expiration")
    tree.heading("CVV", text="CVV")

    # Ajout des données des comptes au Treeview
    for idx, compte in enumerate(comptes, start=1):
        if compte.has_carte():
            tree.insert("", tk.END, text=str(idx), values=(compte.get_carte(), f"{compte.get_user_family_name()} {compte.get_user_name()}", f"{compte.get_expdate()}", f"{compte.CVV}"))

    tree.pack(expand=True, fill="both")

def payer():
    # Création d'une nouvelle fenêtre pour afficher la liste des comptes
    fenetre_payer = tk.Toplevel()
    fenetre_payer.title("Payer")

    spinbox = tk.Spinbox(fenetre_payer, from_=0, to=100000)
    spinbox.pack(padx=20, pady=20)

    def valider_et_fermer():
        somme = spinbox.get()  # Récupère la valeur du Spinbox
        print(f"La somme sélectionnée est : {somme}")
        fenetre_payer.destroy()  # Ferme la fenêtre actuelle
        nouvelle_fenetre = tk.Tk()  # Ouvre une nouvelle fenêtre
        nouvelle_fenetre.title("Nouvelle Fenêtre")
        label = tk.Label(nouvelle_fenetre, text="Ceci est une nouvelle fenêtre.")
        label.pack()
        nouvelle_fenetre.mainloop()

    bouton_valider = tk.Button(fenetre_payer, text="Valider", command=valider_et_fermer)
    bouton_valider.pack(pady=10)

def main():
    nom_fichier = r'program\clients.csv'
    comptes_crees = creer_comptes_depuis_fichier(nom_fichier)
    
    # Affichage des identifiants des comptes créés dans la console
    for idx, compte in enumerate(comptes_crees, start=1):
        print(f"Compte {idx}:")
        print(f"  Nom: {compte.get_user_family_name()}")
        print(f"  Prénom: {compte.get_user_name()}")
        print(f"  Identifiant: {compte.get_identifiant()}")
        print(f"  Solde: {compte.get_solde()} EUR")
        if compte.has_carte():
            print(f"  Carte Identifiant: {compte.carte_identifiant}")
            print(f"  Date d'expiration: {compte.expiration_date}")
            print(f"  CVV: {compte.CVV}")
        else:
            print("  Aucune carte associée.")
        print()

    # Création de la fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("Accueil Compte Banque")
    
    # Ajout d'un label pour le titre
    label_titre = tk.Label(fenetre, text="Accueil Compte Banque", font=("Arial", 18, "bold"))
    label_titre.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    
    # Création des boutons
    bouton_accueil = tk.Button(fenetre, text="Accueil", command=fenetre.destroy)
    bouton_visualiser_comptes = tk.Button(fenetre, text="Visualisation des comptes", command=lambda: afficher_liste_comptes(comptes_crees))
    bouton_visualiser_cartes = tk.Button(fenetre, text="Visualiser des cartes", command=lambda: afficher_liste_cartes(comptes_crees))
    bouton_payer = tk.Button(fenetre, text="Payer", command=payer)
    
    # Disposition des boutons en colonne
    bouton_accueil.grid(row=1, column=0, padx=5, pady=5)
    bouton_visualiser_comptes.grid(row=2, column=0, padx=5, pady=5)
    bouton_visualiser_cartes.grid(row=3, column=0, padx=5, pady=5)
    bouton_payer.grid(row=4, column=0, padx=5, pady=5)
    
    # Centrage des boutons
    fenetre.columnconfigure(0, weight=1)
    
    # Exécution de l'interface graphique
    fenetre.mainloop()

if __name__ == "__main__":
    main()
