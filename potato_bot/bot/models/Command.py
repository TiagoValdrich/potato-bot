from discord import Message, VoiceClient
from aiohttp import ClientSession

# @Interface
class Command:
    """
        All the commands that will be created on this bot, must have heritage from this class.
    """

    @staticmethod
    def info() -> dict:
        raise NotImplemented(
            "This method must be implemented describing the command name, it's description, kind of command, permissions..."
        )

    async def run(
        self,
        session: ClientSession,
        message: Message,
        params: list,
        voice_clients: list,
    ) -> dict:
        raise NotImplemented(
            "This method must be implemented with the command functionality!"
        )
