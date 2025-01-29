import os

def choose_option(options, prompt):
    """
    display a prompt and a list of options for the user to choose from.

    args:
        options (list): a list of options to display.
        prompt (str): a message prompting the user to make a choice.

    returns:
        any: The selected option from the list.
    """
    print(f"\n{prompt}")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    while True:
        choice = input("Enter the number of your choice: ")

        if choice.isdigit():
            choice = int(choice) - 1

            if 0 <= choice < len(options):
                return options[choice]

        print("Invalid choice. Please try again.")


def list_character_files(directory_path):
    """
    lists the names of the files in the specified directory and removes "_character.txt" from the names.

    :param directory_path: path to the directory containing character files.
    :return: list of cleaned file names.
    """

    try:
        # list all files in the given directory
        files = os.listdir(directory_path)

        # remove "_character.txt" from file names and return the cleaned names
        cleaned_names = files
        #cleaned_names = [file.replace("_character.txt", "") for file in files if file.endswith("_character.txt")]

        return cleaned_names
    except FileNotFoundError:
        print(f"Error: Directory '{directory_path}' not found.")

        return []
    except Exception as e:
        print(f"An error occurred: {e}")

        return []