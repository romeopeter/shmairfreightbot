from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton


class CommandHandlerCallbacks:
    """
    Mix-in classes defines Telegram client commands as callback functions
    """

    def start_callback(self, update, context) -> None:
        """Processes '/start' command from user"""

        reply_text = update.message.reply_text
        keyboard: list = [
            [
                InlineKeyboardButton(
                    "Register shipment", callback_data="register_shipment"
                ),
                InlineKeyboardButton("Track shipment", callback_data="track_shipment"),
            ]
        ]

        if update:

            # Greet user
            reply_text(f"Welcome {update.message.from_user.first_name} 👋🏿")

            # Display inline keyboard to user
            reply_text(
                "Do you want register shipment or track a shipment?",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

    def inline_button_callback(self, update, context) -> None:
        query = update.callback_query.answer()

        # Defines which button was tapped on from what is assigned to 'callback-data' in 'InlineKeyboardButton' object
        button = query.data

        if button == "register_shipment":
            self.register_shipment_callback(update=update, context=context)
        elif button == "track_shipment":
            self.track_shipment_callback(update=update, context=context)

    def register_shipment_callback(self, update, context) -> None:
        """
        Processes 'register_shipment' inline button command
        """

        reply_text = update.message.reply_text

        text: str = """Good pick👍🏿 \n\nI can help you track your shipment\n\nYou can control me by sending these commands:\n\n*Tracking Details*\n /setitemname \- set shipment item name\n/settrackingnumber \- Set shipment tracking number\n/setcaurrier \- Set caurrier name"""

        reply_text(text)

    def track_shipment_callback(self, update, context) -> None:
        """
        Processes 'track_shipment' inline button command
        """

        reply_text = update.message.reply_text

        text: str = """Good pick👍🏿 \n\nI can help you create your shipment\n\nYou can control me by sending these commands:\n\n*User Details*\n /setname \- set your name\n/setemail \- Set your email address\n/setphonenumber \- Set your phone number"""

        reply_text(text)

    # Collects user detatails
    def set_name_callback(self, update, context) -> None:
        """Processes commands to set user details"""

        if update:
            try:
                first_name = str(context.args[0]) or update.message.from_user.first_name
                last_name = str(context.args[1]) or update.message.from_user.lat_name
                print(first_name, last_name)

                if first_name or last_name:
                    update.message.reply_text(f"Hello {first_name}!")
                    return
            except (ValueError, IndexError):
                update.message.reply_text("/setname <first_name last_name>")

    def set_email_callback(self, update, context):
        if update:
            try:
                response = update.message.from_user.text
                print(response)
            except:
                update.message.reply_text("Awesome👍🏿 Your detail has been set")

    def set_phone_callback(self, update, context):
        if update:
            try:
                response = update.message.from_user.text
                print(response)
            except:
                update.message.reply_text("Awesome👍🏿 Your detail has been set")

    # Collects tracking details
    def set_item_name_callback(self, update, context) -> None:
        """Processes commands to set user details"""

        if update:
            try:
                first_name = str(context.args[0]) or update.message.from_user.first_name
                last_name = str(context.args[1]) or update.message.from_user.lat_name
                print(first_name, last_name)

                if first_name or last_name:
                    update.message.reply_text(f"Hello {first_name}!")
                    return
            except (ValueError, IndexError):
                update.message.reply_text("/setname <first_name last_name>")

    def set_tracking_number_callback(self, update, context):
        if update:
            try:
                response = update.message.from_user.text
                print(response)
            except:
                update.message.reply_text("Awesome👍🏿 Your detail has been set")

    def set_caurrier_callback(self, update, context):
        if update:
            try:
                response = update.message.from_user.text
                print(response)
            except:
                update.message.reply_text("Awesome👍🏿 Your detail has been set")
