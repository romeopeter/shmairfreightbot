import easypost
from decouple import config


class Tracker:
    """Tracker object uses EasyPost service for tracking shipment"""

    def __init__(self, client_id) -> None:
        """Initializes 'Tracker' object"""
        self.client_id = client_id

        # Set API key
        easypost.api_key = self.client_id

    def track(self, tracking_id: str, carrier_name: str = None) -> dict:
        easypost.Tracker.create(tracking_code=tracking_id, carrier=carrier_name)


if __name__ == "__main__":
    try:
        tracker = Tracker(client_id=config("EASY_POST_API_TOKEN", cast=str))
        track = tracker.track("EZ4000000004")
        print(track)
    except Exception as e:
        print(e)
