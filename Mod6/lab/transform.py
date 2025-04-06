"""Data transformations"""


import pandas as pd


def get_survivors(data, who="both"):
    """Extracts information on survived vs dead for a given group of passengers

    Prameters
    ---------
    data: pd.DataFrame
        The DataFrame to extract information from.
    who: str (default = "both")
        The group of passengers to extract information about.

    Returns
    -------
    pd.DataFrame
        If who = "both", return female and male survivor/dead numbers, else
        return either female or male.
    """
    assert isinstance(data, pd.DataFrame)
    people = data.groupby("gender")["survived"].value_counts().unstack()
    people.columns = ["dead", "survived"]

    if who == "females survived":
        people = people.loc["female"]
    elif who == "males survived":
        people = people.loc["male"]

    return people
