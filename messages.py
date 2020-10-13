import json, random

messages = open("./messages.json").read()
messages = json.loads(messages)

def randomMessage(key):
    return random.choice(list(messages[key]))
