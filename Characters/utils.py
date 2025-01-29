import random
import logging
import os
import json
from typing import Union, List, Dict
from Characters import character as character_class
from Integrations.DnDFiveApi import client as dndfiveapi
from Cli.utils import choose_option, list_character_files

# constants for stats, file extension, and directory
STATS = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
FILE_EXTENSION = "_character.txt"
CHARACTER_STORAGE_DIR = "Storage/Characters"

# Configure logging
logging.basicConfig(level=logging.INFO)

def display(character: Union[character_class.Character, type]) -> None:
    """
    display the summary of a character.

    args:
        character (Character): The character object to display.
    """
    print("\n--- Character Summary ---")
    print(f"Name: {character.name}")
    print(f"Race: {character.race}")
    print(f"Class: {character.char_class}")
    print(f"Background: {character.background}")
    print(f"Alignment: {character.alignment}")
    print("Ability Scores:")

    for stat, score in character.ability_scores.items():
        print(f"  {stat}: {score}")

    print("-------------------------\n")

def race_options() -> List[str]:
    """
    fetch available races from the DnDFiveApi.

    returns:
        List[str]: A list of race names.
    """
    try:
        race_results = dndfiveapi.get_request('/races')
        return [race['name'] for race in race_results]
    except Exception as e:
        print(f"Error fetching race options: {e}")
        return []

def class_options() -> List[str]:
    """
    fetch available character classes from the DnDFiveApi.

    returns:
        List[str]: A list of class names.
    """
    try:
        character_class_results = dndfiveapi.get_request('/classes')
        return [char_class['name'] for char_class in character_class_results]
    except Exception as e:
        print(f"Error fetching class options: {e}")
        return []

def roll_ability_scores() -> Dict[str, int]:
    """
    roll ability scores for a character using 4d6 drop the lowest method.

    returns:
        dict[str, int]: a dictionary with stats as keys and rolled scores as values.
    """
    scores = {}
    print("\nRolling ability scores...")

    for stat in STATS:
        rolls = sorted(random.randint(1, 6) for _ in range(4))
        total = sum(rolls[1:])  # Sum the top 3 rolls
        scores[stat] = total
        print(f"{stat}: {total} (Rolls: {rolls})")

    return scores

def create_character() -> character_class.Character:
    """
    create a new character by gathering user inputs and rolling ability scores.

    returns:
        character: The newly created character object.
    """
    character = character_class.Character()

    character.name = input("Enter your character's name: ")
    races = race_options()

    if races:
        character.race = choose_option(races, 'Choose a Race: ')
    else:
        character.race = "Unknown"

    classes = class_options()

    if classes:
        character.char_class = choose_option(classes, 'Choose a Class: ')
    else:
        character.char_class = "Unknown"

    character.background = input("\nEnter your character's background: ")
    character.alignment = input("Enter your character's alignment (e.g., Neutral Good): ")
    character.ability_scores = roll_ability_scores()

    return character

def get_character_file_path(character: character_class.Character) -> str:
    """
    construct the file path for a character in the storage directory.
    """

    # ensure the storage directory exists
    os.makedirs(CHARACTER_STORAGE_DIR, exist_ok=True)
    return os.path.join(CHARACTER_STORAGE_DIR, f"{character.name}{FILE_EXTENSION}")


def save_character(character: character_class.Character) -> str:
    """
    save the character's details to a text file in the storage directory.
    """
    file_path = get_character_file_path(character)

    try:
        with open(file_path, "w") as file:
            # save the character's attributes as a string
            file.write(str(character.__dict__))

        logging.info(f"Character saved as {file_path}!")

        return file_path
    except Exception as error:
        logging.error(f"An error occurred while saving the character: {error}")

        raise

def load_character() -> Union[dict[str, str], None]:
    """
    loads the contents of the given character file and returns it as a Python object.

    :return: the JSON contents of the file as a Python object, or None if an error occurs.
    """
    character_files = list_character_files(CHARACTER_STORAGE_DIR)

    character_file = choose_option(character_files, "Choose a character to load:")
    path_and_file = CHARACTER_STORAGE_DIR + "/" + character_file

    try:
        with open(path_and_file, 'r') as file:
            # parse the JSON contents of the file
            character_data = json.load(file)
            return character_data
    except FileNotFoundError:
        print(f"Error: File '{character_file}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{character_file}' does not contain valid JSON.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return None


