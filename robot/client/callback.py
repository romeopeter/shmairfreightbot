import sys

import re

from typing import Any

from telegram import Update
from telegram.ext import CallbackContext
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton

from decouple import config

from psycopg2.sql import SQL

from robot.storage.dbconnection import Connection


class CommandHandlerCallbacks:
    """Mix-in classes defines Telegram client callback methods"""

    def __init__(self) -> None:
        self._store = self.store_details()


    def start_callback(self, update, context) -> None:
        """Processes '/start' command from user"""

        customer_name = str(update.message.from_user.first_name)
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
        reply_text(f"Hello {update.message.from_user.first_name} 👋")

        customer_name = self._remove_double_quotes(customer_name)

        # Store name
        statement = SQL("INSERT INTO shipment ({}) VALUES (%s)")
        store_name = self._store.create(
            statement=statement,
            values= {"table_column":'name', "column_value":customer_name}
        )

        if store_name:
            # Reply user with inline keyboard to selection options
            reply_text(
                "Do you want to register shipment or track shipment?\nUse the buttons below to answer👇",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )



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
            user_email = str(context.args[0]).strip()

            # Validate user email
            email_regex = (
                "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
                or "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
            )

            # Validate email
            if self._validation_regex(email_regex, user_email):

                user_email = self._remove_double_quotes(user_email)

                # Store email
                statement = SQL("INSERT INTO shipment ({}) VALUES (%s)")
                store_email = self._store.create(
                    statement=statement,
                    values={"table_column":'email',"column_value":user_email}
                )

                if store_email:
                    reply_text("Success! Email set. /help")
            else:
                reply_text(
                    "Invalid email addresss\!\n hint: /setemail _info@domain\.com_",
                    parse_mode="MarkdownV2",
                )
        except (IndexError, ValueError):
            reply_text(
                "Email addresss not set\!\n hint: /setemail _Your email\. e\.g\: info@domain\.com_",
                parse_mode="MarkdownV2",
            )

    def set_phone_callback(self, update: Update, context: CallbackContext) -> None:
        """Process '/setphonenumber' command from user"""

        reply_text = update.message.reply_text

        try:
            phone_number = str(context.args[0]).strip()

            if self._validation_regex("([0-9]{11})", phone_number):

                phone_number = self._remove_double_quotes(phone_number)

                # Store phone number
                statement = SQL("INSERT INTO shipment ({}) VALUES (%s)")
                store_pnumber = self._store.create(
                    statement=statement,
                    values={
                        "table_column":'phone_number',
                        "column_value":phone_number
                    }
                )

                if store_pnumber:
                    reply_text("Success! Phone number set. /help")
            else:
                reply_text(
                    "Invalid phone number\!\n hint: /setphonenumber _081XXXXXX00_",
                    parse_mode="MarkdownV2",
                )
        except (IndexError, ValueError):
            reply_text(
                "Phone number not set\!\n hint: /setphonenumber _Your phone number_",
                parse_mode="MarkdownV2",
            )

    def set_item_name_callback(self, update: Update, context: CallbackContext):
        """Process '/setitemname' command"""
        reply_text = update.message.reply_text

        try:
            item_name = str(context.args[0]).strip()

            item_name = self._remove_double_quotes(item_name)

            # Store item name
            statement = SQL("INSERT INTO shipment ({}) VALUES (%s)")
            store_item = self._store.create(
                statement=statement,
                values={"table_column":'item_name', "column_value":item_name}
            )

            if store_item:
                reply_text("Success! Item name set. /help")

        except (IndexError, ValueError):
            reply_text(
                "Item name not set\!\n hint: /setitemname _package name_",
                parse_mode="MarkdownV2",
            )

    def set_carrier_callback(self, update: Update, context: CallbackContext) -> None:
        """Process '/setcarrier' command from user"""
        reply_text = update.message.reply_text

        try:
            carrier_name = str(context.args[0]).strip()
            carrier_name = self._remove_double_quotes(carrier_name)

            # Store carrier
            statment = SQL("INSERT INTO shipment ({}) VALUES (%s)")
            store_carrier = self._store.create(
                statement=statment,
                values={"table_column":'carrier', "column_value":carrier_name}
            )

            if store_carrier:
                reply_text("Success! Carrier name set. /help")
        except (ValueError, IndexError):
            error_response = """Carrier name not set\.\n hint: /setcarriername _shipment tracking number_"""

            reply_text(error_response, parse_mode="MarkdownV2")

    def set_tracking_number_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Process '/settrackingnumber' command from user"""

        reply_text = update.message.reply_text

        try:
            tracking_id = str(context.args[0]).strip()
            tracking_id = self._remove_double_quotes(tracking_id)

            # Store tracking id
            statment = SQL("INSERT INTO shipment ({}) VALUES (%s)")
            store_tracking_id = self._store.create(
                statement=statment,
                values={
                    "table_column":'tracking_id',
                    "column_value":tracking_id
                }
            )

            if store_tracking_id:
                reply_text("Success! Tracking number set. /help")
        except (IndexError, ValueError):

            error_response = """Tracking id not set or Invalid id\!\n hint: /settrackingnumber _shipment tracking number_"""

            reply_text(error_response, parse_mode="MarkdownV2")

    def set_address_callback(self, update: Update, context: CallbackContext) -> None:
        """Process '/setaddress' command"""

        reply_text = update.message.reply_text

        try:
            company = str(context.args[0]).strip()
            street = str(context.args[1]).strip()
            city = str(context.args[2]).strip()
            state = str(context.args[3]).strip()
            zip_code = str(context.args[4]).strip()

            company,
            street,
            city,
            state,
            zip_code = (
                self._remove_double_quotes(company, street, city, state, zip_code)
            )

            if company and street and city and state and zip_code:
                print(company,street,city,state,zip_code)

                # Store address
                statment = SQL(
                    """INSERT INTO shipment ({},{},{},{},{})
                    VALUES (%s, %s, %s, %s, %s)"""
                )

                store_address = self._store.create(
                    statement=statment,
                    values={
                        "table_columns": [
                            'company',
                            'street',
                            'city',
                            'state',
                            'zip_code'
                        ],
                        "column_values": [company,street,city,state,zip_code]
                    }
                )

                if store_address:
                    reply_text("Success! Address set. /help")

                return
        except (ValueError, IndexError) as e:
            print(e)
            error_response = """Address not set\!\n Hint: /setaddress _company street city state zip\_code _\n Note: _Use \- instead of space to seperate longer words\. e\.g\: "1st\-Avenue" instead of "1st Avenue"_"""

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

    def store_details(self) -> Connection:
        """
        Initializes and returns 'Connection' object to connect to database

        Returns
        -------
        Connection: object -- Return 'Connection' object
        """

        connect_db = Connection(
            host=config("HOST", cast=str),
            database=config("DATABASE", cast=str),
            user=config("USER", cast=str),
            password=config("PASSWORD", cast=str),
        )

        return connect_db

    def _remove_double_quotes(self, *args):
        """
        Parses strings with double quotes to single quote. Returns generator object if multple elements are passed in. Object must converted to 'List'

        Parameters
        ----------
        *args -- allows multple non keyword arguments.

        Returns
        ------
        Two data type. Can't say for now.

        Usage
        ----
        >>> self.name = "John Doe"
        >>>
        >>> name_newstring = self._remove_double_quotes(self.name)
        >>> name_newstring
        >>> # 'John Doe'
        >>>
        >>> self.company = "XYZ Ltd"
        >>> self.state = "FCT"
        >>> self.city = "FCT"
        >>> self.zip_code = "0000"
        >>>
        >>> address_newstring = self._remove_double_quotes(self.company,self.state,self.city,self.zip_code)
        >>> List(address_newstring)
        >>> # ['XYZ Ltd','FCT','FCT','0000']
        """

        values = []

        if len(args) == 1:
            return args[0].replace('"','')
        else:
            for n in args:
                values.append(n.replace('"',''))
            return values

