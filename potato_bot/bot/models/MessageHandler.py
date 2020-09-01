from os import listdir
from os.path import isfile, join
from importlib import import_module
from potato_bot import ROOT_PATH
from potato_bot.bot.models.Command import Command
from discord import Message, Embed
from aiohttp import ClientSession


class MessageHandler:
    """
        Get discord message and check if there is any command related to it.
        If the message is assign to a command, this class will instantiate the command
    """

    BOT_PREFIX = "!"
    HELP_COMMAND = "help"

    def __init__(self, bot, message: Message, session: ClientSession):
        self.message = message
        self.bot = bot
        self.session = session
        self.commands_available = {}

        self._get_commands_trigger()

    def _get_commands_trigger(self) -> None:
        commands_dir = join(ROOT_PATH, "bot", "commands")

        for f in listdir(commands_dir):
            if isfile(join(commands_dir, f)) and ".py" in f:
                class_name = f.replace(".py", "")
                module_path = f"potato_bot.bot.commands.{class_name}"

                command_model: Command = getattr(import_module(module_path), class_name)
                command_info = command_model.info()

                self.commands_available[command_info["name"]] = command_model

    def valid_message(self) -> bool:
        if (
            self.bot.user.id != self.message.author.id
            and isinstance(self.message.content, str)
            and len(self.message.content) > 0
            and self.message.content[0] == self.BOT_PREFIX
        ):
            return True

        return False

    async def display_commands_info(self) -> None:
        embed = Embed(
            title="Commands available",
            description=f"All the commands bellow must be used with the bot prefix {self.BOT_PREFIX}.\n Example.: !headsortails\n",
            color=0x4287F5,
        )

        for name in self.commands_available:
            command: Command = self.commands_available[name]()
            command_info = command.info()

            if command_info["description"]:
                embed.add_field(
                    name=name, value=command_info["description"], inline=False
                )

        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await self.message.channel.send(embed=embed)

    async def handle(self):
        if self.valid_message():
            striped_message: list = self.message.content.split(" ")
            command_name = striped_message.pop(0).replace(self.BOT_PREFIX, "")

            if command_name == self.HELP_COMMAND:
                await self.display_commands_info()

            if command_name in list(self.commands_available.keys()):
                command: Command = self.commands_available[command_name]()
                await command.run(
                    self.session, self.message, striped_message, self.bot,
                )
