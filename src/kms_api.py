"""This module provides the Key Management System (KMS) API for generating, storing,distributing, rotating, and revoking cryptographic keys."""
import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import time
from src.pqc import Kyber, Dilithium
from src.hybrid_crypto import HybridCrypto


class KMS:
    """
    Manages cryptographic keys for the framework.
    """
    def __init__(self, master_password: str = "supersecretpassword"):
        self.master_password = master_password.encode('utf-8')
        self.salt = b'\x8d\x9b\x1c\x0f\x1e\x0c\x1b\x0a\x1d\x0b\x1f\x0d\x1a\x0e\x19\x09' # Fixed salt for simplicity in prototype
        self.fernet = self._derive_fernet_key()
        self.hybrid_crypto = HybridCrypto()
        self.key_store_path = "./kms_key_store.json"
        self._load_key_store()

    def _derive_fernet_key(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_password))
        return Fernet(key)

    def _load_key_store(self):
        if os.path.exists(self.key_store_path):
            with open(self.key_store_path, 'r') as f:
                encrypted_data = f.read()
            try:
                decrypted_data = self.fernet.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')
                self.key_store = json.loads(decrypted_data)
            except Exception as e:
                print(f"Error loading key store: {e}. Initializing empty key store.")
                self.key_store = {}
        else:
            self.key_store = {}

    def _save_key_store(self):
        encrypted_data = self.fernet.encrypt(json.dumps(self.key_store).encode('utf-8'))
        with open(self.key_store_path, 'w') as f:
            f.write(encrypted_data.decode('utf-8'))

    def generate_pqc_key_pair(self, key_id: str, algorithm: str = "Kyber") -> dict:
        """
        Generates and stores a PQC key pair.
        """
        if algorithm == "Kyber":
            pqc_instance = Kyber()
        elif algorithm == "Dilithium":
            pqc_instance = Dilithium()
        else:
            raise ValueError("Unsupported PQC algorithm.")
        public_key, private_key = pqc_instance.generate_keypair()
        self.key_store[key_id] = {
            "type": "PQC",
            "algorithm": algorithm,
            "public_key": base64.b64encode(public_key).decode('utf-8'),
            "private_key": base64.b64encode(private_key).decode('utf-8'),
            "status": "active",
            "created_at": time.time(),
            "last_rotated_at": time.time()
        }
        self._save_key_store()
        return self.key_store[key_id]

    def generate_symmetric_key(self, key_id: str) -> dict:
        """
        Generates and stores a symmetric key.
        """
        symmetric_key = os.urandom(32) # AES-256 key
        self.key_store[key_id] = {
            "type": "Symmetric",
            "algorithm": "AES-256",
            "key": base64.b64encode(symmetric_key).decode('utf-8'),
            "status": "active",
            "created_at": time.time(),
            "last_rotated_at": time.time()
        }
        self._save_key_store()
        return self.key_store[key_id]

    def get_key(self, key_id: str) -> dict | None:
        """
        Retrieves a key by its ID.
        """
        return self.key_store.get(key_id)

    def rotate_key(self, key_id: str) -> str:
        """
        Rotates an existing key. The old key is marked as inactive, and a new key is generated.
        Returns the ID of the new key.
        """
        old_key = self.get_key(key_id)
        if not old_key:
            raise ValueError(f"Key with ID '{key_id}' not found for rotation.")

        old_key["status"] = "inactive"
        new_key_id = f"{key_id}_rotated_{int(time.time())}"

        if old_key["type"] == "PQC":
            self.generate_pqc_key_pair(new_key_id, old_key["algorithm"])
        elif old_key["type"] == "Symmetric":
            self.generate_symmetric_key(new_key_id)
        else:
            raise ValueError("Unsupported key type for rotation.")

        self._save_key_store()
        return new_key_id

    def revoke_key(self, key_id: str) -> None:
        """
        Revokes a key by marking it as revoked.
        """
        key = self.get_key(key_id)
        if not key:
            raise ValueError(f"Key with ID '{key_id}' not found for revocation.")
        key["status"] = "revoked"
        self._save_key_store()

    def perform_hybrid_key_exchange_with_kms(self, recipient_public_key: bytes) -> tuple[bytes, bytes, bytes]:
        """
        Performs a hybrid key exchange using KMS-managed keys.
        This simulates the KMS acting as one party in the key exchange.
        """
        # In a real scenario, the KMS would manage its own key pairs and perform
        # the key exchange using its internal PQC capabilities.
        # For this prototype, we'll simulate it by generating a new Kyber key pair
        # and using the provided recipient_public_key.

        # 1. KMS generates its own ephemeral Kyber key pair
        kms_kyber = Kyber()
        kms_pk, kms_sk = kms_kyber.generate_keypair()

        # 2. KMS encapsulates a shared secret using the recipient's public key
        ciphertext, shared_secret = kms_kyber.encapsulate(recipient_public_key)

        # In a real system, the KMS would securely store/manage the shared_secret
        # and potentially derive a session key from it.
        # For this example, we return the shared_secret, ciphertext, and KMS's public key
        # (which would be sent to the recipient for decapsulation).
        return shared_secret, ciphertext, kms_pk

    def encrypt_data_with_kms_key(self, key_id: str, data: bytes) -> tuple[bytes, bytes, bytes]:
        """
        Encrypts data using a symmetric key managed by the KMS.
        """
        key_info = self.get_key(key_id)
        if not key_info or key_info["type"] != "Symmetric" or key_info["status"] != "active":
            raise ValueError(f"Invalid or inactive symmetric key with ID '{key_id}'.")

        symmetric_key = base64.b64decode(key_info["key"])
        return self.hybrid_crypto.encrypt_data(data, symmetric_key)

    def decrypt_data_with_kms_key(self, key_id: str, ciphertext: bytes, nonce: bytes, tag: bytes) -> bytes:
        """
        Decrypts data using a symmetric key managed by the KMS.
        """
        key_info = self.get_key(key_id)
        if not key_info or key_info["type"] != "Symmetric" or key_info["status"] != "active":
            raise ValueError(f"Invalid or inactive symmetric key with ID '{key_id}'.")

        symmetric_key = base64.b64decode(key_info["key"])
        return self.hybrid_crypto.decrypt_data(ciphertext, nonce, tag, symmetric_key)

    def sign_data_with_kms_key(self, key_id: str, data: bytes) -> bytes:
        """
        Signs data using a PQC signing key managed by the KMS.
        """
        key_info = self.get_key(key_id)
        if not key_info or key_info["type"] != "PQC" or key_info["status"] != "active":
            raise ValueError(f"Invalid or inactive PQC key with ID '{key_id}'.")

        private_key = base64.b64decode(key_info["private_key"])
        return self.hybrid_crypto.sign_data(data, private_key)

    def verify_data_with_kms_key(self, key_id: str, data: bytes, signature: bytes) -> bool:
        """
        Verifies data using a PQC verification key managed by the KMS.
        """
        key_info = self.get_key(key_id)
        if not key_info or key_info["type"] != "PQC" or key_info["status"] != "active":
            raise ValueError(f"Invalid or inactive PQC key with ID '{key_id}'.")

        public_key = base64.b64decode(key_info["public_key"])
        return self.hybrid_crypto.verify_data_signature(data, signature, public_key)
if __name__ == "__main__":
    print("Running KMS Example:")
    kms = KMS(master_password="mysecurepassword")

    # Generate PQC Key Pair
    print("\n--- Generating PQC Key Pair ---")
    pqc_key_id = "my_kyber_key"
    pqc_keys = kms.generate_pqc_key_pair(pqc_key_id, "Kyber")
    print(f"Generated Kyber Key Pair for {pqc_key_id}: Public Key (first 10 bytes) {pqc_keys["public_key"][:10]}...")
    retrieved_pqc_key = kms.get_key(pqc_key_id)
    print(f"Retrieved Kyber Key Status: {retrieved_pqc_key["status"]}")

    # Generate Symmetric Key
    print("\n--- Generating Symmetric Key ---")
    sym_key_id = "my_aes_key"
    symmetric_key = kms.generate_symmetric_key(sym_key_id)
    print(f"Generated Symmetric Key for {sym_key_id}: {symmetric_key["key"][:10]}...")
    retrieved_sym_key = kms.get_key(sym_key_id)
    print(f"Retrieved Symmetric Key Status: {retrieved_sym_key["status"]}")

    # Rotate PQC Key
    print("\n--- Rotating PQC Key ---")
    new_pqc_key_id = kms.rotate_key(pqc_key_id)
    print(f"Rotated {pqc_key_id} to new ID: {new_pqc_key_id}")
    old_pqc_key_status = kms.get_key(pqc_key_id)["status"]
    new_pqc_key_status = kms.get_key(new_pqc_key_id)["status"]
    print(f"Old Kyber Key Status ({pqc_key_id}): {old_pqc_key_status}")
    print(f"New Kyber Key Status ({new_pqc_key_id}): {new_pqc_key_status}")

    # Revoke Symmetric Key
    print("\n--- Revoking Symmetric Key ---")
    kms.revoke_key(sym_key_id)
    revoked_sym_key_status = kms.get_key(sym_key_id)["status"]
    print(f"Revoked Symmetric Key Status ({sym_key_id}): {revoked_sym_key_status}")

    # --- Performing Hybrid Key Exchange with KMS ---
    print("\n--- Performing Hybrid Key Exchange with KMS ---")
    # Simulate a recipient generating a Kyber key pair
    recipient_kyber = Kyber()
    recipient_public_key, _ = recipient_kyber.generate_keypair()

    try:
        shared_secret_kms, ciphertext_kms, kms_pk_exchange = kms.perform_hybrid_key_exchange_with_kms(recipient_public_key)
        print(f"KMS Shared Secret (first 10 bytes): {shared_secret_kms[:10]}...")
        print(f"KMS Ciphertext (first 10 bytes): {ciphertext_kms[:10]}...")
        print(f"KMS Public Key (first 10 bytes): {kms_pk_exchange[:10]}...")
    except Exception as e:
        print(f"Hybrid Key Exchange with KMS failed: {e}")

    # Clean up (optional)
    # os.remove("kms_key_store.json")
    # print("Cleaned up kms_key_store.json")