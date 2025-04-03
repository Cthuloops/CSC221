"""Menu functions"""


def print_menu():
    """Print the main menu."""
    print("M6Lab: Titanic")
    print("1. Display Dataset")
    print("2. Get the number of records(passengers) listed in the dataset.")
    print("3. Get the number of Survived vs Dead.")
    print("4. Get the number of Females and/or Males.")
    print("5. Get the number of passengers per class.")
    print("6. Get the number of passengers traveling alone(Survived vs Dead)")
    print("7. Get the number of Survived vs Dead by age group")
    print("8. Exit")


def get_int_range(min, max):
    """Prompt the user for an int between min and max, inclusive.

    Parameters
    ----------
    min: int
        The minimum number allowed.
    max: int
        The maximum number allowed.

    Returns
    -------
    int
        An int between min and max, inclusive.
    """
    assert isinstance(min, int), "min must be an integer."
    assert isinstance(max, int), "max must be an intger."
    choice = min - 1
    while choice < min or choice > max:
        try:
            choice = int(input(f"Enter a number between {min} and {max}: "))
        except ValueError:
            print("Invalid: please enter a valid integer.")
        else:
            return choice


def print_submenu(header, options):
    """Print formatted submenu.

    Parameters
    ----------
    header: str
        Title for the menu.
    options: tuple[str, ...]
        Tuple of strings that contain the submenu options.
    """
    print()
    gutter = len(options) + len(": ")
    max_length = max([len(option) for option in options])
    print(f"{header:~^{max_length + gutter}}")
    for i in range(len(options)):
        print(f"{i}: options[i]")


def get_string(options):
    """Prompts user to enter a string, validates against options.

    Parameters
    ----------
    options: tuple[str, ...]
        Tulp of strings with valid submenu options.

    Returns
    -------
    str
        Option entered by the user.
    """
    choice = ""
    while choice not in [c.strip().casefold() for c in options]:
        choice = input("Please type your choice: ").strip().casefold()

    return choice
