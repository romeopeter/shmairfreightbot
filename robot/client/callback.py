from telegram import Update
from telegram.ext import CallbackContext
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton

import re


class CommandHandlerCallbacks:
    """Mix-in classes defines Telegram client callback methods"""

    def __init__(self):
        # Initiate register and tracking details dict
        self.registeration_and_shipment_details: dict = {
            "user_details": {},
            "shipment_details": {},
        }

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

        # Check for update.
        if update:

            # Greet user
            reply_text(f"Welcome {update.message.from_user.first_name} 👋")

            # Reply user with inline keyboard to selection options
            reply_text(
                "Do you want to register shipment or track shipment?\nUse the buttons below to answer👇",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

            print(self.registeration_and_shipment_details)

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

        text: str = """Good pick👍 \n\nI can help you create your shipment\n\nYou can control me by sending these commands:\n\n*User Details*\n /setname \- set your name\n/setemail \- Set your email address\n/setphonenumber \- Set your phone number\n/trackingnumber \- Set shipment tracking number\n/setcaurriername \- Set shipment caurrier name\n\n_Dont't want to register, but track shipment? use the /start command to select your option_"""

        update.callback_query.edit_message_text(text, parse_mode="MarkdownV2")

    def track_shipment_callback(self, update: Update, context: CallbackContext) -> None:
        """Processes 'track_shipment' inline button command"""

        text: str = """Good pick👍 \n\nI can help you track your shipment\n\nYou can control me by sending these commands:\n\n*Tracking Details*\n/settrackingnumber \- Set shipment tracking number\n/setcaurrier \- Set caurrier name\n\n_Dont't want to track, but register shipment? use the /start command to select your option_"""

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

                    # Store name in
                    self.registeration_and_shipment_details["user_details"][
                        "first_name"
                    ] = first_name
                    self.registeration_and_shipment_details["user_details"][
                        "last_name"
                    ] = last_name
                    return
            except (ValueError, IndexError):
                update.message.reply_text("/setname <first_name last_name>")

    def set_email_callback(self, update, context):
        """Process '/setemail' command from user"""

        if update:
            try:
                user_email = context.args[0]

                # Validate user email
                email_regex = (
                    "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
                    or "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
                )

                if self._validation_regex(email_regex, email_regex):
                    self.registeration_and_shipment_details["user_details"][
                        "email"
                    ] = user_email
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

        if update:
            try:
                user_phone_number = context.args[0]

                # Validate phone number
                phone_regex = "((^+234)|[0-9]{11})"

                if self._validation_regex(phone_regex, user_phone_number):
                    self.registeration_and_shipment_details["user_details"][
                        "phone_number"
                    ] = user_phone_number
                else:
                    update.message.reply_text(
                        "Invalid phone number!\n _hint: /setemail <08XXXXXXXXX>_",
                        parse_mode="MarkdownV2",
                    )
            except Exception as e:
                print(e)
                # update.message.reply_text("Awesome👍 Your detail has been set")

    # Collects tracking details
    def set_item_name_callback(self, update, context) -> None:
        """Process '/setitemname' command from user"""

        if update:
            try:
                item_name = str(context.args[0])
                self.registeration_and_shipment_details["shipment_details"][
                    "item_name"
                ] = item_name
            except Exception as e:
                print(e)
                # update.message.reply_text("/setname <first_name last_name>")

    def set_tracking_number_callback(self, update, context) -> None:
        """Process '/settrackingnumber' command from user"""

        if update:
            try:
                response = update.message.from_user.text
                print(response)
            except Exception as e:
                print(e)
                # update.message.reply_text("Awesome👍 Your detail has been set")

    def set_caurrier_callback(self, update, context) -> None:
        """Process '/setcaurrier' command from user"""

        if update:
            try:
                caurrier_name = str(context.args[0])
                self.registeration_and_shipment_details["shipment_details"][
                    "caurrier_name"
                ] = caurrier_name
            except Exception as e:
                print(e)
                # update.message.reply_text("Awesome👍 Your detail has been set")

    def _validation_regex(self, pattern: str, string: str) -> bool:
        """Validate specific user input using regex"""
        if re.search(pattern=pattern, string=string):
            return True
        else:
            return False
