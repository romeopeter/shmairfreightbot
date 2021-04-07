from flask import Flask, request

import easypost
from decouple import config

app = Flask(__name__)


@app.route("/easypost-webhook", methods=["GET"])
def process_webhook():
    """Recieve and process tracker webhook alerts"""

    # Check if webhook is a tracker event before proceeding.
    webhook_request = request.get_json()

    if (
        webhook_request["object"] == "Event"
        and webhook_request["description"] == "tracker.updated"
    ):
        print(webhook_request)

        event = easypost.Event.recieve(request.data)
        tracker = event.result

        # Checks delivery status and updates customer via SMS.
        message = ""
        if tracker.status == "delivered":
            message += f"Your package has been delivered\nPackage signed by {tracker.signed_by}"
        elif tracker.status == "in_transit":
            for tracking_details in tracker.details:
                if tracking_detail.messsage == "ARRIVAL SCAN":
                    message = (
                        +f"Hi,\n Your packag has arrived in {tracking_details.tracking_location.city}\n\n. Package signed by {tracker.signed_by}\n\n Click the link for live tracking: {tracker.public_url}"
                    )
                    break
        else:
            for tracking_details in tracker.tracking_details:
                if tracking_details.status == tracker.status:
                    message += f"{tracker.carrier} says: {tracking_details.message} in {tracking_details.tracking_location.city}, {tracking_details.tracking_location.country}\nClick the link for live preview tracking: {tracker.public_url}"
                    break
        return "Update on package sent to customer via SMS"
    else:
        return "Request is not a Tracker event. Waiting event..."


if __name__ == "__main__":
    app.run(debug=True, port=1234)
