import os


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