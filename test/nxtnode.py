from unittest import TestCase
from src.settings import Settings
from src import nxtnode


class Test(TestCase):
    def test_get_height(self):
        settings = Settings()
        self.assertGreaterEqual(nxtnode.get_height(settings), 1180285)

    def test_get_blockchain_transactions(self):
        settings = Settings()
        tx = nxtnode.get_blockchain_deposits(settings, "NXT-QQ3T-92RV-GGHG-39TWE", 1, 1181961-1)
        self.assertEqual(len(tx), 1)
        tx = nxtnode.get_blockchain_deposits(settings, "NXT-QQ3T-92RV-GGHG-39TWE", 1, 1181962-1)
        self.assertEqual(len(tx), 0)

        height = nxtnode.get_height(settings)
        tx = nxtnode.get_blockchain_deposits(settings, "NXT-QQ3T-92RV-GGHG-39TWE", height - 1181961, 1181961-1)
        self.assertEqual(len(tx), 0)
        tx = nxtnode.get_blockchain_deposits(settings, "NXT-QQ3T-92RV-GGHG-39TWE", height - 1181962, 1181961-1)
        self.assertEqual(len(tx), 1)

        tx = nxtnode.get_blockchain_deposits(settings, "NXT-QQ3T-92RV-GGHG-39TWE", 1, 1181891-1)
        self.assertEqual(len(tx), 1)
        self.assertEqual(tx[0].message, 'yay! Another message!')
        tx = nxtnode.get_blockchain_deposits(settings, "NXT-QQ3T-92RV-GGHG-39TWE", 1, 1181890-1)
        self.assertEqual(len(tx), 2)

    def test_get_account(self):
        settings = Settings()
        self.assertEqual(nxtnode.get_account(settings, "aaa"), "NXT-PLR6-Z7K9-KJQ9-GWQ6R")
