from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler

from decouple import config

from callback import CommandHandlerCallbacks


class Client(CommandHandlerCallbacks):
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

        self.token = token
        self.bot = Bot(token=self.token)
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def get_me(self) -> dict:
        """
        Tests Bot's auth token.

        Returns
        -------
        dict -- Dictionary filled with Bot's auth details
        """

        return self.bot.get_me()

    def set_handler(self) -> None:
        """
        Dispatches callback function in to process user inputs via 'CommandHandler' method
        """

        self.dispatcher.add_handler((CommandHandler("start", self.start_callback)))

    def start_client(self) -> None:
        """
        Sets dispatcher and starts the bot

        Returns
        -------
        None -- Returns nothing.
        """

        self.set_handler()
        self.updater.start_polling()


if __name__ == "__main__":
    tclient = Client(token=config("TELEGRAM_API_TOKEN", cast=str))
    tclient.start_client()
