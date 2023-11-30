from .askii_art import askii_art_main
from morrisseau_cleaner import functions

def display_menu():
    """Display the menu of options for the user."""

    print("Welcome to the Morrisseau Project Cleaner Module!")
    print("  choose a file - Choose input and output files")
    print("  clean spaces - Clean spaces in the chosen file")
    print("  clean pipes - Clean pipes in the chosen file")
    print("  help - Show available commands")
    print("  clean dates - Clean dates in the chosen file")
    print("  clean titles - Clean titles in the chosen file")
    print("  clean pages - Clean pages in the chosen file")
    print("  exit - Exit the program")

def terminal_main():
    askii_art_main()
    display_menu()

    input_file = None
    output_file = None

    while True:
        command = input("Enter a command: ").lower()
        input_file = None 
        output_file = None
        if command == "choose a file":
            input_file = functions.get_file_path()
            output_file = functions.get_output_file_path(input_file)
        if input_file and output_file:
            if command == "clean spaces":
                functions.clean_spaces(input_file, output_file)
            elif command == "clean pipes":
                functions.clean_pipes(input_file, output_file)
            elif command == "clean dates":
                functions.clean_dates(input_file, output_file)
            elif command == "clean titles":
                functions.clean_titles(input_file, output_file)
            elif command == "clean pages":
                functions.clean_pages(input_file, output_file)
        else: 
            print("Please choose a file first.")
        if command == "help":
            display_menu()
        if command == "exit":
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    terminal_main()
