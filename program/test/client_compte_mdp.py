import socket
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib

# Paramètres du serveur
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
RETRY_LIMIT = 5

def send_request(account_id, account_name, hashed_password):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        request = f"{account_id};{account_name};{hashed_password}"  # Ajout du mot de passe hashé dans la requête
        retries = 0
        while retries < RETRY_LIMIT:
            try:
                client_socket.sendto(request.encode(), (SERVER_HOST, SERVER_PORT))
                client_socket.settimeout(5)  # Temps d'attente pour la réponse en secondes
                response, server_address = client_socket.recvfrom(1024)
                return response.decode()
            except socket.timeout:
                retries += 1
        return None

def handle_submit():
    global entry_account_id, entry_account_name, entry_password  # Déclaration globale des variables

    account_id = entry_account_id.get()
    account_name = entry_account_name.get()
    password = entry_password.get()  # Récupération du mot de passe saisi par l'utilisateur

    if not account_id or not account_name or not password:
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
        return

    # Hashage du mot de passe avec SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    response = send_request(account_id, account_name, hashed_password)

    if response:
        show_account_info(response)
    else:
        messagebox.showerror("Erreur", "Aucune réponse du serveur après plusieurs tentatives.")

def show_account_info(info):
    account_info = info.split(";")
    
    if len(account_info) < 8:
        messagebox.showerror("Erreur", "Réponse invalide du serveur")
        return

    # Création d'une nouvelle fenêtre pour afficher les informations du compte
    fenetre_info_compte = tk.Toplevel()
    fenetre_info_compte.title("Informations du Compte")

    # Création du cadre pour afficher les informations
    frame = ttk.Frame(fenetre_info_compte, padding="10")
    frame.grid(row=0, column=0, sticky="nsew")

    # Affichage des informations du compte
    labels = ["Numéro de Compte", "Nom", "Prénom", "Solde", "Carte Présente", "Carte Identifiant", "Date d'Expiration", "CVV"]
    for i, label_text in enumerate(labels):
        label = ttk.Label(frame, text=label_text, font=("Arial", 12, "bold"))
        label.grid(row=i, column=0, sticky="w", padx=5, pady=5)

        value = ttk.Label(frame, text=account_info[i], font=("Arial", 12))
        value.grid(row=i, column=1, sticky="w", padx=5, pady=5)

    # Redimensionnement des colonnes du cadre
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

def main():
    global entry_account_id, entry_account_name, entry_password  # Déclaration globale des variables

    fenetre_principale = tk.Tk()
    fenetre_principale.title("Client Compte Bancaire")

    # Création d'un cadre pour les entrées
    cadre_entrees = ttk.Frame(fenetre_principale, padding="10")
    cadre_entrees.grid(row=0, column=0, sticky="nsew")

    # Entrée pour le numéro de compte
    label_account_id = ttk.Label(cadre_entrees, text="Numéro de Compte:")
    label_account_id.grid(row=0, column=0, padx=5, pady=5)

    entry_account_id = ttk.Entry(cadre_entrees, width=30)
    entry_account_id.grid(row=0, column=1, padx=5, pady=5)

    # Entrée pour le nom du propriétaire
    label_account_name = ttk.Label(cadre_entrees, text="Nom du Propriétaire:")
    label_account_name.grid(row=1, column=0, padx=5, pady=5)

    entry_account_name = ttk.Entry(cadre_entrees, width=30)
    entry_account_name.grid(row=1, column=1, padx=5, pady=5)

    # Entrée pour le mot de passe
    label_password = ttk.Label(cadre_entrees, text="Mot de passe:")
    label_password.grid(row=2, column=0, padx=5, pady=5)

    entry_password = ttk.Entry(cadre_entrees, width=30, show="*")
    entry_password.grid(row=2, column=1, padx=5, pady=5)

    # Bouton pour valider la demande
    bouton_valider = ttk.Button(cadre_entrees, text="Valider", command=handle_submit)
    bouton_valider.grid(row=3, column=0, columnspan=2, pady=10)

    # Redimensionnement des colonnes du cadre d'entrées
    cadre_entrees.columnconfigure(1, weight=1)

    fenetre_principale.mainloop()

if __name__ == "__main__":
    main()
