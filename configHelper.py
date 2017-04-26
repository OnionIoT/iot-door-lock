import os
import json

# read a json config file
def readConfig(filename='config.json'):
    # build the absolute filepath if running via another script
    dirName = os.path.dirname(os.path.abspath(__file__))
    fullPath = '/'.join([dirName, filename])
    # read the config file
    with open(fullPath) as file:
        data = json.load(file)
        return data