# Imports
from colorama import Fore, Back, Style
from datetime import 

# Functions
def log(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time + ": " + message)
