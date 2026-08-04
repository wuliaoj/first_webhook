import os

import requests


WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
MESSAGE = "上班了 可以摸魚了"


def send_discord_message() -> None:
    if not WEBHOOK_URL:
        raise ValueError("沒有設定 DISCORD_WEBHOOK_URL")

    response = requests.post(
        WEBHOOK_URL,
        json={"content": MESSAGE},
        timeout=15,
    )

    response.raise_for_status()
    print("訊息發送成功")


if __name__ == "__main__":
    send_discord_message()