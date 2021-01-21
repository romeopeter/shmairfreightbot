class CommandHandlerCallbacks:
    """
    Mix-in classes defines Telegram client commands as callback functions
    """

    def start_callback(self, update, context) -> None:
        """Processes '/start' command from user"""

        text = """Hey👋🏿 \n\nI can help you create and track your shipment\n\nYou can control me by sending these commands:\n\n*User Details*\n /setname \- set your name\n/setemail \- Set your email address\n/setphonenumber \- Set your phone number
        \n\n*Tracking Details*\n /setitemname \- set your name\n/settrackingnumber \- Set your email address\n/setcaurrier \- Set your phone number"""

        if update:
            update.message.reply_text(text=text, parse_mode="MarkdownV2")

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
