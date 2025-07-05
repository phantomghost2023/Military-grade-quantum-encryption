import argparse
from src.hybrid_qkd_api import hybrid_encrypt, hybrid_decrypt


def encrypt_file(input_filepath, output_filepath):
    with open(input_filepath, "rb") as f:
        plaintext = f.read()
    # For demonstration, we'll use a placeholder key pair generation.
    # In a real scenario, this would involve KMS and PQC key generation.
    # Assuming hybrid_encrypt returns ciphertext and necessary metadata
    ciphertext, metadata = hybrid_encrypt(plaintext, None)  # None for placeholder key
    with open(output_filepath, "wb") as f:
        f.write(ciphertext)
    print(f"File '{input_filepath}' encrypted to '{output_filepath}'.")


def decrypt_file(input_filepath, output_filepath):
    with open(input_filepath, "rb") as f:
        ciphertext = f.read()
    # Assuming hybrid_decrypt takes ciphertext and metadata to return plaintext
    plaintext = hybrid_decrypt(ciphertext, None)  # None for placeholder key/metadata
    with open(output_filepath, "wb") as f:
        f.write(plaintext)
    print(f"File '{input_filepath}' decrypted to '{output_filepath}'.")


def main():
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

    if args.action == "encrypt":
        encrypt_file(args.input, args.output)
    elif args.action == "decrypt":
        decrypt_file(args.input, args.output)


if __name__ == "__main__":
    main()
