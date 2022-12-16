import json
import os

class Crypto:
    def __init__(self, guild):
        self.guild = guild
        if not os.path.exists(f"../assets/server/{self.guild}"):
            os.mkdir(f"../assets/server/{self.guild}")
        if not os.path.exists(f"../assets/server/{self.guild}/crypto.json"):
            info = {
                "ethereum": 1000,
                "bitcoin": 10000,
                "pi": 500,
            }
            with open(f"../assets/server/{self.guild}/crypto.json", "w+") as file:
                json.dump(info, file, indent=2)
            self.ethereum = 1000
            self.bitcoin = 10000
            self.pi = 500

        else:
            with open(f"../assets/server/{self.guild}/crypto.json", "r+") as file:
                contenue = json.load(fp=file)
            self.ethereum = contenue["ethereum"]
            self.bitcoin = contenue["bitcoin"]
            self.pi = contenue["pi"]

    def save(self, ethereum=None, bitcoin=None, pi=None):
        if pi != None:
            self.pi = pi
        if bitcoin != None:
            self.bitcoin = bitcoin
        if ethereum != None:
            self.ethereum = ethereum
        value = {
            "ethereum": self.ethereum,
            "bitcoin": self.bitcoin,
            "pi": self.pi,
        }
        with open(f"../assets/server/{self.guild}/crypto.json", "w+") as file:
            json.dump(value, file, indent=2)
            file.close()