import os


def createIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    return True
