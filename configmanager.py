import json
import logger
from colorama import init, Fore, Back, Style

def get_config():
    try:
        with open('config.json') as f:
            config = json.load(f)
        return config
    except:
        logger.log(Back.RED + "[ ERROR ] -> Config file corrupted")
        return None

def set_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f)
