# Project_python_master_IRS
projet_python_semaine_IRS




---- premier projet : final_banque.py

Ce programme lit un fichier contenant des noms prénom et pour chaque personne, un compte bancaire et décide arbitrairement de crée une carte bancaire. Possibilité par la suite pour l'utilisateur au travers d'une interface graphique d'afficher l'intégralité des comptes avec leur numero, propriétaire, solde etc ou bien de visualisé les cartes avec le numero de carte, propriétaire, date d'expiration et CVV.



------ deuxième projet : final_client_banque.py et final_serveur_banque.py

Ces programmes fonctionnent en architecture Client/Serveur. L'application Serveur host des données de comptes stocké dans un fichier. L'application cliente, demande à l'utilisateur sur une interface graphique de taper un numéro de compte, un nom et un mot de passe. Le programme envoie le numero de compte, le nom et le hash du mot de passe au serveur. Si les informations sont valides, le serveur envoie une erreur si les informations ne sont pas valides ou bien envoie les données si elles correspondent. Coté programme client, après reception des données une nouvelle fenetre s'ouvre avec les informations correspondantes.