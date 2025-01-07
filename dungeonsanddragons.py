import random

import dndfiveapi

class Character:
    def __init__(self):
        self.name = ""
        self.race = ""
        self.char_class = ""
        self.background = ""
        self.alignment = ""
        self.ability_scores = {}

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

def choose_race():
    race_results = dndfiveapi.get_request('/races')
    races = []

    for race in race_results:
        races.append(race['name'])

    print("\nChoose a race:")
    for i, race in enumerate(races, start=1):
        print(f"{i}. {race}")
    choice = int(input("Enter the number of your choice: ")) - 1
    return races[choice]

def choose_class():
    character_class_results = dndfiveapi.get_request('/classes')
    character_classes = []

    for character_class in character_class_results:
        character_classes.append(character_class['name'])

    print("\nChoose a class:")
    for i, char_class in enumerate(character_classes, start=1):
        print(f"{i}. {char_class}")
    choice = int(input("Enter the number of your choice: ")) - 1
    return character_classes[choice]

def roll_ability_scores():
    stats = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
    scores = {}
    print("\nRolling ability scores...")
    for stat in stats:
        rolls = [random.randint(1, 6) for _ in range(4)]
        rolls.remove(min(rolls))  # Drop the lowest roll
        scores[stat] = sum(rolls)
        print(f"{stat}: {scores[stat]} (Rolls: {rolls})")
    return scores

def main():
    print("Welcome to the D&D Character Builder!\n")
    character = Character()

    character.name = input("Enter your character's name: ")
    character.race = choose_race()
    character.char_class = choose_class()
    character.background = input("\nEnter your character's background: ")
    character.alignment = input("Enter your character's alignment (e.g., Neutral Good): ")
    character.ability_scores = roll_ability_scores()

    character.display()

    save = input("Do you want to save this character? (yes/no): ").strip().lower()
    if save == "yes":
        with open(f"{character.name}_character.txt", "w") as file:
            file.write(str(character.__dict__))
        print("Character saved!")

if __name__ == "__main__":
    main()
