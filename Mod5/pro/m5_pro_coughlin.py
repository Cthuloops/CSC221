"""This program interacts with a sqlite database"""
# Menu driven program to access a sqlite database
# 03/25/2025
# CSC221 M5Pro - Database
# Harley Coughlin


def main():
    """Entry point to the program."""
    choice = 0
    while choice != 6:
        print_menu()
        choice = get_menu_choice()

        if choice == 1:
            ...
        elif choice == 2:
            ...
        elif choice == 3:
            ...
        elif choice == 4:
            ...
        elif choice == 5:
            ...
        elif choice == 6:
            print("Thanks for using the program.")


def print_menu():
    """Prints the main menu."""
    options = (
        "1) Display OWNER content and create DataFrame",
        "2) Display PETS content and create DataFrame",
        "3) Retrieve Owner and Pet data for specific Owner",
        "4) Calculate Total Charge by Owner",
        "5) Retrieve pet information by PetBreed",
        "6) Exit")
    print(f"{'Main Menu':-^{max(len(opt) for opt in options)}}")
    for opt in options:
        print(opt)


def get_menu_choice():
    """Gets a menu option"""
    try:
        choice = int(input("Enter menu option: "))
        if choice < 1 or choice > 6:
            raise ValueError
    except ValueError:
        print("Please enter a valid number between 1 and 6.\n")
    else:
        return choice


if __name__ == "__main__":
    main()
