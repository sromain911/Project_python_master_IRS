import random
import string
import tkinter as tk
from tkinter import messagebox

class CompteBancaire:
    def __init__(self, solde_initial, titulaire):
        self.numero_compte = self.generer_numero_compte()
        self.solde = solde_initial
        self.titulaire = titulaire
        self.carte_associee = None

    def generer_numero_compte(self):
        return ''.join(random.choices(string.digits, k=10))

    def lier_carte(self, carte):
        self.carte_associee = carte

class CarteBancaire:
    def __init__(self, titulaire, date_expiration, cvv):
        self.numero_carte = self.generer_numero_carte()
        self.titulaire = titulaire
        self.date_expiration = date_expiration
        self.cvv = cvv
        self.compte_associe = None

    def generer_numero_carte(self):
        return ''.join(random.choices(string.digits, k=16))

    def lier_compte(self, compte):
        self.compte_associe = compte

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulateur de paiement par carte bleue")
        self.geometry("400x400")
        self.minsize(200, 200)

        # Initialisation des comptes et cartes
        self.compte = CompteBancaire(solde_initial=1000.0, titulaire="John Doe")
        self.carte = CarteBancaire("John Doe", "12/25", "123")
        self.compte.lier_carte(self.carte)
        self.carte.lier_compte(self.compte)

        self.creer_menu()
        self.creer_widgets()

    def creer_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.menu_operations = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_operations.add_command(label="Consulter les comptes", command=self.consulter_comptes)
        self.menu_operations.add_command(label="Consulter les cartes", command=self.consulter_cartes)
        self.menu_operations.add_command(label="Effectuer un paiement", command=self.effectuer_paiement)
        self.menu_bar.add_cascade(label="Menu", menu=self.menu_operations)

    def creer_widgets(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def consulter_comptes(self):
        self.clear_frame()

        compte_info = f"Numéro de compte: {self.compte.numero_compte}\n" \
                      f"Titulaire: {self.compte.titulaire}\n" \
                      f"Solde: {self.compte.solde:.2f} €"
        self.create_text_widget(compte_info)

    def consulter_cartes(self):
        self.clear_frame()

        carte_info = f"Numéro de carte: {self.carte.numero_carte}\n" \
                     f"Titulaire: {self.carte.titulaire}\n" \
                     f"Date d'expiration: {self.carte.date_expiration}\n" \
                     f"CVV: {self.carte.cvv}"
        self.create_text_widget(carte_info)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_text_widget(self, content):
        text_widget = tk.Text(self.main_frame, wrap=tk.WORD, height=10)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        text_widget.bind("<Button-3>", lambda event: self.show_context_menu(event, text_widget))

    def show_context_menu(self, event, widget):
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Copier", command=lambda: self.copy_text(widget))
        context_menu.post(event.x_root, event.y_root)

    def copy_text(self, widget):
        self.clipboard_clear()
        self.clipboard_append(widget.get("1.0", tk.END).strip())

    def effectuer_paiement(self):
        self.clear_frame()

        # Champ pour saisir le montant
        tk.Label(self.main_frame, text="Montant à payer:").grid(row=0, column=0)
        self.montant_entry = tk.Entry(self.main_frame)
        self.montant_entry.grid(row=0, column=1)

        # Bouton pour valider le montant
        self.valider_button = tk.Button(self.main_frame, text="Valider", command=self.afficher_champs_carte)
        self.valider_button.grid(row=0, column=2)

    def afficher_champs_carte(self):
        self.montant = float(self.montant_entry.get())

        # Supprimer les champs de montant et le bouton valider
        self.montant_entry.grid_forget()
        self.valider_button.grid_forget()

        # Champs pour les informations de la carte
        tk.Label(self.main_frame, text="Numéro de carte:").grid(row=1, column=0)
        self.numero_carte_entry = tk.Entry(self.main_frame)
        self.numero_carte_entry.grid(row=1, column=1)

        tk.Label(self.main_frame, text="Titulaire:").grid(row=2, column=0)
        self.titulaire_entry = tk.Entry(self.main_frame)
        self.titulaire_entry.grid(row=2, column=1)

        tk.Label(self.main_frame, text="Date d'expiration (MM/YY):").grid(row=3, column=0)
        self.date_expiration_entry = tk.Entry(self.main_frame)
        self.date_expiration_entry.grid(row=3, column=1)

        tk.Label(self.main_frame, text="CVV:").grid(row=4, column=0)
        self.cvv_entry = tk.Entry(self.main_frame)
        self.cvv_entry.grid(row=4, column=1)

        # Bouton pour payer
        self.payer_button = tk.Button(self.main_frame, text="Payer", command=self.valider_paiement)
        self.payer_button.grid(row=5, column=1)

    def valider_paiement(self):
        numero_carte = self.numero_carte_entry.get()
        titulaire = self.titulaire_entry.get()
        date_expiration = self.date_expiration_entry.get()
        cvv = self.cvv_entry.get()

        # Vérification des informations de la carte
        if (numero_carte == self.carte.numero_carte and
                titulaire == self.carte.titulaire and
                date_expiration == self.carte.date_expiration and
                cvv == self.carte.cvv):

            # Vérification du solde
            if self.compte.solde >= self.montant:
                self.compte.solde -= self.montant
                messagebox.showinfo("Succès", "Paiement réussi!")
            else:
                messagebox.showerror("Erreur", "Solde insuffisant!")
        else:
            messagebox.showerror("Erreur", "Informations de la carte incorrectes!")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
