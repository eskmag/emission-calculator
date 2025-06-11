def get_float_input(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_int_input(prompt: str) -> int:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_choice_input(prompt: str, choices: dict) -> str:
    while True:
        print(prompt)
        for key, label in choices.items():
            print(f"{key}. {label.capitalize()}")
        choice = input("Enter your choice: ")
        if choice in choices:
            return choices[choice]
        print("Invalid choice. Please try again.")
