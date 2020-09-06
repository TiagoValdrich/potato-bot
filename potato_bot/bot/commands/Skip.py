import logging

from potato_bot.bot.models.Command import Command
from potato_bot.bot.models.PlaylistCli import PlaylistCli
from potato_bot.bot.commands.Play import Play
from discord import Message, VoiceChannel, TextChannel, VoiceClient
from aiohttp import ClientSession
from typing import List
from pytube import YouTube

logger = logging.getLogger(__name__)


class Skip(Command):
    """
        Skip the current music that is playing
    """

    def __init__(self):
        self.playlist_cli = PlaylistCli()

    @staticmethod
    def info():
        return {
            "name": "skip",
            "description": "Skip the current music that is playing",
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
                        play = await Play().build(message, bot)
                        play.download_and_play()

            return {"success": True}
        except Exception as e:
            logger.error(f"An error has occurred to skip music: {e}")
            return {"success": False}
