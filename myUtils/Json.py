import json

def jsonParser(jsonFileName):
    result = dict()
    with open(jsonFileName, 'r', encoding="utf8") as f:
        result = json.load(f)
    return result