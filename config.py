import json

with open("config.json" , "r") as f:
    conf = json.load(f)

TOKEN = conf['bot-token']
PREFIX = conf['prefix']