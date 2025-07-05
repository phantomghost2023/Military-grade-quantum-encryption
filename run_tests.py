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
        dilithium = Dilithium(security_level=2)
        print("✓ Dilithium initialization successful")
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False
    
    try:
        from src.hybrid_qkd_api import hybrid_encrypt, hybrid_decrypt
        
        # Test hybrid encryption (placeholder)
        ciphertext, metadata = hybrid_encrypt(b"test")
        print("✓ Hybrid encryption test successful")
        
        # Test hybrid decryption (placeholder)
        plaintext = hybrid_decrypt(ciphertext)
        print("✓ Hybrid decryption test successful")
        
    except Exception as e:
        print(f"✗ Hybrid API test failed: {e}")
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