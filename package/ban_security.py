import os

class Ban:
    def __init__(self, guild):
        self.guild = guild
        self.list = []
        if not os.path.exists(f"../assets/server/{self.guild}"):
            os.mkdir(f"../assets/server/{self.guild}")
        if not os.path.exists(f"../assets/server/{self.guild}/ban.txt"):
            with open(f"../assets/server/{self.guild}/ban.txt", "a+") as file:
                file.close()
        else:
            with open(f"../assets/server/{self.guild}/ban.txt", "r+") as file:
                for lines in file.readlines():
                    self.list.append(lines.replace("\n", ""))

    def add(self, user):
        with open(f"../assets/server/{self.guild}/ban.txt", "a+") as file:
            file.write(f"{user}\n")

    def remove(self, user):
        ban_list = []
        with open(f"../assets/server/{self.guild}/ban.txt", "r+") as file:
            for lines in file.readlines():
                if lines.replace("\n", "") != str(user):
                    ban_list.append(lines)
            with open(f"../assets/server/{self.guild}/ban.txt", "w+") as file:
                file.writelines(ban_list)

    def check(self, user):
        for ban in self.list:
            if ban == str(user):
                return True