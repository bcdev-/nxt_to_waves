from pyblake2 import blake2b
from sha3 import keccak_256 as sha3_256
from base58 import b58decode


base58_waves_account_length = 35
raw_waves_account_length = 26


class BlockchainParameters:
    def __init__(self, testnet):
        self.testnet = testnet
        self.AddressVersion = b'\x01'
        self.ChainId = b'T' if testnet else b'W'
        self.HashLength = 20
        self.ChecksumLength = 4


def waves_account_valid(account, testnet):
    def blake2b256_keccak256(data):
        b = blake2b(digest_size=32)
        b.update(data)
        return sha3_256(b.digest()).digest()

    address_version = b'\x01'
    chain_id = b'T' if testnet else b'W'

    try:
        if len(account) != base58_waves_account_length:
            return False
        decoded = b58decode(account)
        if len(decoded) != raw_waves_account_length:
            return False
        if decoded[0:1] != address_version or decoded[1:2] != chain_id:
            return False
        public_key_hash = decoded[0:22]
        checksum = blake2b256_keccak256(public_key_hash)[:4]

        if checksum != decoded[22:26]:
            return False

        return True
    except Exception:
        return False
