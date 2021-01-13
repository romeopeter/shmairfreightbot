import telegram
from decouple import config
from typing import List, Dict, Union, Optional


class Client:
    """
    Telegram client interface. Object interacts with user inputs via Telegram's API
    """

    def __init__(self, token: str) -> None:
        """
        Initializes Client Object

        Parameters
        --------
        token: str
            Telegram bot token key

        Returns
        -------
        None -- Nothing is returned
        """

        self.bot = telegram.Bot(token=token)

        # Test call
        print(self.bot.get_me())


if __name__ == "__main__":
    tclient = Client(token=config("TELEGRAM_API_TOKEN", cast=str))
