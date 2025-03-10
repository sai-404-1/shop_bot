import json

import myConstants
def jsonParser(jsonFileName):
    result = dict()
    with open(jsonFileName, 'r', encoding="utf8") as f:
        result = json.load(f)
    return result

def getMainDataset():
    return jsonParser(myConstants.CONSTANTS.MAIN_DATASET_PATH)