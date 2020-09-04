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

    def get_musics(self, channel_id):
        return self._conn.lrange(channel_id, 0, -1)

    def add_music(self, channel_id, music_url: str):
        return self._conn.rpush(channel_id, music_url)

    def get_next_music(self, channel_id):
        return self._conn.lpop(channel_id)

