import base64
import pandas as pd
import requests

import environ

env = environ.Env()
env.read_env()


class Parsers:
    def __init__(self):
        self.r = requests

    def partkom(self, article, maker_id):
        token = base64.b64encode(
            f"{env('PARTKOM_LOGIN')}:{env('PARTKOM_PASS')}"
            .encode('utf-8')).decode()
        base_url = env('PARTKOM_SEARCH')
        headers = {
            'Authorization': f'Basic {token}',
            'Accept': 'application/json',
            'Content-type': 'application/json',
        }

        params = {
            'number': article,
            'maker_id ': maker_id
        }

        result = self.r.get(base_url, headers=headers, params=params)

        if result.status_code != 200:
            return "Error"
        else:
            if len(result.json()) > 0:
                prices = pd.Series([p['price'] for p in result.json()])
                prices = prices.astype(float)
                return prices.mean().round(2)
            return "Нет данных"
