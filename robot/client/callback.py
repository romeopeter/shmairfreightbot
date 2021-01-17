class CommandHandlerCallbacks:
    """
    Mix-in classes defines Telegram client commands as callback functions
    """

    def start_callback(self, update, context) -> None:
        """
        Processes '/start' command from user
        """

        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")
