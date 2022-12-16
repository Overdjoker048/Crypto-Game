from discord.commands import slash_command, option
import discord
import random
import time
from package import addon
from package.user import User
from package.crypto import Crypto
from package.ban_security import Ban
from discord.ext import commands

def main():
    client = commands.Bot(command_prefix="$", help_command=None, intents=discord.Intents.all())

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(name="[Version: Beta 1.0]"))

    def ban_embed(member: discord.Member, guild: discord.Guild):
        ban_msg = discord.Embed(title="Erreur", description=f"Tu ne peux pas utiliser de commande car\ntu es banni de Crypto Game sur {guild}.", color=discord.Color.red())
        ban_msg.set_author(name=member, icon_url=member.avatar)
        return ban_msg

    @staticmethod
    def crypto_shop(client: discord.AutocompleteContext):
        return ["Bitcoin", "Ethereum", "Pi"]

    @staticmethod
    def give_crypto(client: discord.AutocompleteContext):
        return ["Ethereum", "Pi"]

    @slash_command(description="Affiche l'argent du joueur selectionner.")
    async def balance(ctx, member: discord.Member = None):
        if not Ban(ctx.guild.id).check(ctx.author.id):
            crypto = Crypto(ctx.guild.id)
            if member == None:
                addon.logs("balance", ctx.author, ctx.guild.id)
                member = ctx.author
            else:
                addon.logs("balance", ctx.author, ctx.guild.id, member.id)
            if member.bot == False:
                owner = User(member, ctx.guild.id)
                embed = discord.Embed(title=f":moneybag:Balance:", description=f"{owner.money}$\n{owner.ethereum} Ethereum(s) [{crypto.ethereum * owner.ethereum}$]\n{owner.bitcoin} Bitcoin(s) [{crypto.bitcoin * owner.bitcoin}$]\n{owner.pi} Pi(s) [{crypto.pi * owner.pi}]", color=discord.Color.orange())
                embed.set_author(name=member, icon_url=member.avatar)
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title=f"Erreur", description=f"Un bot ne possède pas d'argent ni de crypto-monnaie.", color=discord.Color.red())
                await ctx.respond(embed=embed)
        else:
            await ctx.respond(embed=ban_embed(ctx.author, ctx.guild))

    @slash_command(description="Affiche la valeur de chaque crypto-monnaie.")
    async def value(ctx):
        if not Ban(ctx.guild.id).check(ctx.author.id):
            addon.logs("value", ctx.author, ctx.guild.id)
            embed = discord.Embed(title=f"Crypto-monnaie pix:", description=f"Ethereum: {Crypto(ctx.guild.id).ethereum}$.\nBitcoin: {Crypto(ctx.guild.id).bitcoin}$.\nPi: {Crypto(ctx.guild.id).pi}$.", color=discord.Color.orange())
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(embed=ban_embed(ctx.author, ctx.guild))

    @slash_command(description="Permet de donner de l'Ethereum à un utilisateur.")
    @option(name="crypto", autocomplete=give_crypto)
    async def give(ctx, member: discord.Member, crypto, quantite: float):
        if not Ban(ctx.guild.id).check(ctx.author.id):
            addon.logs("give", ctx.author, ctx.guild.id, member.id)
            if member.id != ctx.author.id:
                if member.bot == False:
                    nmb, decimal = str(quantite).split(".")
                    char = 0
                    for i in decimal:
                        char += 1
                    if char <= 3:
                        owner1 = User(ctx.author, ctx.guild.id)
                        owner2 = User(member, ctx.guild.id)
                        if crypto == "Ethereum":
                            var = [owner1.ethereum, owner2.ethereum, "Ethereum(s)"]
                        elif crypto == "Pi":
                            var = [owner1.pi, owner2.pi, "Pi(s)"]
                        if var[0] >= quantite:
                            var[0] -= quantite
                            give_crypto = quantite * (random.randint(95, 110)/100)
                            var[1] += give_crypto
                            if crypto == "Ethereum":
                                owner1.save(ethereum=var[0])
                                owner2.save(ethereum=var[1])
                            elif crypto == "Pi":
                                owner1.save(pi=var[0])
                                owner2.save(pi=var[1])
                            embed = discord.Embed(title="Transfert d'argent", description=f"Le transfert a bien été réalisé.\n{member} possède maintenant {var[1]} {var[2]}.", color=discord.Color.green())
                            embed.set_author(name=member, icon_url=member.avatar)
                            await ctx.respond(embed=embed)
                        else:
                            embed = discord.Embed(title="Erreur", description=f"Le transfert n'a pas pu se faire\ncar il te manque {quantite-var[1]}{var[2]}.", color=discord.Color.red())
                            await ctx.respond(embed=embed)
                    else:
                        embed = discord.Embed(title="Erreur", description=f"Vous pouvez donner que jusqu'à 3 chiffres après la virgule.", color=discord.Color.red())
                        await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(title="Erreur", description=f"Tu ne peux pas donner de crypto-monnaie à un bot.", color=discord.Color.red())
                    await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="Erreur", description=f"Tu ne peux pas te donner de crypto-monnaie.", color=discord.Color.red())
                await ctx.respond(embed=embed)
        else:
            await ctx.respond(embed=ban_embed(ctx.author, ctx.guild))

    @slash_command(description="Mine de la crypto-monnaie.")
    async def mining(ctx):
        if not Ban(ctx.guild.id).check(ctx.author.id):
            addon.logs("mining", ctx.author, ctx.guild.id)
            owner = User(ctx.author, ctx.guild.id)
            if not owner.mining == True:
                owner.mining_run()
                owner.save()
                embed = discord.Embed(title="Validation", description=f"Ta séance de minage vient de commencer.\nUtilise la commande /recup dans 1h pour récuperer\nla crypto-monnaie qui a été miné.", color=discord.Color.green())
            else:
                embed = discord.Embed(title="Erreur", description=f"Tu as déja une séance de minage en cours.", color=discord.Color.red())
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(embed=ban_embed(ctx.author, ctx.guild))

    @slash_command(description="Récupère la crypto-monnaie récupéré en minant.")
    async def recup(ctx):
        if not Ban(ctx.guild.id).check(ctx.author.id):
            addon.logs("recup", ctx.author, ctx.guild.id)
            owner = User(ctx.author, ctx.guild.id)
            if owner.mining == True:
                if owner.sec <= int(time.time()):
                    owner.sec = None
                    owner.mining = False
                    drop_ethereum = random.randint(1000, 5000)/1000
                    drop_bitcoin = random.randint(1, 1000)/1000
                    drop_pi = random.randint(100, 5000) / 1000
                    owner.ethereum += drop_ethereum
                    owner.bitcoin += drop_bitcoin
                    owner.pi += drop_pi
                    owner.save()
                    embed = discord.Embed(title="Séance de minage:", color=discord.Color.green())
                    embed.add_field(name="Ethereum", value=drop_ethereum, inline=True)
                    embed.add_field(name="Bitcoin", value=drop_bitcoin)
                    embed.add_field(name="Pi", value=drop_pi)
                else:
                    min = int((owner.sec - int(time.time()))/60)
                    sec = int(owner.sec - int(time.time()) - min * 60)
                    embed = discord.Embed(title="Erreur", description=f"Ta séance de minage n'est pas encore terminer.\nElle se termine dans {min}min {sec}sec", color=discord.Color.red())
            else:
                embed = discord.Embed(title="Erreur", description=f"Tu n'as pas de séance de minage en cours.\nFais /mining pour lancer une séance de minage.", color=discord.Color.red())
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(embed=ban_embed(ctx.author, ctx.guild))

    @slash_command(description="Vend de la crypto-monnaie.")
    @option(name="crypto", autocomplete=crypto_shop)
    async def sell(ctx, crypto, quantite: float):
        if not Ban(ctx.guild.id).check(ctx.author.id):
            nmb, decimal = str(quantite).split(".")
            char = 0
            for i in decimal:
                char += 1
            if char <= 3:
                addon.logs("sell", ctx.author, ctx.guild.id)
                owner = User(ctx.author, ctx.guild.id)
                crypto_value = Crypto(ctx.guild.id)
                if crypto == "Ethereum":
                    var = [owner.ethereum, crypto_value.ethereum, "Ethereum(s)", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Ethereum_logo_2014.svg/1257px-Ethereum_logo_2014.svg.png"]
                elif crypto == "Pi":
                    var = [owner.pi, crypto_value.pi, "Pi(s)", "https://seeklogo.com/images/P/pi-network-lvquy-logo-D798E8CD2E-seeklogo.com.png"]
                elif crypto == "Bitcoin":
                    var = [owner.bitcoin, crypto_value.bitcoin, "Bitcoin(s)", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/1024px-Bitcoin.svg.png"]
                if var[0] >= quantite:
                    for i in range(quantite):
                        owner.money + var[1]
                        var[1] = round(var[1]*0.999)
                    var[0] -= quantite
                    if crypto == "Bitcoin":
                        owner.save(bitcoin=var[0])
                        crypto_value.save(bitcoin=var[1])
                    elif crypto == "Ethereum":
                        owner.save(ethereum=var[0])
                        crypto_value.save(ethereum=var[1])
                    elif crypto == "Pi":
                        owner.save(pi=var[0])
                        crypto_value.save(pi=var[1])
                    embed = discord.Embed(title="Vente effectuer:", description=f"Il vous reste {var[0]} {var[2]} [{var[1] * var[0]}$].", color=discord.Color.green())
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    embed.set_thumbnail(url=var[3])
                    embed.add_field(name=f"{crypto}:", value=var[1], inline=True)
                    await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(title="Erreur", description=f"Vous ne possédez pas assez de bitcoins.\nIl vous manque {quantite - owner.bitcoin} Bitcoin(s).", color=discord.Color.red())
                    await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="Erreur", description=f"Vous pouvez vendre que jusqu'à 3 chiffres après la virgule.", color=discord.Color.red())
                await ctx.respond(embed=embed)
        else:
            await ctx.respond(embed=ban_embed(ctx.author, ctx.guild))

    @slash_command(description="Achete de la crypto-monnaie.")
    @option(name="crypto", autocomplete=crypto_shop)
    async def buy(ctx, crypto, quantite: float):
        if not Ban(ctx.guild.id).check(ctx.author.id):
            nmb, decimal = str(quantite).split(".")
            char = 0
            for i in decimal:
                char += 1
            if char <= 3:
                addon.logs("buy", ctx.author, ctx.guild.id)
                owner = User(ctx.author, ctx.guild.id)
                crypto_value = Crypto(ctx.guild.id)
                if crypto == "Bitcoin":
                    var = [owner.bitcoin, crypto_value.bitcoin, "Bitcoin(s)", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/1024px-Bitcoin.svg.png"]
                elif crypto == "Ethereum":
                    var = [owner.ethereum, crypto_value.ethereum, "Ethereum(s)", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Ethereum_logo_2014.svg/1257px-Ethereum_logo_2014.svg.png"]
                elif crypto == "Pi":
                    var = [owner.pi, crypto_value.pi, "Pi(s)", "https://seeklogo.com/images/P/pi-network-lvquy-logo-D798E8CD2E-seeklogo.com.png"]
                if owner.money >= var[1] * quantite:
                    for i in range(quantite):
                        owner.money += var[1]
                        var[1] = round(var[1] * 1.001)
                    var[0] += quantite
                    if crypto == "Bitcoin":
                        owner.save(bitcoin=var[0])
                        crypto_value.save(bitcoin=var[1])
                    elif crypto == "Ethereum":
                        owner.save(ethereum=var[0])
                        crypto_value.save(ethereum=var[1])
                    elif crypto == "Pi":
                        owner.save(pi=var[0])
                        crypto_value.save(pi=var[1])
                    embed = discord.Embed(title="Achat effectuer:", description=f"Il vous reste {owner.money}$\nvous possédez maintenant {var[0]} {var[2]}[{var[0]*var[1]}].", color=discord.Color.green())
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                    embed.set_thumbnail(url=var[3])
                    embed.add_field(name=f"{crypto}:", value=f"{var[1]}$", inline=True)
                    await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(title="Erreur", description=f"Vous ne possédez pas assez d'argent.\nIl vous manque {quantite*var[1]-owner.money}$.", color=discord.Color.red())
                    await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="Erreur", description=f"Vous pouvez acheter que jusqu'à 3 chiffres après la virgule.", color=discord.Color.red())
                await ctx.respond(embed=embed)
        else:
            await ctx.respond(embed=ban_embed(ctx.author, ctx.guild))

    client.run("OTkwOTg1NDYyMzU5NDAwNDY4.GNg1Q5.ZMX8ySUH6vEJPXdVOtJdkgMHG-5c5XNI9R91-A")

if __name__ == "__main__":
    main()