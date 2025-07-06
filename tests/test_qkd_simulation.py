import unittest
from src.qkd_simulation import simulate_qkd_protocol, generate_quantum_keys

class TestQKDSimulation(unittest.TestCase):
    def test_simulate_qkd_protocol(self):
        # Simulate a QKD protocol and check if keys are generated
        alice_key, bob_key = simulate_qkd_protocol(num_bits=100)
        self.assertIsNotNone(alice_key)
        self.assertIsNotNone(bob_key)
        self.assertEqual(len(alice_key), len(bob_key))
        # In a real QKD simulation, you'd also check for key agreement rate and errors

    def test_generate_quantum_keys(self):
        # Test the quantum key generation function
        key = generate_quantum_keys(num_bits=50)
        self.assertIsNotNone(key)
        self.assertEqual(len(key), 50)
        self.assertTrue(all(bit in ['0', '1'] for bit in key)) # Check if bits are binary

if __name__ == '__main__';
    unittest.main()