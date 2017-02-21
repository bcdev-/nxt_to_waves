from requests import get, post
from unittest import TestCase
import json
import logging
from base58 import b58encode

logger = logging.getLogger(__name__)


def send_currency(settings, currency: str, recipient: str, amount: int, attachment: str) -> str:
    url = settings.config['waves_api_url'] + "/assets/transfer"
    headers = {'api_key': settings.config['waves_api_key']}
    data = {
      "recipient": recipient,
      "assetId": currency,
      "feeAsset": None,
      "amount": amount,
      "attachment": b58encode(attachment.encode('utf-8')),
      "sender": settings.config['waves_address'],
      "fee": settings.config['waves_fee']
    }
    print(json.dumps(data))
    print(url)
    r = post(url, headers=headers, data=json.dumps(data))
    print(r.json())
    return r.json()['id']

