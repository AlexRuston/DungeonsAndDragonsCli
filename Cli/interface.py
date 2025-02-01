from Characters import utils as character_utils
from Cli.utils import choose_option


def load_or_create():
    """
    determine whether to load an existing character or create a new one
    """
    action = choose_option(["Load", "Create"], "Would you like to load an existing character or create a new one?")

    if action == 'Load':
        begin_load_character_creation()
    elif action == 'Create':
        begin_character_creation()
    else:
        print("Invalid selection. Exiting.")


def begin_character_creation():
    """
    entry point for creating a D&D character
    """
    print("Welcome to the D&D Character Builder!\n")

    # create and display the character
    character = character_utils.create_character()
    character_utils.display(character)

    # prompt to save the character
    if input("Do you want to save this character? (yes/no): ").strip().lower() == "yes":
        character_utils.save_character(character)


def begin_load_character_creation():
    """
    entry point for loading a D&D character
    """
    character_data = character_utils.load_character()

    if not character_data:
        print("Failed to load character.")
        return

    # using dataclass if Character class exists
    if hasattr(character_utils, "Character"):
        character = character_utils.Character(**character_data)
    else:
        character = type("Character", (object,), character_data)

    character_utils.display(character)
