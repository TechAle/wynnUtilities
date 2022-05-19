import requests


def sendMessageWebhook(message, url, ping=False, name="WynnStalker"):
    data = {
        "usarname": name,
        "content": ("@everyone" if ping else "") + message
    }

    requests.post(url, json=data)
