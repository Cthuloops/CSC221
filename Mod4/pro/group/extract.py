"""Data extraction module"""

import os.path
import pandas as pd
import transform


def extract_csv(filename):
    """Load CSV file into a Pandas DataFrame

    Parameters
    ----------
    filename: str
        CSV filename

    Returns
    -------
    pd.DataFrame
        DataFrame containing the CSV information
    """
    assert filename is not None, "Filename should not be None."
    assert isinstance(filename, str), \
        f"Expected filename to be a string instead got {filename}."
    assert filename, "File should not be empty"
    assert filename.endswith(".csv"), \
        f"Expected csv file got {filename}."
    file_path = ""
    try:
        file_path = os.path.join(os.getcwd(), filename)
        data = pd.read_csv(file_path)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Error: Could not find filename "
                                f"{file_path}") from exc
    except pd.errors.EmptyDataError as exc:
        raise pd.errors.EmptyDataError(f"Error: File {file_path} is "
                                       f"empty") from exc

    return data


def extract_excel(filename):
    """Load Excel file into a Pandas DataFrame

    Parameters
    ----------
    filename: str
        Excel filename

    Returns
    -------
    pd.DataFrame
        DataFrame containing the Excel information
    """
    assert filename is not None, "Filename should not be None."
    assert filename is not None, "Filename should not be None."
    assert isinstance(filename, str), \
        f"Expected filename to be a string instead got {filename}."
    assert filename, "File should not be empty"
    assert filename.endswith(".xlsx"), \
        f"Expected excel file got {filename}."
    file_path = ""
    try:
        file_path = os.path.join(os.getcwd(), filename)
        data = pd.read_excel(file_path)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Error: Could not find filename "
                                f"{file_path}") from exc
    except pd.errors.EmptyDataError as exc:
        raise pd.errors.EmptyDataError(f"Error: File {file_path} is "
                                       f"empty") from exc

    return data


def extract_data(filenames):

    """
    Extracts data from files and returns a dictionary of DataFrames.
    Parameters
    ----------
    filename: str
        Excel filename

    Returns
    -------
    dict
        dictionary of DataFrames

    bool
        true if error occurs """

    dfs = {}
    error = False
    for filename in filenames:
        df = None
        print(f"Trying to extract from {filename}.")
        try:
            if filename.endswith(".csv"):
                df = extract_csv(filename=filename)
            elif filename.endswith(".xlsx"):
                df = extract_excel(filename=filename)
        except FileNotFoundError as e:
            print(f"Unable to find {filename}. "
                  f"Please ensure it exists in the current directory.")
            print(f"Technical details: {e}")
            error = True
        except pd.errors.EmptyDataError as e:
            print(f"The input file {filename} "
                  f"is empty. Please check the file contents.")
            print(f"Technical details: {e}")
            error = True

        if df is not None and not df.empty:
            if filename.startswith("deanDailyCsar"):
                df = transform.sort_dataframe(df)
                print("Data extraction complete and sorted.")
            dfs[filename] = df
        else:
            print("Data failed to load.")
            error = True

    return dfs, error
