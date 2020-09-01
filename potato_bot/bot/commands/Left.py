import logging

from potato_bot.bot.models.Command import Command
from discord import Message, VoiceChannel, VoiceClient
from aiohttp import ClientSession

logger = logging.getLogger(__name__)


class Left(Command):
    """
        Remove the bot from current voice channel if he is connected in
    """

    @staticmethod
    def info():
        return {
            "name": "left",
            "description": "Remove the bot from current voice channel if he is connected in",
        }

    async def run(
        self, session: ClientSession, message: Message, params: list, bot,
    ) -> dict:
        try:
            voice_channel: VoiceChannel = message.author.voice.channel

            for vc in bot.voice_clients:
                same_voice_channel: bool = voice_channel.name == vc.channel.name

                if same_voice_channel:
                    if vc.is_playing():
                        vc.stop()

                    await vc.disconnect()

            return {"success": True}
        except Exception as e:
            logger.error("An error has occurred when lefting channel: {e}")
            return {"success": False}
