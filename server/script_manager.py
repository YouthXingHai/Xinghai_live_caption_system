import os
import re


class ScriptManager:

    def __init__(self, folder):
        self.folder = folder
        self.scripts = {}
        self.load_scripts()

    def load_scripts(self):

        self.scripts = {}

        for f in os.listdir(self.folder):

            if not f.endswith(".txt"):
                continue

            path = os.path.join(self.folder, f)

            with open(path, "r", encoding="utf8") as file:
                lines = [x.strip() for x in file.readlines() if x.strip()]

            parsed = [self.parse_line(x) for x in lines]

            self.scripts[f] = parsed

    def parse_line(self, line):

        cues = re.findall(r"\[(.*?)\]", line)

        subtitle = re.sub(r"\[.*?\]", "", line).strip()

        return {
            "raw": line,
            "subtitle": subtitle,
            "teleprompter": line,
            "cues": cues
        }

    def list_scripts(self):
        return list(self.scripts.keys())

    def get(self, name):
        return self.scripts.get(name, [])
