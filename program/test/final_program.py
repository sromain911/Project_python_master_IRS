import tk
import os
import sys
import random
import string

class CompteBancaire:
    def __init__(self, user_name, user_family_name):
        self.identifiant = self.generer_compte()
        print(self.identifiant)
        self.user_name = user_name
        self_user_family_name = user_family_name
        self.generer_carte()
    
    def generer_compte(self):
         return ''.join(random.choices(string.digits, k=10))

    def generer_carte(self):
        self.carte_identifiant = ''.join(random.choices(string.digits, k=16))
        print(self.carte_identifiant)
        jour = random.randint(1, 28)
        mois = random.randint(1, 12)
        self.expiration_date = f"{jour:02}/{mois:02}"
        print(self.expiration_date)
        self.CVV = f"{(random.randint(101,999)):03}"
        print(self.CVV)



# Main Function
def main():
    john = CompteBancaire("john", "Doe")


# Main Guard
if __name__ == "__main__":
    main()