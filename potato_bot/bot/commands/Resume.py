import logging

from potato_bot.bot.models.Command import Command
from potato_bot.bot.models.PlaylistCli import PlaylistCli
from potato_bot.bot.commands.Play import Play
from discord import Message, VoiceChannel, TextChannel, VoiceClient
from aiohttp import ClientSession
from typing import List
from pytube import YouTube

logger = logging.getLogger(__name__)


class Resume(Command):
    """
        Resume the queue
    """

    def __init__(self):
        self.playlist_cli = PlaylistCli()

    @staticmethod
    def info():
        return {
            "name": "resume",
            "description": "Resume the queue",
        }

    async def run(
        self, session: ClientSession, message: Message, params: list, bot,
    ) -> dict:
        try:
            voice_channel: VoiceChannel = message.author.voice.channel
            voice_client: VoiceClient = None
            channel: TextChannel = message.channel

            for vc in bot.voice_clients:
                same_voice_channel: bool = voice_channel.name == vc.channel.name

                if same_voice_channel:
                    voice_client = vc
                    break

            if not voice_client:
                voice_client = await voice_channel.connect()

            if not voice_client.is_playing():
                play = await Play().build(message, bot)
                play.download_and_play()
            else:
                await channel.send(
                    "You can't resume the bot while it's already playing a song 😎"
                )

            return {"success": True}
        except Exception as e:
            logger.error(f"An error has occurred to skip music: {e}")
            return {"success": False}
