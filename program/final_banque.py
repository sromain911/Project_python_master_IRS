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

class InterfaceBanque:
    def __init__(self, root, comptes):
        self.root = root
        self.comptes = comptes
        self.root.title("Accueil Compte Banque")

        # Ajout d'un label pour le titre
        label_titre = tk.Label(self.root, text="Accueil Compte Banque", font=("Arial", 18, "bold"))
        label_titre.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Création des boutons
        bouton_visualiser_comptes = tk.Button(self.root, text="Visualisation des comptes", command=self.afficher_liste_comptes)
        bouton_visualiser_cartes = tk.Button(self.root, text="Visualiser des cartes", command=self.afficher_liste_cartes)
        bouton_payer = tk.Button(self.root, text="Payer", command=self.payer)
        bouton_quitter = tk.Button(self.root, text="Quitter", command=self.root.destroy)

        # Disposition des boutons en colonne
        bouton_visualiser_comptes.grid(row=1, column=0, padx=5, pady=5)
        bouton_visualiser_cartes.grid(row=2, column=0, padx=5, pady=5)
        bouton_payer.grid(row=3, column=0, padx=5, pady=5)
        bouton_quitter.grid(row=4, column=0, padx=5, pady=5)

        # Centrage des boutons
        self.root.columnconfigure(0, weight=1)

    def afficher_liste_comptes(self):
        fenetre_liste_comptes = tk.Toplevel(self.root)
        fenetre_liste_comptes.title("Liste des Comptes Bancaires")

        tree = ttk.Treeview(fenetre_liste_comptes, columns=("Numéro de Compte", "Propriétaire du Compte", "Solde", "Carte"))
        tree.heading("#0", text="Numéro")
        tree.heading("Numéro de Compte", text="Numéro de Compte")
        tree.heading("Propriétaire du Compte", text="Propriétaire du Compte")
        tree.heading("Solde", text="Solde")
        tree.heading("Carte", text="Carte")

        for idx, compte in enumerate(self.comptes, start=1):
            carte_presente = "Oui" if compte.has_carte() else "Non"
            tree.insert("", tk.END, text=str(idx), values=(compte.get_identifiant(), f"{compte.get_user_family_name()} {compte.get_user_name()}", f"{compte.get_solde()} EUR", carte_presente))

        tree.pack(expand=True, fill="both")

    def afficher_liste_cartes(self):
        fenetre_liste_cartes = tk.Toplevel(self.root)
        fenetre_liste_cartes.title("Liste des Cartes Bancaires")

        tree = ttk.Treeview(fenetre_liste_cartes, columns=("Numero de Carte", "Propriétaire de la carte", "Date d'expiration", "CVV"))
        tree.heading("#0", text="Numero")
        tree.heading("Propriétaire de la carte", text="Propriétaire de la carte")
        tree.heading("Date d'expiration", text="Date d'expiration")
        tree.heading("CVV", text="CVV")

        for idx, compte in enumerate(self.comptes, start=1):
            if compte.has_carte():
                tree.insert("", tk.END, text=str(idx), values=(compte.get_carte(), f"{compte.get_user_family_name()} {compte.get_user_name()}", f"{compte.get_expdate()}", f"{compte.get_CVV()}"))

        tree.pack(expand=True, fill="both")

    def payer(self):
        fenetre_payer = tk.Toplevel(self.root)
        fenetre_payer.title("Payer")

        label_somme = tk.Label(fenetre_payer, text="Somme à payer :")
        label_somme.pack(padx=20, pady=5)
        spinbox = tk.Spinbox(fenetre_payer, from_=0, to=100000)
        spinbox.pack(padx=20, pady=5)

        def valider_et_ouvrir():
            somme = float(spinbox.get())
            fenetre_payer.destroy()
            self.ouvrir_fenetre_paiement(somme)

        bouton_valider = tk.Button(fenetre_payer, text="Valider", command=valider_et_ouvrir)
        bouton_valider.pack(pady=10)

    def ouvrir_fenetre_paiement(self, somme):
        fenetre_paiement = tk.Toplevel(self.root)
        fenetre_paiement.title("Informations de Paiement")

        label_numero_carte = tk.Label(fenetre_paiement, text="Numéro de carte :")
        label_numero_carte.grid(row=0, column=0, padx=10, pady=5)
        entry_numero_carte = tk.Entry(fenetre_paiement)
        entry_numero_carte.grid(row=0, column=1, padx=10, pady=5)

        label_nom_prenom = tk.Label(fenetre_paiement, text="Nom Prénom du titulaire :")
        label_nom_prenom.grid(row=1, column=0, padx=10, pady=5)
        entry_nom_prenom = tk.Entry(fenetre_paiement)
        entry_nom_prenom.grid(row=1, column=1, padx=10, pady=5)

        label_date_expiration = tk.Label(fenetre_paiement, text="Date d'expiration :")
        label_date_expiration.grid(row=2, column=0, padx=10, pady=5)
        entry_date_expiration = tk.Entry(fenetre_paiement)
        entry_date_expiration.grid(row=2, column=1, padx=10, pady=5)

        label_cvv = tk.Label(fenetre_paiement, text="CVV :")
        label_cvv.grid(row=3, column=0, padx=10, pady=5)
        entry_cvv = tk.Entry(fenetre_paiement)
        entry_cvv.grid(row=3, column=1, padx=10, pady=5)

        def valider_paiement():
            numero_carte = entry_numero_carte.get()
            nom_prenom = entry_nom_prenom.get()
            date_expiration = entry_date_expiration.get()
            cvv = entry_cvv.get()

            for compte in self.comptes:
                if compte.has_carte() and compte.get_carte() == numero_carte and compte.get_expdate() == date_expiration and compte.get_CVV() == cvv:
                    if somme <= compte.get_solde():
                        compte.solde = round(compte.get_solde() - somme, 2)
                        messagebox.showinfo("Succès", f"Paiement de {somme} EUR réussi pour {nom_prenom}.")
                        fenetre_paiement.destroy()
                        return
                    else:
                        messagebox.showerror("Erreur", "Solde insuffisant.")
                        return
            messagebox.showerror("Erreur", "Informations de carte incorrectes.")

        bouton_valider = tk.Button(fenetre_paiement, text="Valider le paiement", command=valider_paiement)
        bouton_valider.grid(row=4, column=0, columnspan=2, pady=10)

def main():
    nom_fichier = r'program\clients.csv'
    comptes_crees = creer_comptes_depuis_fichier(nom_fichier)

    root = tk.Tk()
    app = InterfaceBanque(root, comptes_crees)
    root.mainloop()

if __name__ == "__main__":
    main()
