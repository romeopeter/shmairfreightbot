from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler

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

    def set_dispatchers(self) -> None:
        """
        Calls dispatcher to register handlers via 'CommandHandler' method.
        """

        # Dispatches 'start' command callback
        start_command = self.dispatcher.add_handler(
            (CommandHandler("start", self.start_callback))
        )

        # Dispatches command button callback for inline keyboard
        keyboad_command = self.dispatcher.add_handler(
            CallbackQueryHandler(self.inline_button_callback, pass_user_data=True)
        )

        """Prevent text command before keyboad commands when in inline mode.
        Text command example: '/setname', '/setemail', '/setphonenumber' etc"""
        if start_command:

            if keyboad_command:

                # Dispatches user details callbacks
                self.dispatcher.add_handler(
                    (CommandHandler("setname", self.set_name_callback))
                )
                self.dispatcher.add_handler(
                    (CommandHandler("setemail", self.set_email_callback))
                )
                self.dispatcher.add_handler(
                    (CommandHandler("setphonenumber", self.set_phone_callback))
                )

                # Dispatches user tracking details callbacks
                self.dispatcher.add_handler(
                    (CommandHandler("setitemname", self.set_item_name_callback))
                )
                self.dispatcher.add_handler(
                    (
                        CommandHandler(
                            "settrackingnumber", self.set_tracking_number_callback
                        )
                    )
                )
                self.dispatcher.add_handler(
                    (CommandHandler("setcaurrier", self.set_caurrier_callback))
                )
            else:
                chat_id = self.bot.get_updates()
                # self.bot.send_message(chat_id=chat_id, texg="I'm sorry but I can't do that")
                print(chat_id)

    def start_client(self) -> None:
        """
        Sets dispatcher and starts the bot

        Returns
        -------
        None -- Returns nothing.
        """

        self.set_dispatchers()
        self.updater.start_polling()

    def stop_client(self):
        # Stop client from running when the Ctrl + c signal is detected
        self.updater.idle()


if __name__ == "__main__":
    tclient = Client(token=config("TELEGRAM_API_TOKEN", cast=str))

    print("Starting Bot...")

    # Start client
    tclient.start_client()

    # Start client
    tclient.stop_client()
