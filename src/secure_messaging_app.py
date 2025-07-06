"""This module provides a secure messaging application using a Hybrid QKD Framework."""
import argparse
import base64
from src.hybrid_qkd_api import hybrid_encrypt, hybrid_decrypt
from src.error_handling.error_handler import ErrorHandler, QuantumEncryptionError
from src.data_manager import DataManager
from src.auth import get_user_by_username

data_manager = DataManager()

def send_message(sender_id: str, recipient_id: str, message: str) -> str:
    """Sends a secure message from a sender to a recipient and stores it in the database.

    Args:
        sender_id (str): The username of the sender.
        recipient_id (str): The username of the recipient.
        message (str): The message content to be sent.

    Returns:
        str: The data_id of the stored encrypted message.
    """
    print(f"Sending message from {sender_id} to {recipient_id}...")

    sender_user = get_user_by_username(sender_id)
    recipient_user = get_user_by_username(recipient_id)

    if not sender_user:
        raise ValueError(f"Sender user '{sender_id}' not found.")
    if not recipient_user:
        raise ValueError(f"Recipient user '{recipient_id}' not found.")

    encrypted_message = hybrid_encrypt(message.encode("utf-8"))
    print(f"Encrypted message: {encrypted_message[:20]}...")  # Show first 20 bytes

    encryption_metadata = {
        "algorithm": "hybrid_qkd",
        "sender_username": sender_id,
        "recipient_username": recipient_id,
        "original_message_length": len(message)
    }

    data_id = data_manager.store_encrypted_data(
        user_id=sender_user['id'],
        data_type="secure_message",
        encrypted_content=encrypted_message,
        encryption_metadata=encryption_metadata
    )

    if data_id:
        print(f"Message stored with data_id: {data_id}")
        return data_id
    else:
        raise Exception("Failed to store encrypted message.")


def receive_message(recipient_id: str, data_id: str) -> None:
    """Receives and decrypts a secure message for a recipient from the database.

    Args:
        recipient_id (str): The username of the recipient.
        data_id (str): The data_id of the encrypted message in the store.

    """
    print(f"\n{recipient_id} receiving message with data_id: {data_id}...")

    recipient_user = get_user_by_username(recipient_id)
    if not recipient_user:
        raise ValueError(f"Recipient user '{recipient_id}' not found.")

    stored_data = data_manager.retrieve_encrypted_data(data_id)

    if not stored_data:
        print(f"Error: Message with data_id {data_id} not found.")
        return

    # Basic authorization check: ensure recipient is intended recipient or has permission
    # In a real system, this would be more robust, potentially involving KMS access control
    if stored_data['encryption_metadata'].get('recipient_username') != recipient_id:
        print(f"Warning: User {recipient_id} is not the intended recipient of message {data_id}.")
        # Depending on policy, might raise an error or proceed with a warning

    encrypted_message = stored_data['encrypted_content']
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
    parser.add_argument("--data_id", help="Optional: Data ID to retrieve a message instead of sending.")

    args = parser.parse_args()

    try:
        if args.data_id:
            receive_message(args.recipient, args.data_id)
        else:
            data_id = send_message(args.sender, args.recipient, args.message)
            # After sending, simulate receiving the same message by its data_id
            receive_message(args.recipient, data_id)
    except QuantumEncryptionError as e:
        ErrorHandler.handle_error(e)
    except Exception as e:
        ErrorHandler.handle_error(e, message="An unexpected error occurred in secure messaging app.", level="critical")



if __name__ == "__main__":
    main()
