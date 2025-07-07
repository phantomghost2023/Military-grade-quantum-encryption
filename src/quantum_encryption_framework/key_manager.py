from src.pqc import Dilithium

class KeyManager:
    def __init__(self, security_level=3):
        self.dilithium = Dilithium(security_level=security_level)

    def generate_keypair(self) -> tuple[bytes, bytes]:
        # Generates a Dilithium key pair
        public_key, private_key = self.dilithium.generate_keypair()
        return public_key, private_key

    def sign(self, message: bytes, private_key: bytes) -> bytes:
        # Signs a message using Dilithium
        signature = self.dilithium.sign(message, private_key)
        return signature

    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        # Verifies a message signature using Dilithium
        is_valid = self.dilithium.verify(message, signature, public_key)
        return is_valid
