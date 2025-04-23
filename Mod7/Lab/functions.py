"""Database extraction functions"""


import pandas as pd
import sqlite3


def _get_table_information(_db_name, _table_name):
    """Opens a connection to the named database and retrieves information
    from the named table.

    Parameters
    ----------
    db_name: str
        Name of the db to access.
    table_name: str
        Name of the table to extract the data from.

    Returns
    -------
    list[dict]
        List of dicts of rows in the table
    """
    assert isinstance(_db_name, str)
    assert isinstance(_table_name, str)
    assert _db_name != "", "_db_name should not be empty"
    assert _table_name != "", "_table_name should not be empty"

    rows = []
    conn = None
    try:
        conn = sqlite3.connect(_db_name)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(f"SELECT * FROM {_table_name};").fetchall()
    except sqlite3.Error as e:
        raise e
    finally:
        if conn is not None:
            conn.close()
    assert isinstance(rows, list)
    return [dict(row) for row in rows]


def get_table_dataframe(table_name):
    """Returns a dataframe made from table information

    Parameters
    ----------
    table_name: str
        Either OWNER or PETS

    Returns
    -------
    pd.DataFrame
    """
    table_names = ["OWNER", "PETS"]
    assert isinstance(table_name, str)
    assert table_name != "", "Table name should not be empty"

    table_name = table_name.upper()
    assert table_name in table_names, "Table name needs to be OWNER or PETS"

    table = _get_table_information("vet_serv.db", table_name)
    return pd.DataFrame(table)


def _get_owner_pet_dataframe(owner_id):
    """Internal function to retrieve all pet and owner information associated
    with an owner id.

    Parameters
    ----------
    owner_id: int
        Owner ID

    Returns
    -------
    pd.DataFrame
        DataFrame will be empty if there's no entries found for the owner in
        the pet table.
    """
    assert isinstance(owner_id, int)

    rows = None
    conn = None
    try:
        conn = sqlite3.connect("vet_serv.db")
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            f"""
            SELECT o.*, p.*
            FROM OWNER o
            INNER JOIN PETS p ON o.OwnerId = p.OwnerId
            WHERE o.OwnerId = {owner_id};
            """).fetchall()
    except sqlite3.Error as e:
        raise e
    finally:
        if conn is not None:
            conn.close()
    if rows is not None:
        rows = [dict(row) for row in rows]
    return pd.DataFrame(rows)


def _filter_dataframe(data, columns):
    """Filters a dataframe to the specified columns.

    Parameters
    ----------
    data: pd.DataFrame
        The data frame to filter.
    columns: list[str]
        The column names to filter for.

    Returns
    -------
    pd.DataFrame
        If the DataFrame isn't empty, returns a filtered DataFrame,
        else, just returns the empty DataFrame.
    """
    assert isinstance(data, pd.DataFrame)
    assert isinstance(columns, list)
    for col in columns:
        assert isinstance(col, str)
    if data.empty:
        return data
    return data[columns]


def get_owner_pet_dataframe(owner_id, columns=[]):
    """Gets dataframe by owner id and filters for columns

    Parameters
    ----------
    owner_id: int
        The owner id to retrieve information for.
    columns: list[str] | []
        If empty, do no filtering.
        Otherwise, filter based on the fields specified in the list.

    Returns
    -------
    pd.DataFrame
        Filtered dataframe
    """
    assert isinstance(owner_id, int)
    assert isinstance(columns, list)
    df = _get_owner_pet_dataframe(owner_id)
    if len(columns) != 0:
        df = _filter_dataframe(df, columns)
    assert isinstance(df, pd.DataFrame)
    return df


if __name__ == "__main__":
    columns = ["OwnerId", "OwnerFirstName", "OwnerLastName", "OwnerEmail",
               "PetId", "PetName", "PetBreed", "PetDOB"]
    print(get_owner_pet_dataframe(1011, columns))
