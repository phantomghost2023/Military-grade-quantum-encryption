"""This module provides the command-line interface for the quantum encryption project."""
import argparse
from src.hybrid_qkd_api import hybrid_encrypt, hybrid_decrypt
from src.error_handling.error_handler import ErrorHandler, QuantumEncryptionError


def encrypt_file(input_filepath: str, output_filepath: str) -> None:
    """Encrypts a file using the hybrid encryption scheme.

    Args:
        input_filepath (str): The path to the input file.
        output_filepath (str): The path to the output file.
    """
    with open(input_filepath, "rb") as f:
        plaintext = f.read()
    # For demonstration, we'll use a placeholder key pair generation.
    # In a real scenario, this would involve KMS and PQC key generation.
    # Assuming hybrid_encrypt returns ciphertext and necessary metadata
    ciphertext = hybrid_encrypt(plaintext)
    with open(output_filepath, "wb") as f:
        f.write(ciphertext)
    print(f"File '{input_filepath}' encrypted to '{output_filepath}'.")


def decrypt_file(input_filepath: str, output_filepath: str) -> None:
    """Decrypts a file using the hybrid encryption scheme.

    Args:
        input_filepath (str): The path to the input file.
        output_filepath (str): The path to the output file.
    """
    with open(input_filepath, "rb") as f:
        ciphertext = f.read()
    # Assuming hybrid_decrypt takes ciphertext and metadata to return plaintext
    plaintext = hybrid_decrypt(ciphertext)
    with open(output_filepath, "wb") as f:
        f.write(plaintext)
    print(f"File '{input_filepath}' decrypted to '{output_filepath}'.")


def main():
    """Main function to parse arguments and run the file encryption/decryption utility."""
    parser = argparse.ArgumentParser(
        description="File encryption/decryption utility using Hybrid QKD Framework."
    )
    parser.add_argument(
        "action",
        choices=["encrypt", "decrypt"],
        help="Action to perform: encrypt or decrypt.",
    )
    parser.add_argument("input", help="Input file path.")
    parser.add_argument("output", help="Output file path.")

    args = parser.parse_args()

    try:
        if args.action == "encrypt":
            encrypt_file(args.input, args.output)
        elif args.action == "decrypt":
            decrypt_file(args.input, args.output)
    except QuantumEncryptionError as e:
        ErrorHandler.handle_error(e)
    except Exception as e:
        ErrorHandler.handle_error(e, log_level="critical")


if __name__ == "__main__":
    main()
