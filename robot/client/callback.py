from telegram import Update
from telegram.ext import CallbackContext
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton


class CommandHandlerCallbacks:
    """Mix-in classes defines Telegram client callback methods"""

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

        # Check for update, then reply.
        if update:

            # Greet user
            reply_text(f"Welcome {update.message.from_user.first_name} 👋🏿")

            # Display inline keyboard to user
            reply_text(
                "Do you want to register shipment or track shipment?\nUse the buttons below to answer👇🏿",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

    def inline_button_callback(self, update: Update, context: CallbackContext) -> None:
        """Defines which button was tapped on from what is assigned to 'callback-data' in 'InlineKeyboardButton' object"""

        query = update.callback_query

        if query.data == "register_shipment":
            query.answer("👍🏿")
            self.register_shipment_callback(update=update, context=context)
        elif query.data == "track_shipment":
            query.answer("👍🏿")
            self.track_shipment_callback(update=update, context=context)

    def register_shipment_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Processes 'register_shipment' inline button command"""

        text: str = """Good pick👍🏿 \n\nI can help you create your shipment\n\nYou can control me by sending these commands:\n\n*User Details*\n /setname \- set your name\n/setemail \- Set your email address\n/setphonenumber \- Set your phone number\n\n_Use the /start command to pick your options_"""

        update.callback_query.edit_message_text(text, parse_mode="MarkdownV2")

    def track_shipment_callback(self, update: Update, context: CallbackContext) -> None:
        """Processes 'track_shipment' inline button command"""

        text: str = """Good pick👍🏿 \n\nI can help you track your shipment\n\nYou can control me by sending these commands:\n\n*Tracking Details*\n /setitemname \- set shipment item name\n/settrackingnumber \- Set shipment tracking number\n/setcaurrier \- Set caurrier name\n\n_Use the /start command to pick your options_"""

        update.callback_query.edit_message_text(text, parse_mode="MarkdownV2")

    # Collects user detatails
    def set_name_callback(self, update, context) -> None:
        """Process '/setname' command from user"""

        if update:
            try:
                first_name = str(context.args[0]) or update.message.from_user.first_name
                last_name = str(context.args[1]) or update.message.from_user.last_name
                print(first_name, last_name)

                if first_name or last_name:
                    update.message.reply_text(f"Hello {first_name}!")
                    return
            except (ValueError, IndexError):
                update.message.reply_text("/setname <first_name last_name>")

    def set_email_callback(self, update, context):
        """Process '/setemail' command from user"""

        if update:
            try:
                response = update.message.from_user.text
                print(response)
            except:
                update.message.reply_text("Awesome👍🏿 Your detail has been set")

    def set_phone_callback(self, update, context) -> None:
        """Process '/setphonenumber' command from user"""

        if update:
            try:
                response = update.message.from_user.text
                print(response)
            except:
                update.message.reply_text("Awesome👍🏿 Your detail has been set")

    # Collects tracking details
    def set_item_name_callback(self, update, context) -> None:
        """Process '/setitemname' command from user"""

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

    def set_tracking_number_callback(self, update, context) -> None:
        """Process '/settrackingnumber' command from user"""

        if update:
            try:
                response = update.message.from_user.text
                print(response)
            except:
                update.message.reply_text("Awesome👍🏿 Your detail has been set")

    def set_caurrier_callback(self, update, context) -> None:
        """Process '/setcaurrier' command from user"""

        if update:
            try:
                response = update.message.from_user.text
                print(response)
            except:
                update.message.reply_text("Awesome👍🏿 Your detail has been set")
