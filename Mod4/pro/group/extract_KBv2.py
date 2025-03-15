"""Data extraction module"""

import os.path
import pandas as pd


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
    assert filename is not None, "File should not be None."
    assert isinstance(filename, str), "Expected filename to be a string" \
                                      f"instead got {filename}."
    assert filename, "File should not be empty"
    assert filename.endswith(".csv"), f"Expected csv file got {filename}."
    data = pd.DataFrame()
    file_path = ""
    try:
        file_path = os.path.join(os.getcwd(), filename)
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Could not find filename {file_path}")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"Error: File {file_path} is empty")

    return data
