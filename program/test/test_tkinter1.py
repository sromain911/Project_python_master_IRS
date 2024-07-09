import tkinter as tk

# Fonction pour afficher le solde du compte
def afficher_solde():
    # Code pour afficher le solde du compte
    pass

# Fonction pour afficher les cartes bancaires
def afficher_cartes():
    # Code pour afficher les cartes bancaires
    pass

# Fonction pour effectuer un paiement en ligne
def paiement_en_ligne():
    # Code pour effectuer un paiement en ligne
    pass

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Accueil Compte Banque")

# Ajout d'un label pour le titre
label_titre = tk.Label(fenetre, text="Accueil Compte Banque", font=("Arial", 18, "bold"))
label_titre.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

# Création des boutons
bouton_accueil = tk.Button(fenetre, text="Accueil", command=fenetre.destroy)
bouton_visualiser_comptes = tk.Button(fenetre, text="Visualisation des comptes", command=afficher_solde)
bouton_visualiser_cartes = tk.Button(fenetre, text="Visualisation des cartes", command=afficher_cartes)
bouton_paiement_en_ligne = tk.Button(fenetre, text="Payer en ligne", command=paiement_en_ligne)

# Disposition des boutons en colonne
bouton_accueil.grid(row=1, column=0, padx=5, pady=5)
bouton_visualiser_comptes.grid(row=2, column=0, padx=5, pady=5)
bouton_visualiser_cartes.grid(row=3, column=0, padx=5, pady=5)
bouton_paiement_en_ligne.grid(row=4, column=0, padx=5, pady=5)

# Centrage des boutons
fenetre.columnconfigure(0, weight=1)

# Exécution de l'interface graphique
fenetre.mainloop()