import discord
import asyncio
from pathlib import Path
from discord.ext import commands


class Voc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="attendre",
        description="fait patientez les gens",
        visible=True
    )
    async def patientez(self, ctx, personne: discord.Member):
        if ctx.author.guild_permissions.administrator is False:
            await ctx.send(
                "Vous n'avez pas la permission d'utiliser cette commande."
            )
            return
        if personne == ctx.author:
            await ctx.send(
                "Vous ne pouvez pas vous faire patienter vous-même."
            )
            return
        if personne.bot:
            await ctx.send("Vous ne pouvez pas faire patienter un bot.")
            return
        if personne.voice is None or personne.voice.channel is None:
            await ctx.send(
                f"{personne.mention} n'est pas dans un canal vocal."
            )
            return
        channel = personne.voice.channel
        voice_client = ctx.guild.voice_client

        if voice_client is None:
            voice_client = await channel.connect()
        elif voice_client.channel != channel:
            await voice_client.move_to(channel)

        if voice_client.is_playing():
            voice_client.stop()

        audio_path = Path(__file__).parent.parent / "audio" / "patientez.mp3"
        if not audio_path.is_file():
            await ctx.send(f"Fichier audio introuvable : {audio_path}")
            return

        def on_audio_error(error):
            if error:
                print(f"Erreur audio : {error}")

        while personne.voice is not None and personne.voice.channel == channel:
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(str(audio_path))
            )
            print(f"Lecture du fichier audio : {audio_path}")
            voice_client.play(source, after=on_audio_error)

            while voice_client.is_playing():
                await asyncio.sleep(0.5)

            await asyncio.sleep(10)

        if voice_client.is_playing():
            voice_client.stop()
        await voice_client.disconnect()

    @patientez.error
    async def patientez_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(
                "Membre introuvable. Utilisez une mention, par exemple "
                "`$attendre @mon_double_compte`."
            )
            return
        raise error

    @commands.hybrid_command(
        name="stop_attendre",
        description="Arrête de faire patienter les gens",
        visible=True,
        guild_permissions=discord.Permissions(administrator=True)
    )
    async def stop_attendre(self, ctx):
        if ctx.author.guild_permissions.administrator is False:
            await ctx.send(
                "Vous n'avez pas la permission d'utiliser cette commande."
            )
            return
        voice_client = ctx.guild.voice_client
        if voice_client is None:
            await ctx.send("Le bot n'est pas connecté à un canal vocal.")
            return
        if voice_client.is_playing():
            voice_client.stop()
        await voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Voc(bot))
