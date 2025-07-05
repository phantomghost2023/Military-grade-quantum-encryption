"""This module provides a secure messaging application using a Hybrid QKD Framework."""
import argparse
from src.hybrid_qkd_api import hybrid_encrypt, hybrid_decrypt
from src.error_handling.error_handler import ErrorHandler, QuantumEncryptionError


def send_message(sender_id: str, recipient_id: str, message: str) -> bytes:
    """Sends a secure message from a sender to a recipient.

    Args:
        sender_id (str): The ID of the sender.
        recipient_id (str): The ID of the recipient.
        message (str): The message content to be sent.

    Returns:
        bytes: The encrypted message.
    """
    print(f"Sending message from {sender_id} to {recipient_id}...")
    # Simulate encryption
    encrypted_message = hybrid_encrypt(message.encode("utf-8"))
    print(f"Encrypted message: {encrypted_message[:20]}...")  # Show first 20 bytes
    return encrypted_message


def receive_message(recipient_id: str, encrypted_message: bytes) -> None:
    """Receives and decrypts a secure message for a recipient.

    Args:
        recipient_id (str): The ID of the recipient.
        encrypted_message (bytes): The encrypted message.

    """
    print(f"\n{recipient_id} receiving message...")
    # Simulate decryption
    decrypted_message = hybrid_decrypt(encrypted_message)
    print(f"Decrypted message: {decrypted_message.decode('utf-8')}")


def main():
    """Main function to parse arguments and run the secure messaging application."""
    parser = argparse.ArgumentParser(
        description="Secure Messaging Application using Hybrid QKD Framework."
    )
    parser.add_argument("--sender", required=True, help="Sender ID.")
    parser.add_argument("--recipient", required=True, help="Recipient ID.")
    parser.add_argument("--message", required=True, help="Message to send.")

    args = parser.parse_args()

    try:
        encrypted_msg = send_message(args.sender, args.recipient, args.message)
        receive_message(args.recipient, encrypted_msg)
    except QuantumEncryptionError as e:
        ErrorHandler.handle_error(e)
    except Exception as e:
        ErrorHandler.handle_error(e, log_level="critical")


if __name__ == "__main__":
    main()
