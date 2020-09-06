import logging

from potato_bot.bot.models.Command import Command
from potato_bot.bot.models.PlaylistCli import PlaylistCli
from discord import Message, VoiceChannel, Embed, TextChannel
from aiohttp import ClientSession
from typing import List
from pytube import YouTube

logger = logging.getLogger(__name__)


class Queue(Command):
    """
        Show the musics that are queued on the channel
    """

    def __init__(self):
        self.playlist_cli = PlaylistCli()

    @staticmethod
    def info():
        return {
            "name": "queue",
            "description": "Show musics in queue to play",
        }

    async def build_queue_embed(self, musics: List[str]) -> Embed:
        embed = Embed(title="Musics on queue:", color=0x4287F5)

        for num, music in enumerate(musics, 1):
            if music:
                yt = YouTube(music)
                name = f"#{num}"
                embed.add_field(name=name, value=yt.title, inline=False)

        return embed

    async def run(
        self, session: ClientSession, message: Message, params: list, bot,
    ) -> dict:
        try:
            channel: TextChannel = message.channel
            voice_channel: VoiceChannel = message.author.voice.channel

            if voice_channel:
                musics = self.playlist_cli.get_musics(voice_channel.id)

                if musics:
                    embed = await self.build_queue_embed(musics)
                    await channel.send(embed=embed)
                else:
                    await channel.send("There is no musics on queue!")

            return {"success": True}
        except Exception as e:
            logger.error(f"An error has occurred when showing channel queue: {e}")
            return {"success": False}
