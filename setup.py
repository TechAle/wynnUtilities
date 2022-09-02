import subprocess
import sys
import requests
import os
from crafter import creations

#subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

try:
    os.makedirs("./crafter/dataset")
except FileExistsError:
    pass
try:
    os.makedirs("./crafter/optCrafter/utils")
except FileExistsError:
    pass

creations.createDataset()


r = requests.get("https://github.com/nlohmann/json/releases/download/v3.11.2/json.hpp")
with open("./crafter/optCrafter/utils/json.hpp", "wb") as f:
    f.write(r.content)