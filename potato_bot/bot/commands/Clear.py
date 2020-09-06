import logging

from potato_bot.bot.models.Command import Command
from potato_bot.bot.models.PlaylistCli import PlaylistCli
from potato_bot.bot.commands.Play import Play
from discord import Message, VoiceChannel, TextChannel, VoiceClient
from aiohttp import ClientSession
from typing import List
from pytube import YouTube

logger = logging.getLogger(__name__)


class Clear(Command):
    """
        Clear all the songs from queue
    """

    def __init__(self):
        self.playlist_cli = PlaylistCli()

    @staticmethod
    def info():
        return {
            "name": "clear",
            "description": "Clear all the songs from queue",
        }

    async def run(
        self, session: ClientSession, message: Message, params: list, bot,
    ) -> dict:
        try:
            channel: TextChannel = message.channel
            voice_channel: VoiceChannel = message.author.voice.channel

            if voice_channel:
                self.playlist_cli.delete_playlist(voice_channel.id)
                await channel.send("Playlist cleared! ✅")

            return {"success": True}
        except Exception as e:
            logger.error(f"An error has occurred to skip music: {e}")
            return {"success": False}
