"""This module provides a hybrid Quantum Key Distribution (QKD) API for secure communication."""

from src.hybrid_crypto import HybridCrypto
import os

_hybrid_crypto_instance = HybridCrypto()

def simulate_qkd_key_exchange():
    """
    Simulates a QKD key exchange and returns the QKD-derived shared key
    and a boolean indicating if eavesdropping was detected.
    """
    qkd_shared_key_str, eavesdropping_detected = _hybrid_crypto_instance.qkd_simulator.run_bb84()
    return qkd_shared_key_str, eavesdropping_detected

def perform_hybrid_key_exchange():
    """
    Performs a full hybrid key exchange, combining QKD simulation and Kyber KEM.
    Returns the QKD-derived key, Kyber ciphertext, Kyber encapsulated secret,
    and Kyber public key. Returns None for keys if eavesdropping is detected.
    """
    return _hybrid_crypto_instance.hybrid_key_exchange()

def encrypt_data_hybrid(data: bytes, session_key: bytes) -> tuple[bytes, bytes, bytes]:
    """
    Encrypts data using the hybrid encryption scheme (AES-256-GCM).
    Args:
        data (bytes): The plaintext data to encrypt.
        session_key (bytes): The symmetric session key (32 bytes for AES-256).
    Returns:
        tuple: (ciphertext, nonce, tag)
    """
    return _hybrid_crypto_instance.encrypt_data(data, session_key)

def decrypt_data_hybrid(ciphertext: bytes, nonce: bytes, tag: bytes, session_key: bytes) -> bytes:
    """
    Decrypts data using the hybrid encryption scheme (AES-256-GCM).
    Args:
        ciphertext (bytes): The encrypted data.
        nonce (bytes): The nonce used during encryption.
        tag (bytes): The authentication tag.
        session_key (bytes): The symmetric session key (32 bytes for AES-256).
    Returns:
        bytes: The decrypted plaintext data.
    """
    return _hybrid_crypto_instance.decrypt_data(ciphertext, nonce, tag, session_key)

def sign_data_hybrid(data: bytes, signing_key: bytes) -> bytes:
    """
    Signs data using Dilithium.
    Args:
        data (bytes): The data to sign.
        signing_key (bytes): The Dilithium signing key.
    Returns:
        bytes: The digital signature.
    """
    return _hybrid_crypto_instance.sign_data(data, signing_key)

def verify_data_signature_hybrid(data: bytes, signature: bytes, verification_key: bytes) -> bool:
    """
    Verifies a data signature using Dilithium.
    Args:
        data (bytes): The original data.
        signature (bytes): The digital signature.
        verification_key (bytes): The Dilithium verification key.
    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    return _hybrid_crypto_instance.verify_data_signature(data, signature, verification_key)

def derive_session_key(shared_secret: bytes, salt: bytes, info: bytes, key_length: int) -> bytes:
    """
    Derives a strong cryptographic key using HKDF.
    """
    return _hybrid_crypto_instance._derive_key(shared_secret, salt, info, key_length)