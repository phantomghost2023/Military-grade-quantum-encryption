"""
This module provides an interface for Post-Quantum Cryptography (PQC) implementations,
focusing on NIST-standardized algorithms for Key Encapsulation Mechanisms (KEMs)
and Digital Signatures.
It leverages the `quantcrypt` library to provide Kyber for KEM and Dilithium for Digital Signatures.
"""

from quantcrypt import kem, dss


class Kyber:
    """Implements the Kyber Key Encapsulation Mechanism (KEM) using quantcrypt."""
    def __init__(self, security_level: str = "512") -> None:
        if security_level not in ["512", "768", "1024"]:
            raise ValueError(
                "Invalid Kyber security level. Choose from '512', '768', '1024'."
            )
        self.security_level = security_level
        self.kem_instance = getattr(kem, f"MLKEM_{security_level}")()

    def generate_keypair(self) -> tuple[bytes, bytes]:
        """
        Generate a Kyber key pair.
        
        Returns:
            tuple: A tuple containing (public_key, private_key)
        """
        pk, sk = self.kem_instance.keygen()
        return pk, sk

    def encapsulate(self, public_key: bytes) -> tuple[bytes, bytes]:
        """
        Encapsulate a shared secret using the recipient's public key.
        
        Args:
            public_key: The recipient's public key
            
        Returns:
            tuple: A tuple containing (ciphertext, shared_secret)
        """
        ct, ss = self.kem_instance.encaps(public_key)
        return ct, ss

    def decapsulate(self, private_key: bytes, ciphertext: bytes) -> bytes:
        """
        Decapsulate a ciphertext to obtain the shared secret.
        
        Args:
            private_key: The private key for decapsulation
            ciphertext: The ciphertext to decapsulate
            
        Returns:
            bytes: The shared secret
        """
        ss = self.kem_instance.decaps(secret_key=private_key, cipher_text=ciphertext)
        return ss


class Dilithium:
    """Implements the Dilithium Digital Signature Scheme (DSS) using quantcrypt."""
    def __init__(self, security_level: str = "2") -> None:
        if security_level not in ["44", "65", "87"]:
            raise ValueError(
                "Invalid Dilithium security level. Choose from '44', '65', '87'.")
        self.security_level = security_level
        self.dss_instance = getattr(dss, f"MLDSA_{security_level}")()

    def generate_keypair(self):
        """
        Generate a Dilithium key pair.
        
        Returns:
            tuple: A tuple containing (verification_key, signing_key)
        """
        vk, sk = self.dss_instance.keygen()
        return vk, sk

    def sign(self, signing_key: bytes, message: bytes | str) -> bytes:
        """
        Sign a message using Dilithium.
        
        Args:
            signing_key: The secret signing key
            message: The message to sign (bytes or str)
            
        Returns:
            bytes: The digital signature
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        sig = self.dss_instance.sign(secret_key=signing_key, message=message)
        return sig

    def verify(self, verification_key: bytes, message: bytes | str, signature: bytes) -> bool:
        """
        Verify a digital signature using Dilithium.
        
        Args:
            verification_key: The public verification key
            message: The message to verify (bytes or str)
            signature: The signature to verify
            
        Returns:
            bool: True if signature is valid, False otherwise
            
        Note:
            The `raises=False` parameter is used to suppress DSSVerifyFailedError
            when verification fails, allowing the method to return False instead.
            This matches the expected behavior in our test cases.
        """
        is_valid = self.dss_instance.verify(
            public_key=verification_key, message=message, signature=signature, raises=False
        )
        return is_valid
