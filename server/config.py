import yaml

class Config:

    def __init__(self,path="config/config.yaml"):

        with open(path,"r",encoding="utf8") as f:
            self.data=yaml.safe_load(f)

    def get(self,key):

        parts=key.split(".")
        v=self.data

        for p in parts:
            v=v[p]

        return v