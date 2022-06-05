import json

def get_config():
    try:
        with open('config.json') as f:
            config = json.load(f)
        return config
    except:
        print("[ ERROR ] -> Config file not found")
        return None
    

def set_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f)