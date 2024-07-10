import socket
import tkinter as tk
from tkinter import ttk, messagebox

# Paramètres du serveur
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
RETRY_LIMIT = 5

def send_request(account_id, account_name):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        request = f"{account_id};{account_name}"
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
    global entry_account_id, entry_account_name  # Déclaration globale des variables

    account_id = entry_account_id.get()
    account_name = entry_account_name.get()

    if not account_id or not account_name:
        messagebox.showwarning("Erreur", "Veuillez entrer le numéro de compte et le nom du propriétaire.")
        return

    response = send_request(account_id, account_name)

    if response:
        show_account_info(response)
    else:
        messagebox.showerror("Erreur", "Aucune réponse du serveur après plusieurs tentatives.")

def show_account_info(info):
    account_info = info.split(";")
    
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
    global entry_account_id, entry_account_name  # Déclaration globale des variables

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

    # Bouton pour valider la demande
    bouton_valider = ttk.Button(cadre_entrees, text="Valider", command=handle_submit)
    bouton_valider.grid(row=2, column=0, columnspan=2, pady=10)

    # Redimensionnement des colonnes du cadre d'entrées
    cadre_entrees.columnconfigure(1, weight=1)

    fenetre_principale.mainloop()

if __name__ == "__main__":
    main()
