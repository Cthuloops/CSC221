"""This program interacts with a sqlite database"""
# Menu driven program to access a sqlite database
# 03/25/2025
# CSC221 M5Pro - Database
# Harley Coughlin


from functions import (
    get_table_dataframe,
    get_owner_pet_dataframe
)


def main():
    """Entry point to the program."""
    choice = 0
    while choice != 6:
        print_menu()
        choice = get_int_range(1, 6)
        assert isinstance(choice, int), "Should only ever be an int"

        if choice == 1:
            owner_df = get_table_dataframe("OWNER")
            print(owner_df)
            owner_df.to_csv(path_or_buf="owner.csv", index=False)
            print("Printed onwer.csv")

        elif choice == 2:
            pets_df = get_table_dataframe("PETS")
            print(pets_df)
            pets_df.to_csv(path_or_buf="pets.csv", index=False)
            print("Printed pets.csv")

        elif choice == 3:
            columns = ["OwnerId", "OwnerFirstName", "OwnerLastName",
                       "OwnerEmail", "PetId", "PetName", "PetBreed", "PetDOB"]
            # Getting the owner table to select id values.
            owner_df = get_table_dataframe("OWNER")
            owner_id = get_owner_id(owner_df)
            # Get the dataframe if the owner id maps to pets in the pets table.
            assert isinstance(owner_id, int)
            if owner_id is not None:
                op_df = get_owner_pet_dataframe(owner_id, columns)
                if op_df.empty:
                    print(f"No pets found for Owner {owner_id}\n")
                else:
                    # Display results and convert dataframe to csv.
                    print(op_df)
                    file_name = op_df.at[0, "OwnerLastName"].lower()
                    file_name += f"_{owner_id}.csv"
                    op_df.to_csv(path_or_buf=file_name, index=False)
                    print(f"Printed {file_name}\n")

        elif choice == 4:
            columns = ["OwnerId", "OwnerFirstName", "OwnerLastName",
                       "OwnerEmail", "PetId", "PetName", "PetBreed", "Service",
                       "Date", "Charge"]
            owner_df = get_table_dataframe("OWNER")
            owner_id = get_owner_id(owner_df)
            assert isinstance(owner_id, int)
            if owner_id is not None:
                op_df = get_owner_pet_dataframe(owner_id, columns)
                if op_df.empty:
                    print(f"No pets found for Owner {owner_id}\n")
                else:
                    print(op_df, '\n')
                    first_name = op_df.at[0, "OwnerFirstName"]
                    last_name = op_df.at[0, "OwnerLastName"]
                    owner_name = first_name + " " + last_name
                    print(f"{'Total Charges':-^20}")
                    print(f"{owner_name}'s total charges = "
                          f"{op_df["Charge"].sum()}\n")

        elif choice == 5:
            pets = get_table_dataframe("PETS")
            print(pets)
            breed = get_breed(pets)
            print(breed)

        elif choice == 6:
            print("Thanks for using the program.")


def print_menu():
    """Prints the main menu."""
    options = (
        "1) Display OWNER content and create DataFrame",
        "2) Display PETS content and create DataFrame",
        "3) Retrieve Owner and Pet data for specific Owner",
        "4) Calculate Total Charge by Owner",
        "5) Retrieve pet information by PetBreed",
        "6) Exit")
    print(f"{'Main Menu':-^{max(len(opt) for opt in options)}}")
    for opt in options:
        print(opt)


def get_int_range(min, max):
    """Gets an int within range min to max."""
    keep_going = True
    while keep_going:
        try:
            choice = int(input("Enter menu option: "))
            if choice < min or choice > max:
                raise ValueError
        except ValueError:
            print(f"Please enter a valid number between {min} and {max}.\n")
        else:
            keep_going = False
            assert isinstance(choice, int), "Choice should never not be an int"
            return choice


def get_owner_id(data):
    """Prompts for owner id and validates against db information

    Parameters
    ----------
    data: pd.DataFrame
        DataFrame conatining the owner information

    Returns
    -------
    int
    """
    invalid = True
    # Get user input.
    while invalid:
        try:
            owner_id = int(input("Enter Owner ID: "))
            id_list = data["OwnerId"].astype(int).to_list()
            if owner_id not in id_list:
                print(f"{owner_id} not found")
                raise ValueError
            else:
                invalid = False
        except ValueError:
            print("Please enter a valid OwnerID")
        else:
            return owner_id


def get_breed(data):
    """Prompts user for breed name and validates it against db information.

    Parameters
    ----------
    data: pd.DataFrame
        Dataframe with information from the pets table.

    Returns
    -------
    str
        Pet breed name
    """
    invalid = True
    while invalid:
        try:
            breed = input("Enter breed type: ")
            breed_list = data["PetBreed"].to_list()
            if breed not in breed_list:
                print(f"{breed} not found")
                raise ValueError
            else:
                invalid = False
        except ValueError:
            print("Please enter a valid breed name")
        else:
            return breed


if __name__ == "__main__":
    main()
