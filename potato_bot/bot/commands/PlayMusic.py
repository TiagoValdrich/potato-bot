import logging, re
from potato_bot.bot.models.Command import Command
from potato_bot.bot.models.YoutubeSearch import YoutubeSearch
from potato_bot.bot.models.PlaylistCli import PlaylistCli
from discord import (
    Message,
    VoiceChannel,
    VoiceClient,
    TextChannel,
    Embed,
    FFmpegPCMAudio,
)
from aiohttp import ClientSession
from pytube import YouTube
from typing import List

logger = logging.getLogger(__name__)


class PlayMusic(Command):

    channel: TextChannel = None
    voice_channel: VoiceChannel = None
    voice_client: VoiceClient = None
    loop = None

    def __init__(self):
        self.playlist_cli = PlaylistCli()

    @staticmethod
    def info() -> dict:
        return {
            "name": "play",
            "description": "Play Youtube songs on your current voice channel.\n Type `>play <youtube_url>` and have fun!",
        }

    async def send_music_title(self, youtube: YouTube):
        await self.channel.send(f"Playing now `{youtube.title}`")

    def _download_and_play(self, error) -> None:
        musics = self.playlist_cli.get_musics(self.voice_channel.id)

        if musics and self.voice_client:
            yt = YouTube(self.playlist_cli.get_next_music(self.voice_channel.id))
            yt.streams.first().download(
                output_path="resources/music/",
                filename=str(self.voice_channel.id),
                skip_existing=False,
            )

            self.voice_client.play(
                FFmpegPCMAudio(f"resources/music/{self.voice_channel.id}.mp4"),
                after=self._download_and_play,
            )

            self.loop.create_task(self.send_music_title(yt))

    def build_musics_embed(self, musics: list) -> Embed:
        embed = Embed(title="Select a music from list below", color=0x4287F5)

        for num, music in enumerate(musics):
            name = "#" + str((num + 1))
            title = music["title"]
            embed.add_field(name=name, value=title, inline=False)

        return embed

    async def connect_voice(self, voice_clients: List[VoiceClient]) -> None:
        if voice_clients:
            for vc in voice_clients:
                same_voice_channel: bool = self.voice_channel.name == vc.channel.name
                same_guild: bool = self.voice_channel.guild.id == vc.guild.id

                if same_voice_channel and same_guild:
                    self.voice_client = vc
                    break

                if not same_voice_channel and same_guild:
                    await vc.disconnect()
                    self.voice_client = await voice_channel.connect()
                    break

        if not self.voice_client:
            self.voice_client = await self.voice_channel.connect()

    async def play(self, video_url: str, bot) -> None:
        await self.connect_voice(bot.voice_clients)

        if self.voice_client.is_connected():
            self.playlist_cli.add_music(self.voice_channel.id, video_url)

            if not self.voice_client.is_playing():
                bot.loop.run_in_executor(None, self._download_and_play, None)
            else:
                await self.channel.send(f"Music added to queue!")

    async def run(
        self, session: ClientSession, message: Message, params: List[str], bot,
    ) -> dict:
        try:
            self.loop = bot.loop

            if params:
                self.channel = message.channel
                self.voice_channel = message.author.voice.channel
                video_url = str(params[0])

                if re.match("^(https:\/\/)", video_url):
                    await self.play(video_url, bot)

                else:
                    music = " ".join(params).replace("--first-result", "")
                    results = await YoutubeSearch.search(session, music)

                    if "--first-result" in params:
                        music = results.pop(0)
                        await self.play(music["video_url"], bot)

                    else:
                        embed = self.build_musics_embed(results)
                        await self.channel.send(embed=embed)
                        await self.channel.send(
                            "Nem adianta enviar o numero da musica, isso ainda nao ta pronto 😿"
                        )

            else:
                await self.channel.send(
                    "❌ You need to specify a music name or a youtube URL ❌"
                )

            return {"success": True}
        except Exception as e:
            logger.error(f"An error has occurred to play music: {e}")
            return {"success": False}
