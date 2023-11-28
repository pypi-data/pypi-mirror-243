import os, shutil

def checkdir(path, reset = True):
    if os.path.exists(path):
        if reset:
            shutil.rmtree(path)
            os.makedirs(path)
    else:
        os.makedirs(path)

    return path


