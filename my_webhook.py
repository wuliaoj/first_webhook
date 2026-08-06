import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from weather import get_weather_message

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_message() -> None:
    if not WEBHOOK_URL:
        raise ValueError("沒有設定 DISCORD_WEBHOOK_URL")

    taiwan_time = datetime.now(
        ZoneInfo("Asia/Taipei")
    ).strftime("%Y-%m-%d %H:%M:%S")

    message = get_weather_massage()

    response = requests.post(
        WEBHOOK_URL,
        json={"content": message},
        timeout=15,
    )

    response.raise_for_status()
    print(f"訊息發送成功，台灣時間：{taiwan_time}")


if __name__ == "__main__":
    send_discord_message()
