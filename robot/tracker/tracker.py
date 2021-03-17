import easypost
from decouple import config

from . import webhook_server


class Tracker:
    """Tracker object uses EasyPost service for tracking shipment"""

    def __init__(self, client_id) -> None:
        """Initializes 'Tracker' object and sets API key"""
        easypost.api_key = client_id

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


if __name__ == "__main__":
    try:
        tracker = Tracker(client_id=config("EASY_POST_API_TOKEN", cast=str))
        # retrieve_tracker = tracker.retrieve_tracker(
        #     id="trk_04b2ae3786b44329a2b62a0eea9279b8"
        # )
    except Exception as e:
        print(e)

# NOTE: Run server from within 'tracker.py'. Idealy, tracker is created before running server.
