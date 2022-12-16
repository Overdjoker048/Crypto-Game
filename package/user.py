import json
import os
import time

class User:
    def __init__(self, host, guild):
        self.id = host.id
        self.guild = guild
        self.name = str(host.name)
        if not os.path.exists(f"../assets/server/{self.guild}"):
            os.mkdir(f"../assets/server/{self.guild}")
        if not os.path.exists(f"../assets/server/{self.guild}/user"):
            os.mkdir(f"../assets/server/{self.guild}/user")
        try:
            with open(f"../assets/server/{self.guild}/user/{self.id}.json", "r+") as file:
                contenue = json.load(fp=file)
            self.money = contenue["money"]
            self.ethereum = contenue["ethereum"]
            self.bitcoin = contenue["bitcoin"]
            self.pi = contenue["pi"]
            self.sec = contenue["sec"]
            self.mining = contenue["mining"]
            self.warn = contenue["warn"]
        except:
            info = {
                "name": self.name,
                "ethereum": 0.0,
                "bitcoin": 0.0,
                "pi": 0.0,
                "money": 10000,
                "sec": None,
                "mining": False,
                "warn": 0,
            }
            with open(f"../assets/server/{self.guild}/user/{self.id}.json", "w+") as file:
                json.dump(info, file, indent=2)
            self.ethereum = 0.0
            self.bitcoin = 0.0
            self.pi = 0.0
            self.money = 10000
            self.sec = None
            self.mining = False
            self.warn = 0

    def save(self, name=None, ethereum=None, bitcoin=None, pi=None, money=None, sec=None, mining=None, warn=None):
        if name != None:
            self.name = name
        if ethereum != None:
            self.ethereum = ethereum
        if bitcoin != None:
            self.bitcoin = bitcoin
        if pi != None:
            self.pi = pi
        if money != None:
            self.money = money
        if sec != None:
            self.sec = sec
        if mining != None:
            self.mining = mining
        if warn != None:
            self.warn = warn
        info = {
            "name": self.name,
            "ethereum": self.ethereum,
            "bitcoin": self.bitcoin,
            "pi": self.pi,
            "money": self.money,
            "sec": self.sec,
            "mining": self.mining,
            "warn": self.warn,
        }
        with open(f"../assets/server/{self.guild}/user/{self.id}.json", "w+") as file:
            json.dump(info, file, indent=2)

    def mining_run(self):
        self.mining = True
        self.sec = int(time.time()) + 3600