from datetime import datetime
from package.ban_security import Ban
from package import addon
import os
import json

def main():
    addon.setup()

    def add_warn(path):
        with open(path, "r+") as file:
            contenue = json.load(fp=file)
            name = contenue["name"]
            money = contenue["money"]
            ethereum = contenue["ethereum"]
            bitcoin = contenue["bitcoin"]
            pi = contenue["pi"]
            sec = contenue["sec"]
            mining = contenue["mining"]
            warn = contenue["warn"]
        info = {
            "name": name,
            "ethereum": ethereum,
            "bitcoin": bitcoin,
            "pi": pi,
            "money": money,
            "sec": sec,
            "mining": mining,
            "warn": float(warn) + 1,
        }
        with open(path, "w+") as file:
            json.dump(info, file, indent=2)
        if float(warn) + 1 == 3:
            Ban(guild_list[line]).add(id_list[line])

    last_edit = 0

    time_list = []
    guild_list = []
    cmd_list = []
    id_list = []
    admin_list = []
    target_list = []

    while True:
        file_logs = f"../assets/server/logs/{datetime.today().year}_{datetime.today().month}_{datetime.today().day}.log"
        if not os.path.exists(file_logs):
            with open(file_logs, "a+") as file:
                file.close()

        current_last_edit = os.path.getmtime(file_logs)
        if last_edit != current_last_edit:
            towrite = []
            with open(file_logs, "r+") as file:
                if len(file.readlines()) != 0:
                    print(file.readlines()[len(file.readlines())-1])
                line = 0
                for line in file.readlines():
                    line += 1
                    try:
                        time, guild, cmd, user, admin, target = line.replace("@Command ", "").replace("@Time ", "").replace("@Guild ", "").replace("@User ", "").replace("@Administrator ", "").replace("@Target ", "").split("|")
                    except:
                        time, guild,  cmd, user, admin = line.replace("@Command ", "").replace("@Time ", "").replace("@Guild ", "").replace("@User ", "").replace("@Administrator ", "").split("|")
                        target = None
                    exist = False
                    for i in time_list:
                        if i == time:
                            exist = True

                    if not exist:
                        time_list.append(str(time))
                        guild_list.append(str(guild))
                        cmd_list.append(str(cmd))
                        id_list.append(str(user))
                        admin_list.append(str(admin))
                        target_list.append(str(target))

                    if not Ban(guild).check(user) or admin == "True":
                        towrite.append(line)

                    if line != 1:
                        if time_list[line] == time_list[line+1] and id_list[line] == id_list[line+1] and guild_list[line] == guild_list[line+1]:
                            if time_list[line] == time_list[line+2] and id_list[line] == id_list[line+2] and guild_list[line] == guild_list[line+2]:
                                add_warn(f"assets/server/{guild_list[line]}/user/{id_list[line]}.json")
                                if target_list[line] == target_list[line+1] and target_list != None:
                                    add_warn(f"assets/server/{guild_list[line]}/user/{target_list[line]}.json")

            with open(file_logs, "w+") as file:
                file.writelines(towrite)
            last_edit = os.path.getmtime(file_logs)

if __name__ == "__main__":
    main()