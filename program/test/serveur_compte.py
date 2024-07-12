import socket
import csv

class CompteBancaire:
    def __init__(self, identifiant, user_family_name, user_name, solde, a_carte, carte_identifiant, expiration_date, CVV):
        self.identifiant = identifiant
        self.user_family_name = user_family_name
        self.user_name = user_name
        self.solde = solde
        self.a_carte = a_carte
        self.carte_identifiant = carte_identifiant
        self.expiration_date = expiration_date
        self.CVV = CVV

    def to_dict(self):
        return {
            "Identifiant": self.identifiant,
            "Nom": self.user_family_name,
            "Prénom": self.user_name,
            "Solde": self.solde,
            "Carte Présente": self.a_carte,
            "Carte Identifiant": self.carte_identifiant,
            "Date d'Expiration": self.expiration_date,
            "CVV": self.CVV
        }

def load_accounts(filename):
    accounts = {}
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                account = CompteBancaire(
                    row["Identifiant"],
                    row["Nom"],
                    row["Prénom"],
                    row["Solde"],
                    row["Carte Présente"],
                    row["Carte Identifiant"],
                    row["Date d'Expiration"],
                    row["CVV"]
                )
                accounts[row["Identifiant"]] = account
    except Exception as e:
        print(f"Erreur lors du chargement des comptes: {str(e)}")
    return accounts

def start_server(host, port, accounts):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"Serveur en écoute sur {host}:{port}")

    while True:
        data, addr = server_socket.recvfrom(1024)
        request = data.decode().split(';')
        if len(request) == 2:
            account_id, name = request
            if account_id in accounts and accounts[account_id].user_family_name == name:
                account = accounts[account_id]
                response = f"{account.identifiant};{account.user_family_name};{account.user_name};{account.solde};{account.a_carte};{account.carte_identifiant};{account.expiration_date};{account.CVV}"
            else:
                response = "Compte non trouvé ou informations incorrectes"
        else:
            response = "Requête mal formatée"

        server_socket.sendto(response.encode(), addr)

if __name__ == "__main__":
    accounts = load_accounts(r'program\comptes_crees.csv')
    start_server('localhost', 12345, accounts)
