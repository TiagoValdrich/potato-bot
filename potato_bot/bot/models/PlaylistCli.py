from redis import Redis
from os import getenv
from dotenv import load_dotenv


class PlaylistCli:
    def __init__(self):
        load_dotenv()
        self._conn = Redis(
            getenv("REDIS_HOST"),
            getenv("REDIS_PORT"),
            0,
            charset="utf-8",
            decode_responses=True,
        )

    def get_playlists(self):
        return self._conn.keys(pattern="*")

    def get_musics(self, voice_channel_id):
        return self._conn.lrange(voice_channel_id, 0, -1)

    def add_music(self, voice_channel_id, music_url: str):
        return self._conn.rpush(voice_channel_id, music_url)

    def get_next_music(self, voice_channel_id):
        return self._conn.lpop(voice_channel_id)

    def delete_playlist(self, voice_channel_id):
        return self._conn.delete(voice_channel_id)

