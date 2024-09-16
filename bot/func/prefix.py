import json
import os

def load_prefixes():
    if not os.path.exists('./json/prefix/prefix.json'): 
        return {}
    with open('./json/prefix/prefix.json', 'r') as f:
        return json.load(f)

def save_prefixes(prefixes):
    with open('./json/prefix/prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

def get_prefix(bot, message):
    if message.guild is None:
        return 'L.'
    prefixes = load_prefixes()
    return prefixes.get(str(message.guild.id), 'L.') 


