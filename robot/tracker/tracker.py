import easypost
from decouple import config


class Tracker:
    """Tracker object uses EasyPost service for tracking shipment"""

    def __init__(self, client_id) -> None:
        """Initializes 'Tracker' object and sets API key"""
        easypost.api_key = client_id

    # ------Tracker API------

    def create_tracker(self, tracking_code: str, carrier: str = None) -> dict:
        """Create a tracker for package when `tracking_code` and `carrier` parameter values are passed in"""

        return easypost.Tracker.create(tracking_code=tracking_code, carrier=carrier)

    def retrieve_tracker(self, id: str) -> dict:
        return easypost.Tracker.retrieve(easypost_id=id)

    def retrieve_tracker_all(
        self,
        start_datetime: str,
        tracking_code: str,
        carrier: str,
        page_size: int = 2,
        end_datetime: str = None,
    ) -> dict:
        track_all = easypost.Tracker.all(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            page_size=page_size,
            tracking_code=tracking_code,
            carrier=carrier,
        )

        return track_all

    # -------Webhooks-------

    def create_webhook(self, url: str) -> dict:
        """Create a webhook. provide URL paramater to send notifications to"""
        return easypost.Webhook.create(ur=url)

    def retrieve_webhook(self, id: str) -> dict:
        """Retrieve a webhook by id"""
        return easypost.webhook.retrieve(id=id)

    def list_webhooks(self) -> dict:
        """Retrieve list of webhooks available to authenticated user"""
        pass


if __name__ == "__main__":
    try:
        tracker = Tracker(client_id=config("EASY_POST_API_TOKEN", cast=str))
        print("Crendential sent to tracker")

        print("Creating webhook url")
        tracker.create_webhook(url="https://b4f323e4c0b6.ngrok.io")
        print("Webhook created")

        tracker.create_tracker(tracking_code="EZ2000000002", carrier="UPS")
        print("Tracker created")
    except Exception as e:
        print(e)
