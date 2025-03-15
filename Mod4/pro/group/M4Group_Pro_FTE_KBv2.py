# This program creates spreadsheets of information on classes offered by FTCC
# 02/09/2025
# CSC221 M2Pro2 - FTE
# Harley Coughlin

import pandas as pd
import extract
import menu
import options
import transform


def main():
    # Control flow booleans
    error = False
    keep_going = True

    dfs = {} # Dictionary to store DataFrames
    filenames = ["deansDailyCsar.csv", "FTE_Tier.xlsx"]
    for filename in filenames:
        print(f"Trying to extract from {filename}.")
        try:
            df = extract.extract_csv(filename=filename)
        except FileNotFoundError as e:
            print(f"""Unable to find the {filename}. Please make sure it exists in
                    the current directory.""")
            print(f"Technical details: {e}")
            error = True
        except pd.errors.EmptyDataError as e:
            print(f"The input file {filename} is empty. Please check the file "
                  "contents.")
            print(f"Technical details: {e}")
            error = True

        if not df.empty:
            df = transform.sort_dataframe(df)
            print("Data extraction complete and sorted.")
            dfs[filename] = df
        else:
            print("Data failed to load.")
            error = True

    # Assign each DataFrame to a variable for easier accessibility
    csar_df = dfs.get("deansDailyCsar.csv")
    tier_df = dfs.get("FTE_Tier.xlsx")





    main_menu_header = "Main Menu"
    main_menu_options = [
        "Enter \"Sec Divisions\" code",
        "Get Course Enrollment Percentage",
        "FTE by Division",
        "FTE per Instructor",
        "FTE per course",
        "Exit"
    ]

    while not error and keep_going:
        menu.print_menu(main_menu_header, main_menu_options)
        option = menu.get_menu_choice(len(main_menu_options))
        if option == 0:
            options.option1(csar_df)
        elif option == 1:
            options.course_enrollment_percentage(csar_df)
        elif option == 2:
            options.fte_per_division(csar_df)
        elif option == 3:
            options.fte_per_faculty(csar_df, tier_df)
        elif option == 4:
            options.fte_per_course(csar_df)
        elif option == 5:
            print("Thanks for playing.")
            keep_going = False
        else:
            print("You shouldn't be here.")
            keep_going = False


if __name__ == "__main__":
    main()
