from datetime import datetime
import os
import time

def setup():
	os.system("python -m pip install -r requirements.txt")
	os.system("python -m pip install --upgrade pip")
	os.system("cls")
	os.system("start admin_cmd.py")
	os.system("start member_cmd.py")
	os.system("start start_cmd.py")
	if not os.path.exists("../assets"):
		os.mkdir("../assets")
	if not os.path.exists("../assets/server"):
		os.mkdir("../assets/server")
	pourcentage = 0
	print(f"Connection...")
	for i in range(100):
		pourcentage += 1
		anim = "█"
		for i in range(int(pourcentage / 5)):
			anim += "█"
		print(f"{pourcentage}% | {anim}", end="\r")
		time.sleep(0.025)
	print("""
  /$$$$$$                                  /$$                      /$$$$$$                                  
 /$$__  $$                                | $$                     /$$__  $$                                 
| $$  \__/  /$$$$$$  /$$   /$$  /$$$$$$  /$$$$$$    /$$$$$$       | $$  \__/ /$$$$$$  /$$$$$$/$$$$   /$$$$$$ 
| $$       /$$__  $$| $$  | $$ /$$__  $$|_  $$_/   /$$__  $$      | $$ /$$$$|____  $$| $$_  $$_  $$ /$$__  $$
| $$      | $$  \__/| $$  | $$| $$  \ $$  | $$    | $$  \ $$      | $$|_  $$ /$$$$$$$| $$ \ $$ \ $$| $$$$$$$$
| $$    $$| $$      | $$  | $$| $$  | $$  | $$ /$$| $$  | $$      | $$  \ $$/$$__  $$| $$ | $$ | $$| $$_____/
|  $$$$$$/| $$      |  $$$$$$$| $$$$$$$/  |  $$$$/|  $$$$$$/      |  $$$$$$/  $$$$$$$| $$ | $$ | $$|  $$$$$$$
 \______/ |__/       \____  $$| $$____/    \___/   \______/        \______/ \_______/|__/ |__/ |__/ \_______/
                     /$$  | $$| $$                                                                           
                    |  $$$$$$/| $$                                                                           
                     \______/ |__/                                                                           
""")

def logs(cmd, user, guild, target = None):
	if user.guild_permissions.administrator:
		administrator = True
	else:
		administrator = False
	file_logs = f"../assets/server/logs/{datetime.today().year}_{datetime.today().month}_{datetime.today().day}.log"
	if not os.path.exists("../assets/server/logs"):
		os.mkdir("../assets/server/logs")
	time = f"{datetime.today().year}:{datetime.today().month}:{datetime.today().day}:{datetime.today().hour}:{datetime.today().minute}:{datetime.today().second}"
	if target == None:
		text = f"@Time {time}|@Guild {guild}|@Command {cmd}|@User {user.id}|@Administrator {administrator}"
	else:
		text = f"@Time {time}|@Guild {guild}|@Command {cmd}|@User {user.id}|@Administrator {administrator}|@Target {target}"
	with open(file_logs, "a+") as file:
		file.write(f"{text}\n")

def ref_deci(nmb: float):
	entier, decimal = str(nmb).split(".")
	tour = 0
	new_decimale = ""
	for i in decimal:
		if tour == 3:
			new_decimale += "."
		new_decimale += str(i)
		tour += 1
	print(f"new_decimal:{new_decimale}")

	return float(f"{entier}.{str(round(float(new_decimale)))}")