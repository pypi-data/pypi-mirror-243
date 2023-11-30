import tkinter as tk
from tkinter import filedialog
import re
import csv
import datetime

def highlight_changes(old_str, new_str) -> None:
    highlighted_str = ""

    for old_char, new_char in zip(old_str, new_str):
        if old_char != new_char:
            highlighted_str += f"\033[91m{new_char}\033[0m"  # Red color for additions
        else:
            highlighted_str += old_char

    # Handle remaining characters if one string is longer than the other
    if len(new_str) > len(old_str):
        highlighted_str += f"\033[91m{new_str[len(old_str):].replace(' ', '␣')}\033[0m"

    print(f"-: {old_str.replace(' ', '␣')} -> {new_str.replace(' ', '␣')} +: {highlighted_str}")

def get_file_path() -> str:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


def get_output_file_path(input_file: str) -> str:
    # Pattern to match the 'output-N' format at the end of the file name
    pattern = r'output-(\d+)'

    # Check if the input file name contains 'output-N' format
    match = re.search(pattern, input_file)
    if match:
        # Extract the version number and increment it
        version = int(match.group(1)) + 1
        output_file = re.sub(pattern, f'output-{version}', input_file)
    else:
        # If 'output-N' format is not found, add it with version 1 before the file extension
        base, ext = input_file.rsplit('.', 1)
        output_file = f"{base}-output-1.{ext}"

    return output_file

def get_column_index(column_name: str) -> int:
    while True:
        try: 
            index = int(input(f"Enter the index of the {column_name} column: "))
            return index-1
        except ValueError:
            print("Invalid value. Please try again.")

def clean_spaces(input_file: str, output_file: str) -> None:
    with open(input_file, 'r') as input_csv:
        with open(output_file, 'w') as output_csv:
            reader = csv.reader(input_csv)
            writer = csv.writer(output_csv)
            for row in reader:
                new_row = []
                for cell in row:
                    original_cell = cell
                    new_cell = cell.strip()
                    new_cell = re.sub(' +', ' ', new_cell)
                    new_row.append(new_cell)
                    highlight_changes(original_cell, new_cell)
                writer.writerow(new_row)


def clean_pipes(input_file: str, output_file: str) -> None:
    with open(input_file, 'r') as input_csv:
        with open(output_file, 'w') as output_csv:
            reader = csv.reader(input_csv)
            writer = csv.writer(output_csv)
            for row in reader:
                new_row = []
                for cell in row:
                    original_cell = cell
                    new_cell = new_cell.replace(' |', '|').replace('| ', '|')
                    new_row.append(cell)
                    highlight_changes(original_cell, new_cell)
                writer.writerow(new_row)

def clean_dates(input_file: str, output_file: str) -> None:
    date_column_index = get_column_index("date")
    known_formats = {
        r'\d{4}-\d{2}-\d{2}': '%Y-%m-%d',  # YYYY-MM-DD is a correct format
        r'\d{4}-\d{2}': '%Y-%m',  # YYYY-MM is a correct format 
        r'\d{4}-\d{4}': 'YYYY-YYYY',  # YYYY-YYYY is a correct format
        r'\d{4}': '%Y',  # YYYY is a correct format
        r'c\.(\s+)?\d{4}(\s+)?(-|to|–)(\s+)?c\.(\s+)?\d{4}\b': 'c. YYYY-c. YYYY',  # Matches various formats indicating a range c. YYYY-c. YYYY
        r'c\.(\s+)?\d{4}\b': 'c. %Y',
        r'\b(not\s+known|unknown|not\s+sure|uncertain|unspecified|unidentifiable|n(\.|a)|N(\.|a)|Nan|NAN)\b': 'n.d.',  # Matches various representations implying "not known" or "unknown" to n.d.
        r'\b(\d{1,2}[./-]\d{1,2}[./-]\d{4}|\d{1,2}[./-]\d{2}[./-]\d{2}|\d{4}[./-]\d{2}[./-]\d{2})\b': '%Y-%m-%d', 
        # DD-MM-YYYY or MM-DD-YYYY: Matches date formats like 01-01-2023 or 12-31-2023.
        # MM/DD/YYYY or DD/MM/YYYY: Matches formats like 01/01/2023 or 12/31/2023.
        # M/D/YY or D-M-YY: Matches formats like 1/1/23 or 31-12-23.
        # YY/MM/DD or YY-MM-DD: Matches formats like 23/01/01 or 23-12-31.

        r'\d{2}\.\d{2}\.\d{4}': '%Y-%m-%d',  # Matches MM.DD.YYYY, change to YYYY-MM-DD
        r'\d{4}\.\d{2}\.\d{2}': '%Y-%m-%d',  # Matches YYYY.MM.DD, change to YYYY-MM-DD
        r'\d{2}\.\d{2}\.\d{2}': '%Y-%m-%d',  # Matches MM.DD.YY, change to YYYY-MM-DD
        r'\d{1,2}-\d{1,2}-\d{2}': '%Y-%m-%d',  # Matches D-M-YY, change to YYYY-MM-DD
        r'\d{1,2}\.\d{1,2}\.\d{2}': '%Y-%m-%d',  # Matches D.M.YY, change to YYYY-MM-DD
        r'\d{1,2}/\d{1,2}/\d{2}': '%Y-%m-%d',  # Matches M/D/YY, change to YYYY-MM-DD
        r'\d{4}-\d{2}': '%Y-%m',  # YYYY-MM
        r'\d{2}/\d{4}': '%Y-%m',  # Matches MM/YYYY, change to YYYY-MM
        r'\d{4}/\d{2}': '%Y-%m',  # Matches YYYY/MM, change to YYYY-MM
        r'\d{2}/\d{2}/\d{2}': '%Y-%m-%d',  # Matches MM/DD/YY, change to YYYY-MM-DD
    }

    with open(input_file, 'r') as input_csv:
        with open(output_file, 'w') as output_csv:
            reader = csv.reader(input_csv)
            writer = csv.writer(output_csv)
            for row_index, row in enumerate(reader):
                new_row = []
                for cell_index, cell in enumerate(row):
                    if cell_index == date_column_index:
                        original_cell = cell
                        for pattern, conversion in known_formats.items():
                            if re.fullmatch(pattern, cell):
                                if conversion or pattern == None:
                                    print(f"I've found a value that I don't know how to handle. The cell is " 
                                          f"in positions {row_index}, {cell_index}. the cell is {cell}.")
                                    if input("Would you like to change this manually? (y/n): ").lower() == "y":
                                        cell = input("Enter the new value: ").strip()
                                    else :
                                        print("I'll keep the original value.")
                                        cell = original_cell
                                else:
                                    cell = datetime.strptime(cell, conversion).strftime(conversion)
                                    break
                        if cell != original_cell:
                            highlight_changes(original_cell, cell)
                        new_row.append(cell)
            writer.writerow(new_row)
    print("Those dates do be looking clean. Nice job!")

def clean_titles(input_file: str, output_file: str) -> None:
    title_column_index = get_column_index("title")
    articles = [
        "a",
        "abaft",
        "aboard",
        "about",
        "above",
        "absent",
        "across",
        "afore",
        "after",
        "against",
        "along",
        "alongside",
        "amid",
        "amidst",
        "among",
        "amongst",
        "an",
        "anenst",
        "apropos",
        "apud",
        "around",
        "as",
        "aside",
        "astride",
        "at",
        "athwart",
        "atop",
        "barring",
        "before",
        "behind",
        "below",
        "beneath",
        "beside",
        "besides",
        "between",
        "beyond",
        "but",
        "by",
        "circa",
        "concerning",
        "despite",
        "down",
        "during",
        "except",
        "excluding",
        "failing",
        "following",
        "for",
        "forenenst",
        "from",
        "given",
        "in",
        "including",
        "inside",
        "into",
        "lest",
        "like",
        "mid",
        "midst",
        "minus",
        "modulo",
        "near",
        "next",
        "notwithstanding",
        "of",
        "off",
        "on",
        "onto",
        "opposite",
        "out",
        "outside",
        "over",
        "pace",
        "past",
        "per",
        "plus",
        "pro",
        "qua",
        "regarding",
        "round",
        "sans",
        "save",
        "since",
        "than",
        "the",
        "through",
        "throughout",
        "till",
        "times",
        "to",
        "toward",
        "towards",
        "under",
        "underneath",
        "unlike",
        "until",
        "unto",
        "up",
        "upon",
        "versus",
        "via",
        "vice",
        "with",
        "within",
        "without",
        "worth"
    ]
    with open(input_file, 'r') as input_csv:
        with open(output_file, 'w') as output_csv:
            reader = csv.reader(input_csv)
            writer = csv.writer(output_csv)
            for row_index, row in enumerate(reader):
                new_row = []
                for cell_index, cell in enumerate(row):
                    if cell_index == title_column_index:
                        original_cell = cell
                        new_cell = cell.strip()
                        for word_index, word in enumerate(new_cell.split()):
                            if word_index == 0 or word not in articles:
                                new_cell = new_cell.replace(word, word.capitalize())
                            else :
                                new_cell = new_cell.replace(word, word.lower())
                        if new_cell != original_cell:
                            highlight_changes(original_cell, new_cell)
                        new_row.append(new_cell)
        print("Titles are now capitalized.")

def clean_pages(input_file: str, output_file: str) -> None: 
    page_column_index = get_column_index("page")
    with open(input_file, 'r') as input_csv:
        with open(output_file, 'w') as output_csv:
            reader = csv.reader(input_csv)
            writer = csv.reader(output_csv)
            for row_index, row in enumerate(reader):
                new_row = []
                for cell_index, cell in enumerate(row):
                    if cell_index == page_column_index:
                        original_cell = cell
                        new_cell = cell.strip()
                        # Use a regular expression to extract the page number format
                        page_number_pattern_match = re.search(r'(\d+)(?:\s*-\s*(\d+))?', new_cell)
                       
                        if page_number_pattern_match:
                           # Reconstruct the cell with cleaned page number format
                            start_page, end_page = page_number_pattern_match.groups()
                            if end_page:
                                cell = f"{start_page}-{end_page}"
                            else:
                                cell = start_page
                    if cell != original_cell:
                        highlight_changes(original_cell, cell)
                    new_row.append(new_cell)
                writer.writerow(new_row)
    print("Pages are now clean.")


    


                                        
                                    
                                    




