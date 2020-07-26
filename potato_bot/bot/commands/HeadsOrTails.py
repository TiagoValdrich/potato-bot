from random import randrange
from discord import Message, TextChannel, File, Embed
from operator import mod


class HeadsOrTails:
    def __init__(self, message: Message):
        self.message = message
        self.channel = message.channel

    async def play(self):
        number = randrange(1, 10)

        if mod(number, 2) == 0:
            embed = Embed(title="Heads!", color=0x00FF00)
            heads_file = File("resources/heads.png", filename="heads.png")
            embed.set_image(url="attachment://heads.png")
            await self.channel.send(file=heads_file, embed=embed)
        else:
            embed = Embed(title="Tails!", color=0x00FF00)
            heads_file = File("resources/tails.png", filename="tails.png")
            embed.set_image(url="attachment://tails.png")
            await self.channel.send(file=heads_file, embed=embed)
