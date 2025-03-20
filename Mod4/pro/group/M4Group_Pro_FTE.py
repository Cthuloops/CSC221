""" This program creates spreadsheets of information on classes
offered by
FTCC
03/21/2025
CSC221 M4Group_Pro_FTE
Harley Coughlin & Karen Brown
"""

import extract
import menu
import options


def main():
    """ Main entry point of the program. Extracts data from required
    files and displays menu for user interaction. Calls corresponding
    functions based on user selection.
    :return: None """

    filenames = ["deanDailyCsar.csv", "FTE_Tier.xlsx"]
    dfs, error = extract.extract_data(filenames)
    if error:
        return  # Exit early if there was an error during extraction

    # Assign each DataFrame to a variable for easier accessibility
    csar_df = dfs.get("deanDailyCsar.csv")
    tier_df = dfs.get("FTE_Tier.xlsx")
    keep_going = True
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
            options.fte_per_course(csar_df, tier_df)
        elif option == 5:
            print("Thanks for playing.")
            keep_going = False
        else:
            print("You shouldn't be here.")
            keep_going = False


if __name__ == "__main__":
    main()
