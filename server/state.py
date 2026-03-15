class CaptionState:

    def __init__(self):
        self.current_script_name=None
        self.lines=[]
        self.index=0

    def load_script(self, name, lines):
        self.current_script_name = name
        self.lines = lines
        self.index=0

    def switch_script(self, name, lines):
        self.current_script_name=name
        self.lines=lines
        self.index=0

    def next(self):
        if self.index < len(self.lines)-1:
            self.index+=1

    def prev(self):
        if self.index>0:
            self.index-=1

    def jump_top(self):
        self.index=0

    def jump_end(self):
        self.index=len(self.lines)-1

    def current_subtitle(self):
        if not self.lines: return ""
        return self.lines[self.index]["subtitle"]

    def current_prompt(self):
        if not self.lines: return ""
        return self.lines[self.index]["teleprompter"]

    def next_prompts(self, n):
        future = self.lines[self.index+1:self.index+1+n]
        return [l["teleprompter"] for l in future]

    def full_script(self):
        return [l["teleprompter"] for l in self.lines]