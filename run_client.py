from decouple import config
from robot.client.tclient import Client

if __name__ == "__main__":
    tclient = Client(token=config("TELEGRAM_API_TOKEN", cast=str))

    # Start client
    tclient.start_client()
    print("Bot's started...")

    # Stop client
    tclient.stop_client()
