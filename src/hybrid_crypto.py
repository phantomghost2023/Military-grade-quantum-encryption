
"""
This module provides functionalities for hybrid cryptographic operations,
combining simulated QKD, Post-Quantum Cryptography (PQC), and classical symmetric encryption.
It includes hybrid key exchange, hybrid encryption/decryption, and data signing/verification.
"""

from src.qkd_simulation import BB84Simulator
from src.pqc import Kyber, Dilithium
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class HybridCrypto:
    """
    Manages hybrid cryptographic operations.
    """

    def __init__(self):
        self.kyber = Kyber()
        self.dilithium = Dilithium()
        self.qkd_simulator = BB84Simulator()

    def _derive_key(self, shared_secret: bytes, salt: bytes, info: bytes, key_length: int) -> bytes:
        """
        Derives a strong cryptographic key using HKDF.
        """
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=key_length,
            salt=salt,
            info=info,
            backend=default_backend()
        )
        return hkdf.derive(shared_secret)

    def hybrid_key_exchange(self) -> tuple[bytes, bytes, bytes, bytes]:
        """
        Performs a hybrid key exchange combining QKD simulation and Kyber KEM.

        Returns:
            tuple: (qkd_shared_key, kyber_ciphertext, kyber_encapsulated_secret, kyber_public_key)
                   qkd_shared_key is None if eavesdropping is detected.
        """
        # 1. Simulated QKD for initial shared secret and eavesdropping detection
        qkd_shared_key_str, eavesdropping_detected = self.qkd_simulator.run_bb84()

        if eavesdropping_detected:
            print("QKD Eavesdropping detected. Aborting key exchange.")
            return None, None, None, None

        qkd_shared_key = qkd_shared_key_str.encode('utf-8') # Convert str to bytes

        # 2. Kyber KEM for key encapsulation
        kyber_public_key, kyber_private_key = self.kyber.generate_keypair()
        kyber_ciphertext, kyber_encapsulated_secret = self.kyber.encapsulate(kyber_public_key)

        # In a real scenario, the encapsulated secret would be sent to the recipient
        # and decapsulated with their private key.
        # For this simulation, we'll return it directly for demonstration.

        return qkd_shared_key, kyber_ciphertext, kyber_encapsulated_secret, kyber_public_key

    def encrypt_data(self, data: bytes, session_key: bytes) -> tuple[bytes, bytes, bytes]:
        """
        Encrypts data using AES-256-GCM.

        Args:
            data (bytes): The plaintext data to encrypt.
            session_key (bytes): The symmetric session key (32 bytes for AES-256).

        Returns:
            tuple: (ciphertext, nonce, tag)
        """
        if len(session_key) != 32:
            raise ValueError("Session key must be 32 bytes for AES-256.")

        nonce = os.urandom(12)  # GCM recommended nonce size
        cipher = Cipher(algorithms.AES(session_key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        tag = encryptor.tag
        return ciphertext, nonce, tag

    def decrypt_data(self, ciphertext: bytes, nonce: bytes, tag: bytes, session_key: bytes) -> bytes:
        """
        Decrypts data using AES-256-GCM.

        Args:
            ciphertext (bytes): The encrypted data.
            nonce (bytes): The nonce used during encryption.
            tag (bytes): The authentication tag.
            session_key (bytes): The symmetric session key (32 bytes for AES-256).

        Returns:
            bytes: The decrypted plaintext data.
        """
        if len(session_key) != 32:
            raise ValueError("Session key must be 32 bytes for AES-256.")

        cipher = Cipher(algorithms.AES(session_key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext

    def sign_data(self, data: bytes, signing_key: bytes) -> bytes:
        """
        Signs data using Dilithium.

        Args:
            data (bytes): The data to sign.
            signing_key (bytes): The Dilithium signing key.

        Returns:
            bytes: The digital signature.
        """
        return self.dilithium.sign(signing_key, data)

    def verify_data_signature(self, data: bytes, signature: bytes, verification_key: bytes) -> bool:
        """
        Verifies a data signature using Dilithium.

        Args:
            data (bytes): The original data.
            signature (bytes): The digital signature.
            verification_key (bytes): The Dilithium verification key.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        return self.dilithium.verify(verification_key, data, signature)

if __name__ == "__main__":
    print("Running Hybrid Crypto Example:")
    hybrid_crypto = HybridCrypto()

    # --- Hybrid Key Exchange ---
    print("\n--- Hybrid Key Exchange ---")
    qkd_key, kyber_ct, kyber_ss, kyber_pk = hybrid_crypto.hybrid_key_exchange()

    if qkd_key is None:
        print("Hybrid key exchange failed due to QKD eavesdropping.")
    else:
        print(f"QKD Shared Key (first 10 bytes): {qkd_key[:10]}...")
        print(f"Kyber Ciphertext (first 10 bytes): {kyber_ct[:10]}...")
        print(f"Kyber Encapsulated Secret (first 10 bytes): {kyber_ss[:10]}...")

        # Simulate recipient decapsulating Kyber secret
        # In a real scenario, the recipient would use their private key to decapsulate kyber_ct
        # For this example, we use the returned kyber_ss directly
        
        # Derive a final session key from both QKD and Kyber secrets
        # For simplicity, we'll concatenate and hash them. In practice, use HKDF with proper salt/info.
        combined_secret = qkd_key + kyber_ss
        salt = os.urandom(16)
        info = b"hybrid-session-key"
        session_key = hybrid_crypto._derive_key(combined_secret, salt, info, 32) # 32 bytes for AES-256
        print(f"Derived Session Key (first 10 bytes): {session_key[:10]}...")

        # --- Hybrid Encryption and Decryption ---
        print("\n--- Hybrid Encryption and Decryption ---")
        original_data = b"This is a super secret message to be encrypted with hybrid cryptography."
        print(f"Original Data: {original_data}")

        ciphertext, nonce, tag = hybrid_crypto.encrypt_data(original_data, session_key)
        print(f"Ciphertext (first 10 bytes): {ciphertext[:10]}...")
        print(f"Nonce (hex): {nonce.hex()}")
        print(f"Tag (hex): {tag.hex()}")

        try:
            decrypted_data = hybrid_crypto.decrypt_data(ciphertext, nonce, tag, session_key)
            print(f"Decrypted Data: {decrypted_data}")
            assert original_data == decrypted_data
            print("Encryption and Decryption successful!")
        except Exception as e:
            print(f"Decryption failed: {e}")

        # --- Data Signing and Verification ---
        print("\n--- Data Signing and Verification ---")
        dilithium_vk, dilithium_sk = hybrid_crypto.dilithium.generate_keypair()
        data_to_sign = b"Important document content."
        print(f"Data to Sign: {data_to_sign}")

        signature = hybrid_crypto.sign_data(data_to_sign, dilithium_sk)
        print(f"Signature (first 10 bytes): {signature[:10]}...")

        is_valid = hybrid_crypto.verify_data_signature(data_to_sign, signature, dilithium_vk)
        print(f"Signature Valid: {is_valid}")

        # Test with tampered data
        tampered_data = b"Important document content. TAMPERED!"
        is_valid_tampered = hybrid_crypto.verify_data_signature(tampered_data, signature, dilithium_vk)
        print(f"Signature Valid (Tampered Data): {is_valid_tampered}")

        assert is_valid is True
        assert is_valid_tampered is False
        print("Signing and Verification successful!")
