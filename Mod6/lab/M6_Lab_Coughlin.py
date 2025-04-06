# This a menu driven program using DataFrames, exception handling, functions,
# file processing, and plotting.
# 04/03/2025
# CSC221 M6Lab - Visualization
# Harley Coughlin


import menu
import display
import transform
import pandas as pd


def main():
    """Entry point to the program."""
    error = False
    filename = "Titanic.xlsx"
    df = pd.DataFrame()

    try:
        df = pd.read_excel(filename)
    except FileNotFoundError:
        print(f"File {filename} not found in current directory")
    except Exception as e:
        print(f"Unexpected error occured: {e}")

    if df.empty:
        error = True
        print("DataFrame is empty")

    choice = 0
    while not error and choice != 8:
        menu.print_menu()
        choice = menu.get_int_range(1, 8)

        if choice == 1:
            display.first_fifteen(df)

        elif choice == 2:
            display.records_amount(df)

        elif choice == 3:
            survivors = transform.get_survivors(df)
            display.survivor_amounts(survivors)

        elif choice == 4:
            header = "Option 4 submenu"
            options = ("Females Survived", "Males Survived", "Both")
            menu.print_submenu(header, options)
            submenu_choice = menu.get_string(options)
            survivors = transform.get_survivors(df, submenu_choice)
            display.survivor_amounts(survivors, submenu_choice)

        elif choice == 5:
            survivors = transform.get_survivors_by_class(df)
            display.survivor_amounts(survivors, "class")

        elif choice == 6:
            survivors = transform.get_survivors_by_travel(df)
            display.survivor_amounts_by_travel(survivors)

        elif choice == 7:
            header = "Option 7 submenu"
            options = ("All", "Infant", "Child", "Teenager", "Young adult",
                       "Adult", "Unknown")
            menu.print_submenu(header, options)
            submenu_choice = menu.get_string(options)
            survivors = transform.get_survivors_by_age(df)
            display.survivor_amounts_by_age(survivors, submenu_choice)

        elif choice == 8:
            print("Nice")


if __name__ == "__main__":
    main()
