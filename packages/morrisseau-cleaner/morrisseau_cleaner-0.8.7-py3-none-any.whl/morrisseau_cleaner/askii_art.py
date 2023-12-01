# This file will generate an ASKII art banner for the cleaner module.

import pyfiglet
import termcolor
import colorama

def askii_art_main():
    colorama.init()
    art = pyfiglet.figlet_format('Morrisseau Project')
    colored_art = termcolor.colored(art, color='magenta')
    print(colored_art)
    colorama.deinit()