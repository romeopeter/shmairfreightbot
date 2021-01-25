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

    def inline_button_callback(self, update, context) -> None:
        """Defines which button was tapped on from what is assigned to 'callback-data' in 'InlineKeyboardButton' object"""

        button = update.callback_query.data

        if button == "register_shipment":
            self.register_shipment_callback(update=update, context=context)
        elif button == "track_shipment":
            self.track_shipment_callback(update=update, context=context)

    def register_shipment_callback(self, update, context) -> None:
        """Processes 'register_shipment' inline button command"""

        # reply_text = update.message.reply_text

        # text: str = """Good pick👍🏿 \n\nI can help you create your shipment\n\nYou can control me by sending these commands:\n\n*User Details*\n /setname \- set your name\n/setemail \- Set your email address\n/setphonenumber \- Set your phone number"""

        # reply_text(text)

        print(repr(update.message.reply_text("jdjdjjdjjjjjdjh")))

    def track_shipment_callback(self, update, context) -> None:
        """Processes 'track_shipment' inline button command"""

        # reply_text = update.message.reply_text

        # text: str = """Good pick👍🏿 \n\nI can help you track your shipment\n\nYou can control me by sending these commands:\n\n*Tracking Details*\n /setitemname \- set shipment item name\n/settrackingnumber \- Set shipment tracking number\n/setcaurrier \- Set caurrier name"""

        # reply_text(text)

        print(repr(update.message.reply_text("jdjdjjdjjjjjdjh")))

    # Collects user detatails
    def set_name_callback(self, update, context) -> None:
        """Process '/setname' command from user"""

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
