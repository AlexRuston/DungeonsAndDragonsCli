import random

from Integrations.DnDFiveApi import client as dndfiveapi

# create character class
class Character:
    def __init__(self):
        self.name = ""
        self.race = ""
        self.char_class = ""
        self.background = ""
        self.alignment = ""
        self.ability_scores = {}

# display character traits function
    def display(self):
        print("\n--- Character Summary ---")
        print(f"Name: {self.name}")
        print(f"Race: {self.race}")
        print(f"Class: {self.char_class}")
        print(f"Background: {self.background}")
        print(f"Alignment: {self.alignment}")
        print("Ability Scores:")
        for stat, score in self.ability_scores.items():
            print(f"  {stat}: {score}")
        print("-------------------------\n")

# function to choose from a list with user input
def choose_option(options, prompt):
    # print the message prompt
    print(f"\n{prompt}")

    # loop the options
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    # validation against a user picking an invalid choice
    while True:
        try:
            choice = int(input("Enter the number of your choice: ")) - 1
            if 0 <= choice < len(options):
                return options[choice]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# choose race
def choose_race():
    # get request to DnDFiveApi
    # returns list of races
    race_results = dndfiveapi.get_request('/races')

    # map the 'name' index to an array
    races = [race['name'] for race in race_results]

    return choose_option(races, "Choose a race:")

# choose class
def choose_class():
    # get request to DnDFiveApi
    character_class_results = dndfiveapi.get_request('/classes')

    # map the 'name' index to an array
    character_classes = [character_class['name'] for character_class in character_class_results]

    return choose_option(character_classes, "Choose a class:")

# roll ability scores
def roll_ability_scores():
    # can't find an api call to get the stats list, so I've hard coded it
    stats = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

    # initiate empty scores dict
    scores = {}

    print("\nRolling ability scores...")

    # loop the stats
    for stat in stats:
        rolls = [random.randint(1, 6) for _ in range(4)]

        # drop the lowest roll
        rolls.remove(min(rolls))

        # sum of remaining rolls given to the stat score
        scores[stat] = sum(rolls)

        print(f"{stat}: {scores[stat]} (Rolls: {rolls})")

    return scores

# entry point
def begin_character_creation():
    print("Welcome to the D&D Character Builder!\n")

    # create a new character
    character = Character()

    character.name = input("Enter your character's name: ")
    character.race = choose_race()
    character.char_class = choose_class()
    character.background = input("\nEnter your character's background: ")
    character.alignment = input("Enter your character's alignment (e.g., Neutral Good): ")
    character.ability_scores = roll_ability_scores()

    character.display()

    save = input("Do you want to save this character? (yes/no): ").strip().lower()

    # store the new character to a txt file
    if save == "yes":
        with open(f"{character.name}_character.txt", "w") as file:
            file.write(str(character.__dict__))

        print("Character saved!")