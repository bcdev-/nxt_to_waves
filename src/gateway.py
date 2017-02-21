import time
from .settings import Settings
from .nxtnode import get_blockchain_deposits, get_account, refund_asset_transfer
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class Gateway:
    def __init__(self):
        self.settings = Settings()

    def new_nxt_deposits(self):
        nxt_address = get_account(self.settings, self.settings.config["nxt_secret_phrase"])
        nxt_confirmations = self.settings.config["nxt_confirmations"]
        last_block = self.settings.config["last_processed_nxt_block"]
        tx_list = get_blockchain_deposits(self.settings, nxt_address, nxt_confirmations, last_block)
        forward, refund = [], []
        for tx in tx_list:
            if tx.is_valid(self.settings):
                forward.append(tx)
            else:
                refund.append(tx)
        newest_block = max(tx_list, key=lambda p: p.height).height if len(tx_list) > 0 else last_block
        return forward, refund, newest_block

    def tick(self):
        forward, refund, newest_block = self.new_nxt_deposits()

        # Update last known NXT block number
        # This is important so that we don't send assets twice
        if len(forward) > 0 or len(refund) > 0:
            self.settings.config['last_processed_nxt_block'] = newest_block
            self.settings.update()

        for tx in forward:
            logger.info("Forwarding transaction: " + str(tx))
            # TODO

        for tx in refund:
            logger.info("Refunding transaction: " + str(tx))
            logger.info(refund_asset_transfer(self.settings, tx))

    def start(self):
        logger.info("Starting NXT->Waves Gateway")
        while True:
            self.tick()
            time.sleep(1)
