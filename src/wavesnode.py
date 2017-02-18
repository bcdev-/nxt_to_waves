from requests import get, post
from .settings import waves_api_url, waves_api_key, waves_fee, waves_address
from unittest import TestCase
import json
import logging

logger = logging.getLogger(__name__)


def get_new_deposit_account():
    url = waves_api_url + "/addresses"
    headers = {'api_key': waves_api_key}
    r = post(url, headers=headers)
    return r.json()['address']


def get_transactions_for_account(account):
    url = waves_api_url + "/transactions/address/%s/limit/1000" % account
    headers = {'api_key': waves_api_key}
    r = get(url, headers=headers)
    return r.json()[0]


def get_current_height():
    url = waves_api_url + "/blocks/height"
    r = get(url)
    return r.json()["height"]


def get_block(height):
    url = waves_api_url + "/blocks/at/%d" % height
    r = get(url)
    return r.json()


def get_transactions_for_block(height):
    return get_block(height)["transactions"]


def send_currency(currency: str, recipient: str, amount: int) -> str:
    url = waves_api_url + "/assets/transfer"
    headers = {'api_key': waves_api_key}
    data = {
      "recipient": recipient,
      "assetId": currency,
      "feeAsset": None,
      "amount": amount,
      "attachment": "",
      "sender": waves_address,
      "fee": waves_fee
    }
    print(json.dumps(data))
    r = post(url, headers=headers, data=json.dumps(data))
    print(r.json())
    return r.json()['id']


def get_balances(address: str) -> dict:
    url = waves_api_url + "/assets/balance/%s" % address
    r = get(url)
    print(r.json())
    assert(r.json()['address'] == address)

    balances = dict()
    for asset in r.json()['balances']:
        balances[asset['assetId']] = asset['balance']

    return balances


def get_currency_balance(address: str, currency: str) -> int:
    balances = get_balances(address)
    if currency in balances:
        return balances[currency]
    return 0


def get_waves_balance(address: str) -> int:
    url = waves_api_url + "/addresses/balance/%s" % address
    r = get(url)
    return r.json()['balance']


def get_transaction(transaction_id: str) -> dict:
    url = waves_api_url + "/transactions/info/%s" % transaction_id
    r = get(url)
    return r.json()


class TestNode(TestCase):
    def test_new_deposit_account(self):
        a1 = get_new_deposit_account()
        a2 = get_new_deposit_account()
        a3 = get_new_deposit_account()
        self.assertNotEqual(a1, a2)
        self.assertNotEqual(a2, a3)
