import os
import json

def createDirectoryIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    return True

def createFileIfNotExists(path, content = ""):
    if not os.path.exists(path):
        f = open(path, 'a')
        f.write(content)
        f.close()

def readConfigFile():
    f = open("./configuration.json")
    data = json.load(f)
    f.close()
    return data
