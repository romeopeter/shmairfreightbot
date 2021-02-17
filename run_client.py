from decouple import config
from robot.client.tclient import Client

if __name__ == "__main__":
    tclient = Client(token=config("TELEGRAM_API_TOKEN", cast=str))

    print("Starting Bot...")

    # Start client
    tclient.start_client()

    # Start client
    tclient.stop_client()
