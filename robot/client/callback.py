from telegram import Update
from telegram.ext import CallbackContext
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton

from json import dump

import re


class CommandHandlerCallbacks:
    """Mix-in classes defines Telegram client callback methods"""

    def __init__(self):
        # Initiate register and tracking details dict
        self.shipment_details: dict = {}

    def start_callback(self, update, context) -> None:
        """Processes '/start' command from user"""

        customer_name = update.message.from_user.first_name
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

        if customer_name:
            # Greet user
            reply_text(f"Hello {update.message.from_user.first_name} 👋")

            # Store name
            self.shipment_details["custormer_name"] = customer_name

            print(self.shipment_details)

            # Reply user with inline keyboard to selection options
            reply_text(
                "Do you want to register shipment or track shipment?\nUse the buttons below to answer👇",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

        return

    def inline_button_callback(self, update: Update, context: CallbackContext) -> None:
        """Get button that was tapped on. This is base on what is assigned to 'callback-data' param in the 'InlineKeyboardButton' object"""

        query = update.callback_query

        if query.data == "register_shipment":
            query.answer("Loading...")
            self.register_shipment_callback(update=update, context=context)
        elif query.data == "track_shipment":
            query.answer("Loading...")
            self.track_shipment_callback(update=update, context=context)

    def register_shipment_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Processes 'register_shipment' inline button command"""

        text: str = """Good pick👍 \n\nI can help you create your shipment\n\nYou can control me by sending these commands:\n\n*User Details*\n /setemail \- Set your email address\n/setphonenumber \- Set your phone number\n/setitemname \- Site item name\n/settrackingnumber \- Set shipment tracking number\n/setcarriername \- Set shipment carrier name\n/setaddress \- Set delivery address\n\n_Dont't want to register, but track shipment? use the /start command to select your option_"""

        update.callback_query.edit_message_text(text, parse_mode="MarkdownV2")

    def track_shipment_callback(self, update: Update, context: CallbackContext) -> None:
        """Processes 'track_shipment' inline button command"""

        text: str = """Good pick👍 \n\nI can help you track your shipment\n\nYou can control me by sending these commands:\n\n*Tracking Details*\n/settrackingnumber \- Set shipment tracking number\n/setcarriername \- Set caurrier name\n\n_Dont't want to track, but register shipment? use the /start command to select your option_"""

        update.callback_query.edit_message_text(text, parse_mode="MarkdownV2")

    # Process user command
    def set_email_callback(self, update: Update, context: CallbackContext) -> None:
        """Process '/setemail' command from user"""

        reply_text = update.message.reply_text

        try:
            user_email: str = str(context.args[0]).strip()

            # Validate user email
            email_regex = (
                "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
                or "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
            )

            if self._validation_regex(email_regex, user_email):
                self.shipment_details["email"] = user_email
                reply_text("Success! Email set. /help")
            else:
                reply_text(
                    "Invalid email addresss\!\n hint: /setemail _info@domain\.com_",
                    parse_mode="MarkdownV2",
                )
        except (IndexError, ValueError) as e:
            print(e)

            reply_text(
                "Email addresss not set\!\n hint: /setemail _Your email\. e\.g\: info@domain\.com_",
                parse_mode="MarkdownV2",
            )

    def set_phone_callback(self, update: Update, context: CallbackContext) -> None:
        """Process '/setphonenumber' command from user"""

        reply_text = update.message.reply_text

        try:
            user_phone_number: str = str(context.args[0]).strip()

            # Validate phone number
            phone_regex = "([0-9]{11})"

            if self._validation_regex(phone_regex, user_phone_number):
                self.shipment_details["customer_phone_number"] = user_phone_number
                reply_text("Success! Phone number set. /help")
            else:
                reply_text(
                    "Invalid phone number\!\n hint: /setphonenumber _Your phone number_",
                    parse_mode="MarkdownV2",
                )
        except (IndexError, ValueError) as e:
            print(e)

            reply_text(
                "Phone number not set\!\n hint: /setphonenumber _Your phone number_",
                parse_mode="MarkdownV2",
            )

    def set_item_name_callback(self, update: Update, context: CallbackContext):
        """Process '/setitemname' command"""
        reply_text = update.message.reply_text

        try:
            item_name: str = str(context.args[0]).strip()
            self.shipment_details["item_name"] = item_name

            reply_text("Success! Item name set. /help")
        except (IndexError, ValueError) as e:
            print(e)

            reply_text(
                "Item name not set\!\n hint: /setitemname _package name_",
                parse_mode="MarkdownV2",
            )

    def set_tracking_number_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Process '/settrackingnumber' command from user"""
        reply_text = update.message.reply_text

        try:
            tracking_id = str(context.args[0]).strip()
            self.shipment_details["tracking_id"] = tracking_id

            reply_text("Success! Tracking number set. /help")
        except (IndexError, ValueError) as e:
            print(e)

            error_response = """Tracking id not set or Invalid id\!\n hint: /settrackingnumber _shipment tracking number_"""

            reply_text(error_response, parse_mode="MarkdownV2")

    def set_carrier_callback(self, update: Update, context: CallbackContext) -> None:
        """Process '/setcarrier' command from user"""
        reply_text = update.message.reply_text

        try:
            carrier_name = str(context.args[0]).strip()
            self.shipment_details["carrier_name"] = carrier_name

            reply_text("Success! Carrier name set. /help")
        except (ValueError, IndexError) as e:
            print(e)

            error_response = """Carrier name not set\.\n hint: /setcarriername _shipment tracking number_"""

            reply_text(error_response, parse_mode="MarkdownV2")

    def set_address_callback(self, update: Update, context: CallbackContext) -> None:
        """Process '/setaddress' command"""
        reply_text = update.message.reply_text

        try:
            company = str(context.args[0]).strip() or ""
            street = str(context.args[1]).strip() or ""
            city = str(context.args[2]).strip() or ""
            state = str(context.args[3]).strip() or ""
            zip_code = str(context.args[4]).strip() or ""

            if company or street or city or state or zip_code:
                self.shipment_details["addresss"] = {
                    "company": company,
                    "street": street,
                    "city": city,
                    "state": state,
                    "zip_code": zip_code,
                }

                reply_text("Success! Address set. /help")

                print(self.shipment_details)

                return
        except (ValueError, IndexError) as e:
            print(e)
            error_response = """Address not set\!\n Hint: /setaddress _company street city state zip\_code _\n Note: _Use \- instead of space to seperate longer words\. e\.g\: "1st\-Avenue" instead of "1st Avenue" for street name_"""

            reply_text(error_response, parse_mode="MarkdownV2")

    def help_callback(self, update: Update, context: CallbackContext) -> None:
        """Process '/help' command"""

        if update:

            help_guide = """Glad to help\!\n\nYou can control me by sending these commands:\n\n*Register shipment*\n /setemail \- Set your email address\n/setphonenumber \- Set your phone number\n/setitemname \- Site item name\n/settrackingnumber \- Set shipment tracking number\n/setcarriername \- Set shipment carrier name\n/setaddress \- Set delivery address\n\n_Dont't want to register, but track shipment? use the /start command to select your option_"""

            update.message.reply_text(help_guide, parse_mode="MarkdownV2")

    def _validation_regex(self, pattern: str, string: str) -> bool:
        """Validate specific user input using regex"""
        if re.search(pattern=pattern, string=string):
            return True
        else:
            return False

    def _parse_markdown_symbols(self, response: str) -> None:
        """This method escape all markdown with a back-slash \ to prevent error wheb parsing markdown"""

        pass

    def get_shipment_details(self) -> dict:
        """ Checks if shipment details available, then return it."""
        if self.shipment_details and len(self.shipment_details) == 7:
            print(self.shipment_details)
            return self.shipment_details
