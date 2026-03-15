import yaml


class Config:

    def __init__(self, path):
        self.path = path
        self.load()

    def load(self):
        with open(self.path, "r", encoding="utf8") as f:
            self.data = yaml.safe_load(f)

    def get(self, key):
        return self.data.get(key)
