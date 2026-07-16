from distil_engine import *

boot()

while True:

    command = input(
        "DISTIL > "
    ).lower().strip()

    if handle_natural_command(command):
        continue

    if command == "help":
        help_menu()

    elif command == "study":
        study()

    elif command == "focus":
        focus()

    elif command == "exit":

        print(
            "DISTIL OFFLINE"
        )

        break

    else:

        print(
            "Unknown command.\n"
        )