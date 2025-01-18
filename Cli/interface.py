from Characters import utils as character_utils

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
