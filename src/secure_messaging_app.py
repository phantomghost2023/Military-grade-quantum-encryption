import argparse
from src.hybrid_qkd_api import hybrid_encrypt, hybrid_decrypt


def send_message(sender_id, recipient_id, message):
    print(f"Sending message from {sender_id} to {recipient_id}...")
    # Simulate encryption
    encrypted_message, metadata = hybrid_encrypt(message.encode("utf-8"), None)
    print(f"Encrypted message: {encrypted_message[:20]}...")  # Show first 20 bytes
    return encrypted_message, metadata


def receive_message(recipient_id, encrypted_message, metadata):
    print(f"\n{recipient_id} receiving message...")
    # Simulate decryption
    decrypted_message = hybrid_decrypt(encrypted_message, None)  # None for placeholder key
    print(f"Decrypted message: {decrypted_message.decode('utf-8')}")


def main():
    parser = argparse.ArgumentParser(
        description="Secure Messaging Application using Hybrid QKD Framework."
    )
    parser.add_argument("--sender", required=True, help="Sender ID.")
    parser.add_argument("--recipient", required=True, help="Recipient ID.")
    parser.add_argument("--message", required=True, help="Message to send.")

    args = parser.parse_args()

    encrypted_msg, metadata = send_message(args.sender, args.recipient, args.message)
    receive_message(args.recipient, encrypted_msg, metadata)


if __name__ == "__main__":
    main()
