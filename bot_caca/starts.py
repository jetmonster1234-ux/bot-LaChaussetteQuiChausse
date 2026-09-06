import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()
token = os.environ["DISCORD_TOKEN"]


class MyBot(commands.Bot):
    async def setup_hook(self):
        for extension in ["cogs.commandes", "cogs.voc"]:
            await self.load_extension(extension)
        synced_commands = await self.tree.sync()
        signatures = [
            f"{command.name}({', '.join(option.name for option in command.parameters)})"
            for command in synced_commands
        ]
        print(f"Commandes slash synchronisees: {', '.join(signatures)}")


intents = discord.Intents.all()
bot = MyBot(command_prefix="$", intents=intents)

keep_alive()
bot.run(token=token)
