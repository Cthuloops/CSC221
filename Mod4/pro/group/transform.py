"""Data transformations"""

import pandas as pd
import extract


def sort_dataframe(data, sort_by=["Sec Divisions", "Sec Name",
                                  "Sec Faculty Info"]):
    """Sorts a DataFrame by columns, in ascending order.

    Parameters
    ----------
    data: pd.DataFrame
        DataFrame to sort.
    sort_by: list[str]
        (default = ["Sec Divisions", "Sec Name", "Sec Faculty Info"])
        Column name(s) to sort by.

    Returns
    -------
    pd.DataFrame
        Sorted DataFrame
    """
    return data.sort_values(by=sort_by)


def get_column_uniques(data, name):
    """Extracts unique values from a column within a DataFrame.

    Parameters
    ----------
    data: pd.DataFrame
        DataFrame to read from.
    name: str
        Name of the column to extract unique values.

    Returns
    -------
    list[str]
        List of unique values.
    """

    # Extract unique, non-null values
    unique_values = data[name].dropna().unique()
    # Explicit conversion to list[str] to prevent type errors
    return [str(x) for x in unique_values]


def get_division_frame(data, name):
    """Extracts all rows associated to a specific division code

    Parameters
    ----------
    data: pd.DataFrame
        DataFrame to extract rows from.
    name: str
        The division code to target.
    """
    # Get empty cells
    if name is None or name == "No code":
        frame = data[data["Sec Divisions"].isna() |
                     (data["Sec Divisions"] == "")]
    else:
        frame = data[data["Sec Divisions"] == name]
    frame = pd.DataFrame(frame)
    return frame


def get_course_frame(data, name, filter=True):
    """Extracts rows associated with a course code

    Parameters
    ----------
    data: pd.DataFrame
        DataFrame to extract rows from.
    name: str
        Course code to filter for.
    filter: bool (default = True)
        If true, face-to-face courses will be filtered

    Returns
    -------
    pd.DataFrame
        All rows associated to the Course Code without face-to-face classes
        with INET meeting times if filtered, else all rows.
    """
    # Get the course rows
    frame = data[data["Sec Name"].str.contains(name)]
    if filter:
        # Get all the face-to-face sections.
        zero_sections = frame["Sec Name"].str.contains(r"-\d0\d\d")
        zero_frame = frame[zero_sections]
        # Group them together and take only the first record for each group.
        zero_frame = zero_frame.groupby("Sec Name", as_index=False).first()
        # Get all the other sections.
        non_zero_frame = frame[~zero_sections]
        frame = pd.concat([zero_frame, non_zero_frame])

    return frame


def get_faculty_frame(data, name):
    """Extracts rows associated with a faculty member or ones not assigned yet.

    Parameters
    ----------
    data: pd.DataFrame
        DataFrame to extract rows from
    name: str
        Faculty name to filter for. 'To be Announced' if looking for unassigned
        courses.

    Returns
    -------
    pd.DataFrame
        All rows associated to the given faculty member of no faculty member.
    """
    # Get faculty rows
    frame = data[data["Sec Faculty Info"] == name]

    return frame

def get_tier_frame():
    """
    extracts the data from FTE_Tier.xlsx into a DataFrame
    :return: pd.DataFrame
        tier_frame: DataFrame containing the Tier and proposed
        funding level for each course ID
    """
    tier_frame = extract.extract_csv('FTE_Tier.xlsx')
    return tier_frame


def generate_FTE(data, tier, support = 1926):
    """
    calculates generated FTE for a set of data and returns it as a
    Pandas Series

    Parameters
    ----------
    data: pd.DataFrame
        DataFrame to calculate generated FTE for

    tier: pd.DataFrame
        DataFrame that holds the proposed funding lever for different tiers

    Returns
    -------
    pd.DataFrame
        generate_FTE: a new DataFrame that has the generated FTE
    """

    # create a dictionary to hold the course ID and their proposed
    # funding
    courseid_to_funding = {
        row["Prefix/Course ID"]: row["New Sector"]
        for _, row in tier.iterrows()
    }

    # Apply computed generated FTE to for all rows in original DataFrame
    data["Generated FTE"] = data.apply(
        lambda row: compute_fte(row, courseid_to_funding, support),
        axis=1)

    return data


def compute_fte(row, courseid_to_funding, support=1926):
    """
    Computes the generate FTE for a single row in a dataframe
    :param row: pd.Series
        a row from the data DataFrame
    :param courseid_to_funding: dict
        a dictionary for the course prefixes and their funding levels
    :param support: int, optional
        a fixed amount for institutional and academic support(default
        is 1926)
    :return: float
        the computed generated FTE value for the row
    """
    course_prefix = row["Course Code"][:3]  # Extract prefix (first 3 chars)
    prop_fund = courseid_to_funding.get(course_prefix, 0)  # Get
    # funding level
    return (prop_fund + support) * row["Total FTE"]  # Apply formula

def total_FTEs(data):
    """
    calculates to total FTE for each course and for a division
    :param data: ps.DataFrame
        A DataFrame that has individual secs generated FTE 
    :return: 
    course_FTE: dictionary
        courses and their total generated FTE
    final_FTE: Interger
        total generated FTE for entire dataframe
    
    """


    # Get the totals for different courses
    course_FTE_total = data.groupby("Course Code")["FTE"].sum().to_dict()

    # Get total for the entire division

    final_FTE_total = data["Generated FTE"].sum()
    return course_FTE_total, final_FTE_total

















