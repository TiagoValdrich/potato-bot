import logging

from potato_bot.bot.models.Command import Command
from potato_bot.bot.models.PlaylistCli import PlaylistCli
from discord import Message, VoiceChannel, Embed, TextChannel
from aiohttp import ClientSession
from typing import List
from pytube import YouTube
from multiprocessing import Pool

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

    @staticmethod
    def fetch_video_title(url):
        yt = YouTube(url)
        return yt.title

    async def build_queue_embed(self, musics: List[str], remaining: int) -> Embed:
        embed = Embed(title="Next 10 musics on queue:", color=0x4287F5)

        with Pool(5) as p:
            results = p.map(Queue.fetch_video_title, musics)

            for num, music_title in enumerate(results, 1):
                if music_title:
                    name = f"#{num}"
                    embed.add_field(name=name, value=music_title, inline=False)

            if remaining:
                embed.set_footer(text=f"Total remaining on queue: {remaining}")

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
                    real_music_list = musics[:10]
                    embed = await self.build_queue_embed(real_music_list, len(musics))
                    await channel.send(embed=embed)
                else:
                    await channel.send("There is no musics on queue!")

            return {"success": True}
        except Exception as e:
            logger.error(f"An error has occurred when showing channel queue: {e}")
            return {"success": False}
