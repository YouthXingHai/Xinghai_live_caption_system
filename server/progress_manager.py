import json
import os

class ProgressManager:

    def __init__(self, path):
        self.path=path
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

    def save(self,script,index):
        with open(self.path,"w") as f:
            json.dump({"script":script,"index":index},f)

    def load(self):
        try:
            with open(self.path) as f:
                return json.load(f)
        except:
            return None