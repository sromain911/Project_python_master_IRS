#PSL Modules

#External modules
#import customtkinter
import tk
#Custom modules
import app

# Main function (entry-point)
def main():
    #application nexw instance
    new_app_instance =app.Application()

    new_app_instance.launch_app()
    new_app_instance.display_menu()

#Main Guard
if __name__ == "__main__":
    main()