import random
import logging
import json
from pathlib import Path
from typing import Union, List, Dict
from Characters import character as character_class
from Integrations.DnDFiveApi import client as dndfiveapi
from Cli.utils import choose_option, list_character_files

STATS = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
FILE_EXTENSION = "_character.txt"
CHARACTER_STORAGE_DIR = Path("Storage/Characters")

logging.basicConfig(level=logging.INFO)

def display(character: Union[character_class.Character, type]) -> None:
    """
    display the summary of a character
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
    fetch available races from the DnDFiveApi
    """
    try:
        return [race['name'] for race in dndfiveapi.get_request('/races')]
    except Exception as e:
        logging.error(f"Error fetching race options: {e}")
        return []

def class_options() -> List[str]:
    """
    fetch available character classes from the DnDFiveApi
    """
    try:
        return [char_class['name'] for char_class in dndfiveapi.get_request('/classes')]
    except Exception as e:
        logging.error(f"Error fetching class options: {e}")
        return []

def roll_ability_scores() -> Dict[str, int]:
    """
    roll ability scores using 4d6 drop-the-lowest method
    """
    return {
        stat: sum(sorted(random.randint(1, 6) for _ in range(4))[1:]) for stat in STATS
    }

def create_character() -> character_class.Character:
    """
    create a new character by gathering user inputs and rolling ability scores
    """
    character = character_class.Character()
    character.name = input("Enter your character's name: ")
    character.race = choose_option(race_options(), 'Choose a Race: ') or "Unknown"
    character.char_class = choose_option(class_options(), 'Choose a Class: ') or "Unknown"
    character.background = input("\nEnter your character's background: ")
    character.alignment = input("Enter your character's alignment (e.g., Neutral Good): ")
    character.ability_scores = roll_ability_scores()
    return character

def get_character_file_path(character: character_class.Character) -> Path:
    """
    construct the file path for storing a character
    """
    CHARACTER_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    return CHARACTER_STORAGE_DIR / f"{character.name}{FILE_EXTENSION}"

def save_character(character: character_class.Character) -> str:
    """
    save character details to a file
    """
    file_path = get_character_file_path(character)
    try:
        with file_path.open("w") as file:
            json.dump(character.__dict__, file, indent=4)
        logging.info(f"Character saved as {file_path}!")
        return str(file_path)
    except Exception as error:
        logging.error(f"Error saving character: {error}")
        raise

def load_character() -> Union[Dict[str, str], None]:
    """
    load a character from a file
    """
    character_files = list_character_files(str(CHARACTER_STORAGE_DIR))
    if not character_files:
        logging.warning("No characters found to load.")
        return None

    character_file = choose_option(character_files, "Choose a character to load:")
    if not character_file:
        return None

    file_path = CHARACTER_STORAGE_DIR / f"{character_file}"

    try:
        with file_path.open("r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File '{file_path}' not found.")
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in file '{file_path}'.")
    except Exception as e:
        logging.error(f"Error loading file: {e}")
    return None
