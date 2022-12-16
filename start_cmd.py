import discord
import random
import os
import json
import time
from package import addon
from discord.commands import slash_command
from discord.ext import commands
from datetime import datetime
from package.crypto import Crypto

def main():
    client = commands.Bot(command_prefix="$", help_command=None, intents=discord.Intents.all())

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(name="[Version: Beta 1.0]"))

    @slash_command(description="Lance le jeux sur le serveur où la commande est executer.")
    @commands.has_permissions(administrator=True)
    async def start(ctx):
        addon.logs("start", ctx.author, ctx.guild.id)
        embed = discord.Embed(title="Validation", description="Le jeu viens de se lancer", color=discord.Color.green())
        await ctx.respond(embed=embed)
        value_channel = discord.utils.get(ctx.guild.text_channels, name='crypto-monnaie-prix')
        category = discord.utils.get(ctx.guild.categories, name='Crypto Game')
        if not category:
            category = await ctx.guild.create_category("Crypto Game")
        if not value_channel:
            value_channel = await ctx.guild.create_text_channel("crypto-monnaie-prix", category=category)
            await value_channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await value_channel.set_permissions(ctx.guild.default_role, add_reactions=False)
        crypto = Crypto(ctx.guild.id)
        embed = discord.Embed(title=f"Crypto-monnaie prix:", description=f"Ethereum: {crypto.ethereum}$\nBitcoin: {crypto.bitcoin}$", color=discord.Color.orange())
        embed.add_field(name='Temps:', value=f"{datetime.today().day}/{datetime.today().month}/{datetime.today().year} | {datetime.today().hour}h {datetime.today().minute}min {datetime.today().second}sec", inline=True)
        await ctx.respond(embed=embed)

        ethereum_time = int(time.time()) + random.randint(60, 600)
        bitcoin_time = int(time.time()) + random.randint(60, 900)
        pi_time = int(time.time()) + random.randint(60, 300)
        while True:
            if time == ethereum_time:
                ethereum_time = int(time.time()) + random.randint(60, 900)
                crypto = Crypto(ctx.guild.id)

                after_ethereum = crypto.ethereum
                if crypto.ethereum == 1000:
                    crypto.ethereum = round(crypto.ethereum * random.randint(75, 125) / 100)
                elif crypto.ethereum > 1000:
                    crypto.ethereum = round(crypto.ethereum * random.randint(50, 125) / 100)
                elif crypto.ethereum < 1000:
                    crypto.ethereum = round(crypto.ethereum * random.randint(75, 150) / 100)
                crypto.save()
                ethereum_pourcentage = round(crypto.ethereum * 100 / after_ethereum)
                if ethereum_pourcentage > 100:
                    ethereum_pourcentage = str(f"+{ethereum_pourcentage - 100}")
                else:
                    ethereum_pourcentage = str(f"-{100 - ethereum_pourcentage}")
                embed = discord.Embed(title=f"Ethereum prix:", description=f"Ethereum: {crypto.ethereum}$ [{ethereum_pourcentage}%]", color=discord.Color.orange())
                embed.add_field(name='Temps:', value=f"{datetime.today().day}/{datetime.today().month}/{datetime.today().year} | {datetime.today().hour}h {datetime.today().minute}min {datetime.today().second}sec", inline=True)
                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Ethereum_logo_2014.svg/1257px-Ethereum_logo_2014.svg.png")
                await value_channel.send(embed=embed)

            if time == pi_time:
                pi_time = int(time.time()) + random.randint(60, 300)
                crypto = Crypto(ctx.guild.id)
                after_pi = crypto.pi
                crypto.pi = round(crypto.pi * random.randint(90, 99) / 100)
                crypto.save()
                pi_pourcentage = round(crypto.pi * 100 / after_pi)
                if pi_pourcentage > 100:
                    pi_pourcentage = str(f"+{pi_pourcentage - 100}")
                else:
                    pi_pourcentage = str(f"-{100 - pi_pourcentage}")
                embed = discord.Embed(title=f"Pi prix:", description=f"Pi: {crypto.pi}$ [{pi_pourcentage}%]", color=discord.Color.orange())
                embed.add_field(name='Temps:', value=f"{datetime.today().day}/{datetime.today().month}/{datetime.today().year} | {datetime.today().hour}h {datetime.today().minute}min {datetime.today().second}sec", inline=True)
                embed.set_thumbnail(url="https://seeklogo.com/images/P/pi-network-lvquy-logo-D798E8CD2E-seeklogo.com.png")
                await value_channel.send(embed=embed)

            if time == bitcoin_time:
                bitcoin_time = int(time.time()) + random.randint(60, 900)
                crypto = Crypto(ctx.guild.id)
                after_bitcoin = crypto.bitcoin
                if crypto.bitcoin == 10000:
                    crypto.bitcoin = round(crypto.bitcoin * random.randint(50, 150) / 100)
                elif crypto.bitcoin > 10000:
                    crypto.bitcoin = round(crypto.bitcoin * random.randint(25, 125) / 100)
                elif crypto.bitcoin < 10000:
                    crypto.bitcoin = round(crypto.bitcoin * random.randint(75, 175) / 100)
                crypto.save()
                bitcoin_pourcentage = round(crypto.bitcoin * 100 / after_bitcoin)
                if bitcoin_pourcentage > 100:
                    bitcoin_pourcentage = str(f"+{bitcoin_pourcentage - 100}")
                else:
                    bitcoin_pourcentage = str(f"-{100 - bitcoin_pourcentage}")

                embed = discord.Embed(title=f"Bitcoin prix:", description=f"Bitcoin: {crypto.bitcoin}$ [{bitcoin_pourcentage}%]", color=discord.Color.orange())
                embed.add_field(name='Temps:', value=f"{datetime.today().day}/{datetime.today().month}/{datetime.today().year} | {datetime.today().hour}h {datetime.today().minute}min {datetime.today().second}sec", inline=True)
                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/1024px-Bitcoin.svg.png")
                await value_channel.send(embed=embed)

            if datetime.today().hour == 23 and datetime.today().min == 59 and datetime.today().second == 59:

                value = {
                    "ethereum": 1000,
                    "bitcoin": 10000,
                    "pi": 5000,
                }
                with open(f"../assets/server/{ctx.guild.id}/crypto.json", "w+") as file:
                    json.dump(value, file, indent=2)

                for user in os.listdir(f"../assets/server/{ctx.guild.id}/user"):
                    with open(f"../assets/server/{ctx.guild.id}/user/{user}.json", "r+") as file:
                        contenue = json.load(fp=file)
                    info = {
                        "name": contenue['name'],
                        "ethereum": 0,
                        "bitcoin": 0,
                        "pi": 0,
                        "money": contenue['money'],
                        "sec": contenue['sec'],
                        "mining": contenue['mining'],
                    }
                    with open(f"../assets/server/{ctx.guild.id}/user/{user}.json", "w+") as file:
                        json.dump(info, file, indent=2)

    client.run("OTkwOTg1NDYyMzU5NDAwNDY4.GNg1Q5.ZMX8ySUH6vEJPXdVOtJdkgMHG-5c5XNI9R91-A")

if __name__ == "__main__":
    main()