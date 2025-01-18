def choose_option(options, prompt):
    """
    display a prompt and a list of options for the user to choose from.

    args:
        options (list): a list of options to display.
        prompt (str): a message prompting the user to make a choice.

    returns:
        any: The selected option from the list.
    """
    print(f"\n{prompt}")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    while True:
        choice = input("Enter the number of your choice: ")

        if choice.isdigit():
            choice = int(choice) - 1

            if 0 <= choice < len(options):
                return options[choice]

        print("Invalid choice. Please try again.")