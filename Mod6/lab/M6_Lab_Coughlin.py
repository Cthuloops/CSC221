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
            ...

        elif choice == 8:
            print("Nice")


if __name__ == "__main__":
    main()
