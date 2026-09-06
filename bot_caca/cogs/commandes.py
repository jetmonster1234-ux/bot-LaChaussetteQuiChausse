import discord
import random
from discord import app_commands
from discord.ext import commands


class Commandes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        description="netiqwantapas",
        brief="Reponds avec pong quand tu marques $ping"
    )
    async def ping(self, ctx):
        await ctx.send('pong')

    @app_commands.command(name='random')
    async def random_command(
        self, interaction: discord.Interaction, maximum: int
    ):
        if maximum < 1:
            await interaction.response.send_message(
                "Le nombre maximum doit être supérieur à 0."
            )
            return

        number = random.randint(1, maximum)
        await interaction.response.send_message(
            f"Le nombre aléatoire est : {number}"
        )

    @app_commands.command(name='cherche_teamate')
    async def cherche_teamate(
        self, interaction: discord.Interaction, niveau: int
    ):
        await interaction.response.send_message(
            f"{interaction.user.mention} Recherche d'un teamate de niveau "
            "minimum : "
            f"{niveau}"
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            await member.send(f"Bienvenue dans l'équipage, {member.name} ! ")
        except discord.Forbidden:
            print(f"Impossible d'envoyer un message privé à {member.name}.")    

async def setup(bot):
    await bot.add_cog(
        Commandes(bot)
    )