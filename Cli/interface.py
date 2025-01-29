from Characters import utils as character_utils
from Cli.utils import choose_option

def load_or_create():
    """
    determine whether to load an existing character or create a new one.
    """
    load_or_create = choose_option(["Load", "Create"], "Would you like to load an existing character or create a new one?")

    if load_or_create == 'Load':
        begin_load_character_creation()
    else:
        begin_character_creation()

def begin_character_creation():
    """
    entry point for creating a D&D character.
    """
    print("Welcome to the D&D Character Builder!\n")

    # create the character
    character = character_utils.create_character()

    # display the created character
    character_utils.display(character)

    # prompt to save the character
    save = input("Do you want to save this character? (yes/no): ").strip().lower()

    if save == "yes":
        character_utils.save_character(character)

def begin_load_character_creation():
    """
    entry point for loading a D&D character.
    """
    character_json = character_utils.load_character()
    character = type('Character', (object,), character_json)

    # display the created character
    character_utils.display(character)
