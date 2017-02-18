from requests import get, post
from src.settings import Settings
import json
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
        return "Sender: %s ID: %s AssetID: %d AmountQNT: %d Height: %d Confirmations: %d Message %s" %\
               (self.sender, self.tx_id, self.asset_id, self.quantity_qnt, self.height, self.confirmations, self.message)


def get_blockchain_transactions(settings, account, confirmations, last_known_block):
    url = settings.config["nxt_api_url"] +\
          "/nxt?requestType=getBlockchainTransactions&account=%s&numberOfConfirmations=%d" % \
          (account, confirmations)
    r = get(url)

    incoming = []
    for tx in r.json()["transactions"]:
        if tx["height"] < last_known_block:
            continue
        if tx["type"] == 2:  # Asset transfer
            if tx["recipientRS"] == settings.config["nxt_address"]:
                message = ""
                if "message" in tx["attachment"]:
                    message = tx["attachment"]["message"]
                elif "encryptedMessage" in tx["attachment"]:
                    message = decrypt_from(settings, tx["senderRS"], tx["attachment"]["encryptedMessage"]["data"], tx["attachment"]["encryptedMessage"]["nonce"])
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

