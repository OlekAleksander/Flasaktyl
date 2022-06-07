from colorama import Fore, Back, Style
from datetime import datetime
def log(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time + ": " + message)
