from flask import Flask, request
import easypost
from decouple import config

app = Flask(__name__)


@app.route("/easypost-webhook", methods=["GET", "POST"])
def process_webhook():

    """Check if wehbook is about tracker event
    If key of 'object' has 'Event' and key 'description' has 'tracker.updated' then it is a tracker event"""

    # Check data returned before proceeding
    webhook_request = request.get_json()

    if (
        webhook_request["object"] == "Event"
        and webhook_request["description"] == "tracker.updated"
    ):
        print(webhook_request)

        event = easypost.Event.recieve(request.data)
        tracker = event.result

        # Check delivery status on package and update customer accordingly
        message = ""
        if tracker.status == "delivered":
            message = +"Your package has been delivered\n"
        else:
            for tracking_details in tracker.tracking_details:
                if tracking_details.status == tracker.status:
                    message = +(
                        f"{tracker.carrier} says: {tracking_details.message} in {tracking_details.tracking_location.city}, {tracking_details.tracking_location.country}"
                    )
                    break
        return "Update on package sent to customer via SMS"
    else:
        return "Request is not a Tracker event. Waiting event..."
