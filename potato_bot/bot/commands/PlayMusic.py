import logging, re, threading, asyncio
from potato_bot.bot.models.Command import Command
from potato_bot.bot.models.YoutubeSearch import YoutubeSearch
from discord import Message, VoiceChannel, VoiceClient, Embed, FFmpegPCMAudio
from aiohttp import ClientSession
from pytube import YouTube
from functools import partial

logger = logging.getLogger(__name__)


class PlayMusic(Command):
    @staticmethod
    def info():
        return {
            "name": "play",
            "description": "Play Youtube songs on your current voice channel.\n Type `!play <youtube_url>` and have fun!",
        }

    def build_musics_embed(self, musics: list):
        embed = Embed(title="Select a music from list below", color=0x4287F5)

        for num, music in enumerate(musics):
            name = "#" + str((num + 1))
            title = music["title"]
            embed.add_field(name=name, value=title, inline=False)

        return embed

    def download_and_play(self, info):
        queue = info["queue"]

        if len(queue["musics"]) > 0:
            yt = YouTube(queue["musics"].pop(0))
            yt.streams.first().download(
                output_path="resources/music/",
                filename=info["filename"],
                skip_existing=False,
            )

            info["voice_client"].play(
                FFmpegPCMAudio(f"resources/music/{info['filename']}.mp4"),
            )

    async def run(
        self, session: ClientSession, message: Message, params: list, bot,
    ) -> dict:
        try:
            if params:
                voice_channel: VoiceChannel = message.author.voice.channel

                # If is to filter only for youtube.com: .+(youtube.com\/watch\?v=)
                if re.match("^(https:\/\/)", params[0]):
                    voice_client: VoiceClient = None
                    voice_channel_id = str(voice_channel.id)

                    if bot.voice_clients:
                        for vc in bot.voice_clients:
                            same_voice_channel: bool = voice_channel.name == vc.channel.name
                            same_guild: bool = voice_channel.guild.id == vc.guild.id

                            if same_voice_channel and same_guild:
                                voice_client = vc
                                break

                            if not same_voice_channel and same_guild:
                                await vc.disconnect()
                                voice_client = await voice_channel.connect()
                                break

                    if not voice_client:
                        voice_client = await voice_channel.connect()

                    if voice_client.is_connected():
                        if voice_client.is_playing():
                            if voice_channel_id in bot.queues.keys():
                                bot.queues[voice_channel_id]["musics"].append(params[0])
                        else:
                            bot.queues[voice_channel_id] = {"musics": [params[0]]}

                    bot.loop.run_in_executor(
                        None,
                        self.download_and_play,
                        {
                            "filename": voice_channel_id,
                            "voice_client": voice_client,
                            "queue": bot.queues[voice_channel_id],
                        },
                    )

                else:
                    music = " ".join(params)
                    results = await YoutubeSearch.search(session, music)
                    embed = self.build_musics_embed(results)
                    await message.channel.send(embed=embed)
                    await message.channel.send(
                        "Nem adianta enviar o numero da musica, isso ainda nao ta pronto 😿"
                    )

            else:
                await message.channel.send(
                    "❌ You need to specify a music name or a youtube URL ❌"
                )

            return {"success": True}
        except Exception as e:
            logger.error(f"An error has occurred to play music: {e}")
            return {"success": False}
