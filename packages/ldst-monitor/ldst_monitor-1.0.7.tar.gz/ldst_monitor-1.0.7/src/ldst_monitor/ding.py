import os
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests


class Ding:
    def __init__(self, token="", sign=""):
        self.token = token
        if token == "":
            self.token = os.getenv("DING_TOKEN")
        self.sign = sign
        if sign == "":
            self.sign = os.getenv("DING_SIGN")

    def _sign(self):
        timestamp = str(round(time.time() * 1000))
        secret = self.sign
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return f'{self.token}&timestamp={timestamp}&sign={sign}'

    #
    def send_text(self, message):
        url = self._sign()
        print(message)
        data = {
            'msgtype': 'markdown',
            "markdown": {
                "title": "Server notification",
                "text": message
            }
        }
        response = requests.post(url, json=data, headers={"Content-Type": "application/json;charset=utf-8"})
        return response.status_code == 200


if __name__ == "__main__":
    ding = Ding()
    ding.send_text("test.")
