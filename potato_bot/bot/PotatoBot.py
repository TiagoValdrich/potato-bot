import logging
from discord import Client, Message, Status, PartialEmoji, Game
from pytube import YouTube
from potato_bot.bot.models.MessageHandler import MessageHandler
from aiohttp import ClientSession


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PotatoBot(Client):

    session: ClientSession = None

    async def on_ready(self):
        game = Game("type !help for some info")
        self.session = ClientSession()
        await self.change_presence(status=Status.idle, activity=game)
        logger.info("☠ Initializing threads! ☠")
        logger.info("🍠 Potato bot is running! 🍠")

    async def on_message(self, message: Message):
        await MessageHandler(self, message, self.session).handle()

    async def on_disconnect(self):
        logger.info("Closing session connection!")
        await self.session.close()

