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


def generate_fte(data, tier, support = 1926):
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

    try:
        # Ensure valid dataframes
        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Parameter 'data' must be a pandas DataFrame.")
        if not isinstance(tier, pd.DataFrame):
            raise TypeError(
                "Parameter 'tier' must be a pandas DataFrame.")

        # Check if required columns exist in 'tier'
        required_tier_columns = ["Prefix/Course ID", "New Sector"]
        for col in required_tier_columns:
            if col not in tier.columns:
                raise KeyError(
                    f"Missing required column '{col}' in tier "
                    f"DataFrame.")

        # Check if required columns exist in 'data'
        required_data_columns = ["Sec Name", "Total FTE"]
        for col in required_data_columns:
            if col not in data.columns:
                raise KeyError(
                    f"Missing required column '{col}' in data "
                    f"DataFrame.")


        # create a dictionary to hold the course ID and their proposed
        # funding

        data["_Course Prefix"] = data["Sec Name"].str[:3]
        data.loc[:, "_Course Prefix"] = data["_Course Prefix"].fillna("UNKNOWN")

        courseid_to_funding = {
            row["Prefix/Course ID"]: row["New Sector"]
            for _, row in tier.iterrows()
        }

        # Apply computed generated FTE to for all rows in original DataFrame
        data["Generated FTE"] = data.apply(
            lambda row: compute_fte(row, courseid_to_funding, support),
            axis=1)
        data.drop(columns=["_Course Prefix"], inplace=True, errors="ignore")

        return data

    except TypeError as e:
        print(f"TypeError in generate_fte: {e}")
    except KeyError as e:
        print(f"KeyError in generate_fte: {e}")
    except Exception as e:
        print(f"Unexpected error in generate_fte: {e}")

    return data.copy()


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

    try:
        # Ensure required columns are in DataFrame
        if "Sec Name" not in row:
            raise KeyError("Missing required column: 'Sec Name'")
        if "Total FTE" not in row:
            raise KeyError("Missing required column: 'Total FTE'")

        # Ensure 'Course Code' is a string and has at least 3 characters
        course_code = row["Sec Name"]
        if not isinstance(course_code, str) or len(course_code) < 3:
            raise ValueError(f"Invalid course code: {course_code}")

        # Extract prefix (first 3 chars)
        course_prefix = row["Sec Name"][:3]

        # Ensure 'Total FTE' is a number
        total_fte = row["Total FTE"]
        if not isinstance(total_fte, (int, float)) or pd.isna(total_fte):
            raise ValueError(f"Invalid 'Total FTE' value: {total_fte}")

        # Get funding level and calculate generated FTE
        prop_fund = courseid_to_funding.get(course_prefix, 0)
        return (prop_fund + support) * total_fte

    except KeyError as e:
        print(f" KeyError in compute_fte: {e}")
    except ValueError as e:
        print(f" ValueError in compute_fte: {e}")
    except TypeError as e:
        print(f" TypeError in compute_fte: {e}")
    except Exception as e:
        print(f" Unexpected error in compute_fte: {e}")

    return 0  # Return 0 if an error occurs so program doesn't crash

def total_ftes(data):
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

    try:
        # Ensure required columns exist
        if "Sec Name" not in data.columns:
            raise KeyError("Missing required column: 'Sec Name'")
        if "Total FTE" not in data.columns:
            raise KeyError("Missing required column: 'Total FTE'")
        if "Generated FTE" not in data.columns:
            raise KeyError("Missing required column: 'Generated FTE'")

        # Ensure FTE column contains valid numeric values
        if not pd.api.types.is_numeric_dtype(data["Total FTE"]):
            raise ValueError("Column 'FTE' must contain only "
                             "numeric values.")

        # Get the totals for different courses
        data["_Course Code"] = data["Sec Name"].str.extract(
            r"([A-Z]{3}-\d{3})")
        course_fte_total = data.groupby("_Course Code")[("Generated "
                                                         "FTE")].sum().to_dict()
        data.drop(columns=["_Course Code"], inplace=True,
                  errors="ignore")

        # Get total for the entire division
        final_FTE_total = data["Generated FTE"].sum()

        return course_fte_total, final_FTE_total

    except KeyError as e:
        print(f"️ KeyError in total_FTEs: {e}")
    except ValueError as e:
        print(f"️ ValueError in total_FTEs: {e}")
    except TypeError as e:
        print(f"️ TypeError in total_FTEs: {e}")
    except Exception as e:
        print(f"️ Unexpected error in total_FTEs: {e}")

    return {}, 0

















