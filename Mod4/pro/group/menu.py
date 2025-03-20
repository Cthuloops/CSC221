"""Menu Functions"""

from util import find_faculty


def get_menu_choice(amount_options):
    """Prompts user for choice, validates, returns choice.

    print_menu is 0 based indexing on the back side but presented in the more
    readable format for the end user by adding 1 to the option number as it is
    printed to the screen. (Option 0 is presented as Option 1)

    Parameters
    ----------
    amount_options: int
        The amount of options presented to the end user.

    Returns
    -------
    int
        User input - 1
    """
    user_input = 0
    while user_input not in range(1, amount_options + 1):
        try:
            user_input = int(input("Enter a number between 1 and "
                                   f"{amount_options}: "))
        except ValueError:
            # Ignoring anything other than a number in the correct range
            ...
    # Need to remove the 1 added to the options when printed for
    # menus that aren't main
    return user_input - 1


def print_menu(header, options):
    """Print formatted menu

    Parameters
    ----------
    header: str
        menu header
    options: list[str]
        menu options
    """
    # Get the amount of digits in the length of  options (e.g. 15 = 2
    # digits).
    length_digits = len(str(len(options)))
    # Add 2 to account for the '. ' in the print loop.
    length_formatting = length_digits + 2
    # Get the length of the longest option for formatting.
    max_length = max(len(op) + length_formatting for op in options)
    if max_length < len(header):
        max_length = len(header) + length_digits

    print(f"{header:-^{max_length}}")
    for i, option in enumerate(options):
        print(f"{i + 1:>{length_digits}}. {option}")


def submenu_course_code(courses):
    """Prompt the user for input, validate, and return it.

    Parameters
    ----------
    courses: list[str]
        List of valid course codes.

    Returns
    -------
    str
        Course code entered by the user.
    """
    print(f"{'Course Code':-^2}")

    choice = ""
    found = False
    keep_going = True
    while not found and keep_going:
        choice = input("Enter course code(or Q to quit): ")
        choice = choice.strip().upper()

        if choice == 'Q':
            keep_going = False
            choice = None
        elif choice in courses:
            found = True
        else:
            print(f"{choice} not found, please check spelling.")

    return choice


def fte_faculty_submenu(faculty):
    """Prompt the user for input, validate, and return it.

    Parameters
    ----------
    faculty: list[str]
        List of valid faculty names.

    Returns
    -------
    str or None
        The faculty member name, or "To be Announced",
         or None if the user quits
    """
    keep_going = True
    while keep_going:

        # Prompt  user for faculty name to search for
        print(f"{'FTE by Faculty':-^2}\n")
        choice = input("Enter the first and/or last name of a faculty "
                       "member,\nTBA for classes with no announced "
                       "faculty,\n(or enter Q to quit) \n "
                       ">>> ").strip().title()
        if choice == 'Q':
            return None
        if choice == "Tba":
            return "To be Announced"

        # call function to search for faculty
        found_name = find_faculty(choice, faculty)

        # If multiple matches are found, prompt user to choose
        if isinstance(found_name, list) and len(found_name) > 1:
            found_name.append("None of these")  # Add a "None" option

            print_menu("Did you mean", found_name)
            name_choice = get_menu_choice(len(found_name))

            # User selects "None of these"
            if name_choice == len(found_name) - 1:
                found_name = None
            else:
                found_name = found_name[name_choice]

        # If exactly one match, return it
        elif isinstance(found_name, list) and len(found_name) == 1:
            found_name = found_name[0]

        # If no matches, notify user and loop again
        if not found_name:
            print(f"{choice} could not be found, "
                  f"please check spelling\n")
            continue  # Restart loop

        return found_name  # Return found faculty name
