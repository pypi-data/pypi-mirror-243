import discord
from discord.ext import commands

class LimecordBot:
    def __init__(self, intents, cmdPrefix):
        self.intents = intents
        self.cmdPrefix = cmdPrefix

        bot = commands.Bot(command_prefix=self.cmdPrefix, intents=self.intents)
        self.bot = bot
    
    def getBot(self):
        return self.bot

    def registerCommand(self, name: str, command: function):
        @self.bot.command(name=name)
        async def _command(ctx):
            command()
