import random
from Characters import character as character_class
from Integrations.DnDFiveApi import client as dndfiveapi
from Cli.utils import choose_option

# display character traits function
def display(character):
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

# choose race
def race_options():
    # get request to DnDFiveApi
    # returns list of races
    race_results = dndfiveapi.get_request('/races')

    # map the 'name' index to an array
    races = [race['name'] for race in race_results]

    return races

# choose class
def class_options():
    # get request to DnDFiveApi
    character_class_results = dndfiveapi.get_request('/classes')

    # map the 'name' index to an array
    character_classes = [character_class['name'] for character_class in character_class_results]

    return character_classes

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

def create_character():
    # create a new character
    character = character_class.Character()

    character.name = input("Enter your character's name: ")
    character.race = choose_option(race_options(), 'Choose a Race: ')
    character.char_class = choose_option(class_options(), 'Choose a Class: ')
    character.background = input("\nEnter your character's background: ")
    character.alignment = input("Enter your character's alignment (e.g., Neutral Good): ")
    character.ability_scores = roll_ability_scores()

    return character