""" Application Main Class

"""

import sys
import os

class Application:
    def __init__(self):
        pass

    def launch_app(self):
        os.system("cls")
        print("Loading...")

    def display_menu(self):
        print("Main Menu\n1 Start a new game\n2 Load Game\n3 Quit")

        user_choice = input()

        # Condition or Switch case (match case)
        if(user_choice == "1"):
            self.app_new_aventure()
        elif(user_choice == "2"):
            pass
        elif(user_choice == "3"):
            self.quit_app()
        else:
            print("Choice doesn't exist")

    def app_new_aventure (self):
        pass

    def quit_app(self):
        sys.exit()