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