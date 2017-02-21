from requests import get, post
from .waves_address import waves_account_valid
import logging

logger = logging.getLogger(__name__)


def get_height(settings):
    url = settings.config["nxt_api_url"] + "/nxt?requestType=getBlockchainStatus"
    r = get(url)
    return r.json()["numberOfBlocks"]


class NXTAssetTransfer:
    def __init__(self, sender, transaction, asset, quantity_qnt, height, confirmations, message):
        self.sender = sender
        self.tx_id = transaction
        self.asset_id = asset
        self.quantity_qnt = quantity_qnt
        self.height = height
        self.confirmations = confirmations
        self.message = message

    def __repr__(self):
        return "Sender: %s ID: %s AssetID: %d AmountQNT: %d Height: %d Confirmations: %d Message: %s" %\
               (self.sender, self.tx_id, self.asset_id, self.quantity_qnt, self.height, self.confirmations, self.message)

    def is_valid(self, settings):
        return waves_account_valid(self.message, settings.config['waves_is_testnet']) and\
               str(self.asset_id) in settings.config['asset_associacions'].keys()


def get_blockchain_deposits(settings, account, confirmations, last_known_block) -> NXTAssetTransfer:
    url = settings.config["nxt_api_url"] +\
          "/nxt?requestType=getBlockchainTransactions&account=%s&numberOfConfirmations=%d" % \
          (account, confirmations)
    r = get(url)

    incoming = []
    for tx in r.json()["transactions"]:
        if tx["height"] <= last_known_block:
            continue
        if tx["type"] == 2:  # Asset transfer
            if tx["recipientRS"] == account:
                message = ""
                if "message" in tx["attachment"]:
                    message = tx["attachment"]["message"]
                elif "encryptedMessage" in tx["attachment"]:
                    message = decrypt_from(settings, tx["senderRS"], tx["attachment"]["encryptedMessage"]["data"], tx["attachment"]["encryptedMessage"]["nonce"])
                message = message.strip()
                logger.info("New asset transfer from %s - txid %s - asset %d, amount %d, message %s" % (tx["senderRS"], tx["transaction"], int(tx["attachment"]["asset"]), int(tx["attachment"]["quantityQNT"]), message))
                incoming.append(NXTAssetTransfer(tx["senderRS"], tx["transaction"], int(tx["attachment"]["asset"]), int(tx["attachment"]["quantityQNT"]), tx["height"], tx["confirmations"], message))

    return incoming


def decrypt_from(settings, sender, data, nonce):
    url = settings.config["nxt_api_url"] + "/nxt?requestType=decryptFrom&account=%s&data=%s&nonce=%s&secretPhrase=%s" % (sender, data, nonce, settings.config["nxt_secret_phrase"])
    r = get(url)
    data = r.json()

    if "decryptedMessage" not in data:
        raise KeyError(data["errorDescription"])
    else:
        return data["decryptedMessage"]


def get_account(settings, secret_phrase):
    url = settings.config["nxt_api_url"] + "/nxt?requestType=getAccountId&secretPhrase=%s" % (secret_phrase)
    r = get(url)
    data = r.json()
    return data["accountRS"]


def refund_asset_transfer(settings, asset_transfer: NXTAssetTransfer):
    url = settings.config["nxt_api_url"] + "/nxt?requestType=transferAsset"
    data = {"requestType": "transferAsset",
            "recipient": asset_transfer.sender,
            "asset": asset_transfer.asset_id,
            "quantityQNT": asset_transfer.quantity_qnt,
            "secretPhrase": settings.config["nxt_secret_phrase"],
            "deadline": 1000,
            "feeNQT": 100000000}
    r = post(url, data=data)
    data = r.json()
    return data
