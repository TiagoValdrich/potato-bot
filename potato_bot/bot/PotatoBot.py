import discord, logging

from potato_bot.bot.commands.HeadsOrTails import HeadsOrTails

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PotatoBot(discord.Client):

    BOT_PREFIX = "!"

    async def on_ready(self):
        logger.info("Potato bot is running!")

    async def on_message(self, message: discord.Message):
        logging.info(f"Message: {message.content}")

        if (
            self.user.id != message.author.id
            and type(message.content) is str
            and len(message.content) > 0
            and message.content[0] == self.BOT_PREFIX
        ):
            if message.content == "!headsortails":
                game = HeadsOrTails(message)
                await game.play()
