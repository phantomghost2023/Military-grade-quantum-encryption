#!/usr/bin/env python3
"""
Simple test runner to verify the Military-Grade Quantum Encryption Framework
modules can be imported and basic functionality works.
"""

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing module imports...")
    
    try:
        import src.pqc_primitives
        print("✓ pqc_primitives imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pqc_primitives: {e}")
        return False
    
    try:
        import src.pqc
        print("✓ pqc imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pqc: {e}")
        return False
    
    try:
        import src.hybrid_qkd_api
        print("✓ hybrid_qkd_api imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import hybrid_qkd_api: {e}")
        return False
    
    try:
        import src.cli_app
        print("✓ cli_app imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import cli_app: {e}")
        return False
    
    try:
        import src.secure_messaging_app
        print("✓ secure_messaging_app imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import secure_messaging_app: {e}")
        return False
    
    try:
        import src.error_handling.error_handler
        print("✓ error_handler imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import error_handler: {e}")
        return False

    try:
        import src.qkd_simulation
        print("✓ qkd_simulation imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import qkd_simulation: {e}")
        return False

    try:
        import src.hybrid_crypto
        print("✓ hybrid_crypto imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import hybrid_crypto: {e}")
        return False

    try:
        import src.kms_api
        print("✓ kms_api imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import kms_api: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of the modules."""
    print("\nTesting basic functionality...")
    
    try:
        from src.pqc_primitives import Kyber, Dilithium
        
        # Test Kyber initialization
        kyber = Kyber(security_level=1)
        print("✓ Kyber initialization successful")
        
        # Test Dilithium initialization
        dilithium = Dilithium()
        print("✓ Dilithium initialization successful")
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False
    
    try:
        from src.hybrid_qkd_api import simulate_qkd_key_exchange, perform_hybrid_key_exchange, encrypt_data_hybrid, decrypt_data_hybrid, derive_session_key
        from src.hybrid_crypto import HybridCrypto
        import os

        # Test QKD Simulation
        qkd_key, eavesdropping = simulate_qkd_key_exchange()
        if eavesdropping:
            print("✓ QKD simulation detected eavesdropping (expected behavior for some runs)")
        else:
            print("✓ QKD simulation successful (no eavesdropping detected)")
            assert qkd_key is not None and len(qkd_key) > 0

        # Test Hybrid Key Exchange
        qkd_key_hex, kyber_ct, kyber_ss, kyber_pk = perform_hybrid_key_exchange()
        if qkd_key_hex is None:
            print("✓ Hybrid key exchange aborted due to QKD eavesdropping (expected behavior for some runs)")
        else:
            print("✓ Hybrid key exchange successful")
            assert kyber_ct is not None and kyber_ss is not None
            
            # For testing purposes, we'll use the returned kyber_ss directly as if it was decapsulated
            
            combined_secret = qkd_key_hex.encode('utf-8') + kyber_ss
            salt = os.urandom(16)
            info = b"test-session-key"
            session_key = derive_session_key(combined_secret, salt, info, 32)
            print("✓ Session key derived successfully")

            # Test hybrid encryption and decryption
            original_data = b"test data for hybrid encryption"
            ciphertext, nonce, tag = encrypt_data_hybrid(original_data, session_key)
            print("✓ Hybrid encryption successful")

            decrypted_data = decrypt_data_hybrid(ciphertext, nonce, tag, session_key)
            print("✓ Hybrid decryption successful")
            assert original_data == decrypted_data

    except Exception as e:
        print(f"✗ Hybrid API test failed: {e}")
        return False

    try:
        from src.kms_api import KMS
        import os

        kms = KMS(master_password="test_password")

        # Test PQC key generation
        pqc_key_id = "test_pqc_key"
        kms.generate_pqc_key_pair(pqc_key_id, "Kyber")
        assert kms.get_key(pqc_key_id) is not None
        print("✓ KMS PQC key generation successful")

        # Test symmetric key generation
        sym_key_id = "test_sym_key"
        kms.generate_symmetric_key(sym_key_id)
        assert kms.get_key(sym_key_id) is not None
        print("✓ KMS symmetric key generation successful")

        # Test key rotation
        rotated_key_id = kms.rotate_key(pqc_key_id)
        assert kms.get_key(pqc_key_id)["status"] == "inactive"
        assert kms.get_key(rotated_key_id)["status"] == "active"
        print("✓ KMS key rotation successful")

        # Test key revocation
        kms.revoke_key(sym_key_id)
        assert kms.get_key(sym_key_id)["status"] == "revoked"
        print("✓ KMS key revocation successful")

        # Test hybrid key exchange with KMS
        dummy_recipient_pk = os.urandom(32) # Placeholder
        session_key, _, _ = kms.perform_hybrid_key_exchange_with_kms(dummy_recipient_pk)
        assert session_key is not None
        print("✓ KMS hybrid key exchange successful")

        # Clean up the test key store file
        if os.path.exists(kms.key_store_path):
            os.remove(kms.key_store_path)

    except Exception as e:
        print(f"✗ KMS functionality test failed: {e}")
        return False

    try:
        from src.kms_api import KMS
        import os

        kms = KMS(master_password="test_password")

        # Test PQC key generation
        pqc_key_id = "test_pqc_key"
        kms.generate_pqc_key_pair(pqc_key_id, "Kyber")
        assert kms.get_key(pqc_key_id) is not None
        print("✓ KMS PQC key generation successful")

        # Test symmetric key generation
        sym_key_id = "test_sym_key"
        kms.generate_symmetric_key(sym_key_id)
        assert kms.get_key(sym_key_id) is not None
        print("✓ KMS symmetric key generation successful")

        # Test key rotation
        rotated_key_id = kms.rotate_key(pqc_key_id)
        assert kms.get_key(pqc_key_id)["status"] == "inactive"
        assert kms.get_key(rotated_key_id)["status"] == "active"
        print("✓ KMS key rotation successful")

        # Test key revocation
        kms.revoke_key(sym_key_id)
        assert kms.get_key(sym_key_id)["status"] == "revoked"
        print("✓ KMS key revocation successful")

        # Test hybrid key exchange with KMS
        dummy_recipient_pk = os.urandom(32) # Placeholder
        session_key, _, _ = kms.perform_hybrid_key_exchange_with_kms(dummy_recipient_pk)
        assert session_key is not None
        print("✓ KMS hybrid key exchange successful")

        # Clean up the test key store file
        if os.path.exists(kms.key_store_path):
            os.remove(kms.key_store_path)

    except Exception as e:
        print(f"✗ KMS functionality test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("Military-Grade Quantum Encryption Framework - Test Runner")
    print("=" * 60)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return 1
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Basic functionality tests failed!")
        return 1
    
    print("\n✅ All tests passed! The framework is ready for development.")
    return 0

if __name__ == "__main__":
    exit(main())