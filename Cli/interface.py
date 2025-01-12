from Characters import utils as character_utils

# entry point
def begin_character_creation():
    print("Welcome to the D&D Character Builder!\n")

    # create the character
    character = character_utils.create_character()

    # display the created character
    character_utils.display(character)

    # store the new character to a txt file
    save = input("Do you want to save this character? (yes/no): ").strip().lower()

    if save == "yes":
        with open(f"{character.name}_character.txt", "w") as file:
            file.write(str(character.__dict__))

        print("Character saved!")