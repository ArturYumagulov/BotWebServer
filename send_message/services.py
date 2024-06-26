import requests
import environ

env = environ.Env()
token = env.str("BOT_TOKEN")


def send_message_to_telegram(addresses_list, message):

    for address in addresses_list:
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={address}&text={message}'
        result = requests.get(url).json()
        if result['ok']:
            return True
        else:
            return False
