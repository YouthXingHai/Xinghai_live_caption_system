import os

import yaml


class CaptionState:

    def __init__(self, file):

        self.file = file
        self.script = None
        self.index = 0

        self.load()

    def load(self):

        if not os.path.exists(self.file):
            return

        with open(self.file, "r") as f:
            data = yaml.safe_load(f)

        self.script = data.get("script")
        self.index = data.get("index", 0)

    def save(self):

        os.makedirs("runtime", exist_ok=True)

        with open(self.file, "w") as f:
            yaml.dump({
                "script": self.script,
                "index": self.index
            }, f)

    def next(self, max_len):

        if self.index < max_len - 1:
            self.index += 1
            self.save()

    def prev(self):

        if self.index > 0:
            self.index -= 1
            self.save()

    def first(self):

        self.index = 0
        self.save()

    def last(self, max_len):

        self.index = max_len - 1
        self.save()
