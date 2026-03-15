import os, re

class ScriptManager:

    def __init__(self, folder):
        self.folder = folder
        self.scripts = {}
        self.load_all_scripts()

    def list_scripts(self):
        return list(self.scripts.keys())

    def load_all_scripts(self):
        for f in os.listdir(self.folder):
            if f.endswith(".txt"):
                self.scripts[f] = self.load_script(f)

    def load_script(self, name):
        path = os.path.join(self.folder, name)
        lines=[]
        with open(path,"r",encoding="utf8") as f:
            for l in f:
                t = l.strip()
                if not t: continue
                cue = bool(re.match(r"^\[.*\]$", t))
                subtitle = "" if cue else t
                lines.append({
                    "teleprompter": t,
                    "subtitle": subtitle,
                    "cue": cue
                })
        return lines

    def get_script(self, name):
        return self.scripts.get(name, [])