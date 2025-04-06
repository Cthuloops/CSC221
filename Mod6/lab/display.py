"""Display the information."""


import pandas as pd


def first_fifteen(data, amount=15):
    """Prints an amount of rows from the top of a DataFrame.

    Parameters
    ----------
    data: DataFrame
        The DataFrame to display information from.
    amount: int (default 15)
        The amount of rows from the top to display.
    """
    print()
    print(data.head(amount))
    print()


def records_amount(data):
    """Prints the amount of records in the DataFrame, not including the header

    Parameters
    ----------
    data: DataFrame
        The DataFrame to display the amount of records
    """
    print(f"\nAmount of passengers: {len(data)}\n")


def survivor_amounts(people, who="all"):
    """Prints the amount of survivors vs dead for a given group of people.

    Parameters
    ----------
    people: pd.DataFrame | pd.Series
        The survivor amounts to display.
    who: str (default: "all")
        The group of passengers to print information about.
        Options: "all", "both", "females survived", "males survived"
    """
    print()
    if who == "all":
        print(f"Dead: {people.dead.sum():>7}")
        print(f"Survived: {people.survived.sum()}")
    elif who == "both":
        print(people)
    elif who == "females survived":
        print(people)
    elif who == "males survived":
        print(people)
    elif who == "class":
        print(people)
    print()
    people.plot()


def survivor_amounts_by_travel(people):
    """Prints information related to the statistics of people traveling alone
    vs. in a group.

    Parameters
    ----------
    people: pd.DataFrame | pd.Series
        The survivor amounts to display.
    """
    print()
    print("Passenger amounts:")
    print(people.sum(axis=1).to_string(dtype=False))
    print(f"{'':~^21}")

    print("Survivorship by group:")
    print(people)
    print(f"{'':~^21}")

    print("Percentage of survivors by group:")
    passenger_totals = people.sum(axis=1)
    passenger_percentages = (people["survived"] / passenger_totals  * 100).round(2)
    print(passenger_percentages.to_string(dtype=False))
    print()


def survivor_amounts_by_age(people, age_group):
    """Prints information about the age groups of passengers

    Parameters
    ----------
    people: pd.DataFrame | pd.Series
        Passengers to display information about.
    """
    print()
    if age_group == "all":
        print(people)
    else:
        print(f"{age_group.title()}:")
        print(people.loc[age_group].to_string(dtype=False))
    print()
