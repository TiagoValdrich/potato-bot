import discord, logging

logger = logging.getLogger(__name__)


class PotatoBot(discord.Client):

    BOT_PREFIX = "!"

    async def on_ready(self):
        logger.info("Potato bot is running!")

    async def on_message(self, message: discord.Message):
        if message.content[0] == self.BOT_PREFIX:
            logging.info(f"Message: {message.content}")
