import discord
from package import addon
from discord.commands import slash_command
from discord.ext import commands
from datetime import datetime
from package.ban_security import Ban
from package.user import User

def main():
    client = commands.Bot(command_prefix="$", help_command=None, intents=discord.Intents.all())

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(name="[Version: Beta 1.0]"))

    def admin_embed():
        return discord.Embed(title="Erreur", description="Vous ne pouvez pas utilisez cette commande\ncar vous n'êtes pas administrateur.", color=discord.Color.red())

    @slash_command(description="Affiche le ping du bot.")
    async def ping(ctx):
        if ctx.author.guild_permissions.administrator:
            addon.logs("ping", ctx.author, ctx.guild.id)
            ping_start = datetime.now()
            latency = client.bot.latency * 1000
            await ctx.send("Pong", delete_after=0.1)

            latency_ms = f"**{str(round(latency, 0))[:-2]}** ms"
            ping_end = (datetime.now() - ping_start).microseconds / 1000
            bot_ping = f"**{round(ping_end)}** ms"

            ping_emb = discord.Embed(title="Bot latency", color=discord.Color.orange())
            ping_emb.add_field(name=":satellite: Discord API", value=latency_ms, inline=True)
            ping_emb.add_field(name=":robot: BOT", value=bot_ping)
            await ctx.respond(embed=ping_emb)
        else:
            await ctx.respond(embed=admin_embed())

    @slash_command(description="Réinitialise le compte d'un utilisateur")
    async def reset(ctx, member: discord.Member):
        if ctx.author.guild_permissions.administrator:
            if member.bot == False:
                addon.logs("reset", ctx.author, ctx.guild.id, member.id)
                owner = User(member, ctx.guild.id)
                owner.money = 10000
                owner.ethereum = 0
                owner.bitcoin = 0
                owner.pi = 0
                owner.save()
                embed = discord.Embed(title=f"Validation:", description=f"Le joueur {member} a bien été réinitialisé.", color=discord.Color.red())
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="Erreur:", description="Tu ne peux pas bannir de bot discord.", color=discord.Color.red())
                await ctx.respond(embed)
        else:
            await ctx.respond(embed=admin_embed())

    @slash_command(description="Affiche la liste de toutes les commandes.")
    async def help(ctx):
        if not Ban(ctx.guild.id).check(ctx.user.id) or ctx.author.guild_permissions.administrator:
            addon.logs("help", ctx.author, ctx.guild.id)
            embed = discord.Embed(title='Liste des commandes:', description='''
            /help    Vous informe sur toutes les commandes de Crypto Game.
            /sell    Permet de vendre du bitcoin ou de l'ethereum.
            /buy     Permet d'acheter ou de vendre du bitcoin ou de l'ethereum.
            /balance Permet d'afficher votre argent.
            /value   Permet d'afficher la valeur des crypto-monnaies.
            /mining  Permet de lancer une séance de minage.
            /recup   Permet de récuperer les crypto-monnaie à la fin de la séance de minage.
            /give    Permet de donner de l'Ethereums à une personne.
            ''', color=discord.Color.orange())
            await ctx.respond(embed=embed)
            if ctx.author.guild_permissions.administrator:
                embed = discord.Embed(title='Commandes Administrateur:', description='''
                        /start     Permet de lancer le jeu.
                        /ping      Affiche le temps de lattence entre l'API discord et le bot.
                        /reset     Réinitialise l'argent de la personne en question.
                        /ban       Permet de bloquer l'acces d'un memebre de ton serveur a Crypto Game.
                        /unban     Permet de restaurer l'acces d'un utilisateur de votre serveur a Crypto Game.
                        /ban_list  Affiche la liste des identifient des membres banni sur ton serveur.
                        ''', color=discord.Color.orange())
                await ctx.respond(embed=embed)
        else:
            ban_msg = discord.Embed(title="Erreur", description=f"Tu ne peux pas utiliser de commande car\ntu es banni de Crypto Game sur {ctx.guild}.", color=discord.Color.red())
            ban_msg.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            await ctx.respond(embed=ban_msg)

    @slash_command(descriptioon="Bloque l'accès à un utilisateur de votre serveur de Crypto Game.")
    async def ban(ctx, user: discord.Member):
        if ctx.author.guild_permissions.administrator:
            if user.bot == False:
                addon.logs("ban", ctx.author, ctx.guild.id, user.id)
                Ban(ctx.guild.id).add(user.id)
                embed = discord.Embed(title="Validation:", description=f"{user} a bien été banni de Crypto Game sur votre serveur.", color=discord.Color.green())
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="Erreur:", description="Tu ne peux pas bannir de bot discord.", color=discord.Color.red())
                await ctx.respond(embed)
        else:
            await ctx.respond(embed=admin_embed())

    @slash_command(descriptioon="Débloque l'accès à un utilisateur de votre serveur de Crypto Game.")
    async def unban(ctx, user: discord.Member):
        if ctx.author.guild_permissions.administrator:
            if Ban(ctx.guild.id).check(user.id):
                addon.logs("unban", ctx.author, ctx.guild.id, user.id)
                Ban(ctx.guild.id).remove(user.id)
                embed = discord.Embed(title="Validation:", description=f"{user} a bien été debanni de Crypto Game sur votre serveur.", color=discord.Color.green())
            else:
                addon.logs("unban", ctx.author, ctx.guild.id)
                embed = discord.Embed(title="Erreur:", description=f"{user} n'est pas banni de Crypto Game sur se serveur.", color=discord.Color.red())
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(embed=admin_embed())

    @slash_command(descriptioon="Affiche toutes les personnes banni de crypto game sur ce serveur.")
    async def ban_list(ctx):
        if ctx.author.guild_permissions.administrator:
            addon.logs("ban_list", ctx.author, ctx.guild.id)
            ban = Ban(ctx.guild.id)
            ban_list = ""
            for url in ban.list:
                ban_list = f"{ban_list}{url}\n"
            embed = discord.Embed(title="Liste des Bans:", description=f"{ban_list}", color=discord.Color.orange())
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(embed=admin_embed())

    client.run("Token")

if __name__ == "__main__":
    main()
