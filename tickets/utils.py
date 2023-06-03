import requests
from django.conf import settings


def telegram_msg(message):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage?chat_id={settings.TELEGRAM_GROUP_ID}&text={message}"
    print(requests.get(url).json()) # this sends the message

def telegram_image(image):
    apiToken = settings.TELEGRAM_TOKEN
    chatID = settings.TELEGRAM_GROUP_ID
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendPhoto'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'photo': image})
        print(response.text)
    except Exception as e:
        print(e)
