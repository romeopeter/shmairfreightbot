from telegram import Update
from telegram.ext import CallbackContext
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton

import re


class CommandHandlerCallbacks:
    """Mix-in classes defines Telegram client callback methods"""

    def __init__(self):
        # Initiate register and tracking details dict
        self.shipment_details: dict = {}

    def start_callback(self, update, context) -> None:
        """Processes '/start' command from user"""

        reply_text = update.message.reply_text

        # inline keyboard command
        keyboard: list = [
            [
                InlineKeyboardButton(
                    "Register shipment", callback_data="register_shipment"
                ),
                InlineKeyboardButton("Track shipment", callback_data="track_shipment"),
            ]
        ]

        # Greet user
        reply_text(f"Welcome {update.message.from_user.first_name} 👋")

        # Reply user with inline keyboard to selection options
        reply_text(
            "Do you want to register shipment or track shipment?\nUse the buttons below to answer👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    def inline_button_callback(self, update: Update, context: CallbackContext) -> None:
        """Defines which button was tapped on from what is assigned to 'callback-data' in 'InlineKeyboardButton' object"""

        query = update.callback_query

        if query.data == "register_shipment":
            query.answer("👍")
            self.register_shipment_callback(update=update, context=context)
        elif query.data == "track_shipment":
            query.answer("👍")
            self.track_shipment_callback(update=update, context=context)

    def register_shipment_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Processes 'register_shipment' inline button command"""

        text: str = """Good pick👍 \n\nI can help you create your shipment\n\nYou can control me by sending these commands:\n\n*User Details*\n /setname \- set your [prefered] name\n/setemail \- Set your email address\n/setphonenumber \- Set your phone number\n/trackingnumber \- Set shipment tracking number\n/setcaurriername \- Set shipment caurrier name\n\n_Dont't want to register, but track shipment? use the /start command to select your option_"""

        update.callback_query.edit_message_text(text, parse_mode="MarkdownV2")

    def track_shipment_callback(self, update: Update, context: CallbackContext) -> None:
        """Processes 'track_shipment' inline button command"""

        text: str = """Good pick👍 \n\nI can help you track your shipment\n\nYou can control me by sending these commands:\n\n*Tracking Details*\n/settrackingnumber \- Set shipment tracking number\n/setcaurrier \- Set caurrier name\n\n_Dont't want to track, but register shipment? use the /start command to select your option_"""

        update.callback_query.edit_message_text(text, parse_mode="MarkdownV2")

    # Process user based commands
    def set_name_callback(self, update, context) -> None:
        """Process '/setname' command from user"""

        try:
            first_name = (
                str(context.args[0]).strip() or update.message.from_user.first_name
            )
            last_name = (
                str(context.args[1]).strip() or update.message.from_user.last_name
            )

            if first_name or last_name:
                update.message.reply_text(f"Hello {first_name}!")

                # Store name in
                self.shipment_details["custormer_fname"] = first_name
                self.shipment_details["customer_lname"] = last_name

        except (ValueError, IndexError):
            update.message.reply_text("/setname <first_name last_name>")

    def set_email_callback(self, update, context):
        """Process '/setemail' command from user"""

        try:
            user_email: str = str(context.args[0]).strip()

            # Validate user email
            email_regex = (
                "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
                or "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
            )

            if self._validation_regex(email_regex, email_regex):
                self.shipment_details["shipment_details"]["email"] = user_email
            else:
                update.message.reply_text(
                    "Invalid email addresss!\n _hint: /setemail <info@domain.com>_",
                    parse_mode="MarkdownV2",
                )
        except Exception as e:
            # update.message.reply_text("Awesome👍 Your detail has been set")
            print(e)

    def set_phone_callback(self, update, context) -> None:
        """Process '/setphonenumber' command from user"""

        try:
            user_phone_number: str = str(context.args[0]).strip()

            # Validate phone number
            phone_regex = "(|[0-9]{11})"

            if self._validation_regex(phone_regex, user_phone_number):
                self.shipment_details["customer_phone_number"] = user_phone_number
            else:
                update.message.reply_text(
                    "Invalid phone number!\n _hint: /setemail <08XXXXXXXXX>_",
                    parse_mode="MarkdownV2",
                )
        except Exception as e:
            print(e)
            # update.message.reply_text("Awesome👍 Your detail has been set")

    def set_tracking_number_callback(self, update, context) -> None:
        """Process '/settrackingnumber' command from user"""

        try:
            tracking_id: str = str(context.args[0]).strip()
            tracking_id_regex = ""
            if self._validation_regex(tracking_id_regex, tracking_id):
                self.shipment_details["tracking_id"] = tracking_id
        except Exception as e:
            print(e)
            # update.message.reply_text(
            #     "Invalid tracking id!\n _hint: /settrackingid <08XXXXXXXXX>_",
            #     parse_mode="MarkdownV2",
            # )

    def set_caurrier_callback(self, update, context) -> None:
        """Process '/setcaurrier' command from user"""

        try:
            caurrier_name = str(context.args[0]).strip()
            self.shipment_details["shipment_details"]["caurrier_name"] = caurrier_name
        except Exception as e:
            print(e)
            # update.message.reply_text("Awesome👍 Your detail has been set")

    def _validation_regex(self, pattern: str, string: str) -> bool:
        """Validate specific user input using regex"""
        if re.search(pattern=pattern, string=string):
            return True
        else:
            return False

    def get_shipment_details(self) -> dict:
        """ Checks if shipment details available, then return it."""
        if self.shipment_details and len(self.shipment_details) == 6:
            print(self.shipment_details)
            return self.shipment_details
