import logging

from random import randrange
from discord import Message, TextChannel, File, Embed
from operator import mod
from potato_bot.bot.models.Command import Command
from aiohttp import ClientSession

logger = logging.getLogger(__name__)


class HeadsOrTails(Command):
    @staticmethod
    def info():
        return {
            "name": "headsortails",
            "description": "The class coin game Heads Or Tails, just drop the command an see if your are lucky today ;)",
        }

    def build_embed(self, title: str, color: int, filename: str):
        embed = Embed(title=title, color=color)
        img_file = File(f"resources/{filename}", filename=filename)
        embed.set_image(url=f"attachment://{filename}")

        return {"file": img_file, "embed": embed}

    async def run(
        self,
        session: ClientSession,
        message: Message,
        params: list,
        voice_clients: list,
    ) -> dict:
        try:
            channel = message.channel
            number = randrange(1, 1000)
            embed_data = None

            if mod(number, 2) == 0:
                embed_data = self.build_embed("Heads", 0x4287F5, "heads.png")
            else:
                embed_data = self.build_embed("Tails", 0x4287F5, "tails.png")

            await channel.send(file=embed_data["file"], embed=embed_data["embed"])

            return {"success": True}
        except Exception as e:
            logger.error(
                f"An error has occurred on Heads or Tails execution, details: {e}"
            )
            return {"success": False}

