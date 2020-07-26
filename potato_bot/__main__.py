import os, logging

from potato_bot.bot.PotatoBot import PotatoBot
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def load_bot_token() -> str:
    token = os.getenv("BOT_TOKEN")

    if not token:
        load_dotenv()
        token = os.getenv("BOT_TOKEN")

    return token


try:
    potato_bot = PotatoBot()
    potato_bot.run(load_bot_token())
except AttributeError as e:
    logger.error("Invalid token, exiting application")
    exit(-1)
