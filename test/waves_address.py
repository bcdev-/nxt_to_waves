from src.waves_address import waves_account_valid
from unittest import TestCase


class Test(TestCase):
    def test_waves_validate_account(self):
        self.assertEqual(waves_account_valid("3Mv61qe6egMSjRDZiiuvJDnf3Q1qW9tTZDB", True), True)
        self.assertEqual(waves_account_valid("3Mv51qe6egMSjRDZiiuvJDnf3Q1qW9tTZDB", True), False)
        self.assertEqual(waves_account_valid("3PAtGGSLnHJ3wuK8jWPvAA487pKamvQHyQw", False), True)
        self.assertEqual(waves_account_valid("3PAtGGSLnHJ3wuK9jWPvAA487pKamvQHyQw", False), False)
