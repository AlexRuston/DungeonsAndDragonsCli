import random
from typing import List, Dict
from Characters import character as character_class
from Integrations.DnDFiveApi import client as dndfiveapi
from Cli.utils import choose_option

# constants for stats
STATS = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

def display(character: character_class.Character) -> None:
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
