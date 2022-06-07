try:
   from colorama import Fore, Back, Style

def log(message,type):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time + "| " + message)
