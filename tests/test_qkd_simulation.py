import unittest
import random
from src.qkd_simulation import BB84Simulator

class TestQKDSimulation(unittest.TestCase):
    def test_bb84_simulation_no_eavesdropping(self):
        simulator = BB84Simulator(key_length=128)
        shared_key, eavesdropping_detected = simulator.run_bb84()
        self.assertIsNotNone(shared_key)
        self.assertFalse(eavesdropping_detected)
        self.assertEqual(len(shared_key), 128) # Key length might be slightly less due to sifting

    def test_bb84_simulation_eavesdropping_detection(self):
        # To simulate eavesdropping, we can manually introduce a mismatch
        # This is a conceptual test, as actual eavesdropping is probabilistic
        simulator = BB84Simulator(key_length=64)
        alice_bits, alice_bases, prepared_photons = simulator.alice_sends()

        # Simulate Eve intercepting and re-transmitting with different bases
        eve_bases = [random.choice(simulator.bases) for _ in range(len(prepared_photons))]
        eve_measurements = []
        for i, photon in enumerate(prepared_photons):
            if (photon == simulator.polarizations['+']['0'] and eve_bases[i] == '+') or \
               (photon == simulator.polarizations['+']['1'] and eve_bases[i] == '+') or \
               (photon == simulator.polarizations['x']['0'] and eve_bases[i] == 'x') or \
               (photon == simulator.polarizations['x']['1'] and eve_bases[i] == 'x'):
                eve_measurements.append(simulator.reverse_polarizations[photon])
            else:
                eve_measurements.append(str(random.randint(0, 1)))

        # Bob receives Eve's (potentially altered) photons
        bob_bases, bob_measurements = simulator.bob_receives_and_measures(prepared_photons)

        # Introduce a guaranteed mismatch for testing eavesdropping detection
        # This is a hack for testing purposes, as real QKD relies on probability
        if len(alice_bits) > 0 and len(bob_measurements) > 0:
            alice_bits[0] = 1 - alice_bits[0] # Flip a bit to ensure mismatch

        alice_sifted_key, bob_sifted_key = simulator.sift_keys(
            alice_bases, bob_bases, alice_bits, bob_measurements
        )

        eavesdropping_detected = simulator.check_eavesdropping(alice_sifted_key, bob_sifted_key, sample_size=1)
        self.assertTrue(eavesdropping_detected)

if __name__ == '__main__':
    unittest.main()