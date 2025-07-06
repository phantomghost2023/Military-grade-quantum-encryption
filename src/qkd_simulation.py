
"""
This module provides a software simulation of a Quantum Key Distribution (QKD) protocol,
specifically the BB84 protocol, to conceptually establish a shared secret key
and demonstrate eavesdropping detection.
"""


import random

class BB84Simulator:
    """
    Simulates the BB84 Quantum Key Distribution protocol.
    """

    def __init__(self, key_length: int = 128):
        """
        Initializes the BB84 simulator.

        Args:
            key_length (int): The desired length of the raw key before sifting.
        """
        self.key_length = key_length
        self.bases = ['+', 'x']  # Rectilinear (+) and Diagonal (x) bases
        self.polarizations = {
            '+': {'0': '↑', '1': '→'},  # Vertical, Horizontal
            'x': {'0': '↗', '1': '↘'}   # Diagonal up, Diagonal down
        }
        self.reverse_polarizations = {
            '↑': '0', '→': '1', '↗': '0', '↘': '1'
        }

    def _generate_random_bits_and_bases(self, length: int):
        """Generates random bits and corresponding random bases."""
        bits = [random.randint(0, 1) for _ in range(length)]
        bases = [random.choice(self.bases) for _ in range(length)]
        return bits, bases

    def alice_sends(self):
        """
        Alice generates random bits and bases, and prepares 'photons'.

        Returns:
            tuple: (alice_bits, alice_bases, prepared_photons)
        """
        alice_bits, alice_bases = self._generate_random_bits_and_bases(self.key_length)
        prepared_photons = []
        for bit, base in zip(alice_bits, alice_bases):
            prepared_photons.append(self.polarizations[base][str(bit)])
        return alice_bits, alice_bases, prepared_photons

    def bob_receives_and_measures(self, prepared_photons: list):
        """
        Bob generates random bases and measures the incoming 'photons'.

        Args:
            prepared_photons (list): List of 'photons' (polarizations) sent by Alice.

        Returns:
            tuple: (bob_bases, bob_measurements)
        """
        bob_bases = [random.choice(self.bases) for _ in range(len(prepared_photons))]
        bob_measurements = []
        for i, photon in enumerate(prepared_photons):
            # If Bob's base matches Alice's, he gets the correct bit.
            # Otherwise, he gets a random bit (simulating quantum uncertainty).
            if (photon == self.polarizations['+']['0'] and bob_bases[i] == '+') or \
               (photon == self.polarizations['+']['1'] and bob_bases[i] == '+') or \
               (photon == self.polarizations['x']['0'] and bob_bases[i] == 'x') or \
               (photon == self.polarizations['x']['1'] and bob_bases[i] == 'x'):
                # Bob's measurement matches Alice's original bit
                bob_measurements.append(self.reverse_polarizations[photon])
            else:
                # Bob's base doesn't match, so he gets a random outcome
                bob_measurements.append(str(random.randint(0, 1)))
        return bob_bases, [int(b) for b in bob_measurements]

    def sift_keys(self, alice_bases: list, bob_bases: list, alice_bits: list, bob_measurements: list):
        """
        Alice and Bob publicly compare their bases to sift the raw key.

        Args:
            alice_bases (list): Alice's chosen bases.
            bob_bases (list): Bob's chosen bases.
            alice_bits (list): Alice's original bits.
            bob_measurements (list): Bob's measured bits.

        Returns:
            tuple: (alice_sifted_key, bob_sifted_key)
        """
        alice_sifted_key = []
        bob_sifted_key = []
        for i in range(len(alice_bases)):
            if alice_bases[i] == bob_bases[i]:
                alice_sifted_key.append(alice_bits[i])
                bob_sifted_key.append(bob_measurements[i])
        return alice_sifted_key, bob_sifted_key

    def check_eavesdropping(self, alice_sifted_key: list, bob_sifted_key: list, sample_size: int = 10):
        """
        Alice and Bob compare a sample of their sifted keys to detect eavesdropping.

        Args:
            alice_sifted_key (list): Alice's sifted key.
            bob_sifted_key (list): Bob's sifted key.
            sample_size (int): Number of bits to compare for eavesdropping detection.

        Returns:
            bool: True if eavesdropping is detected (mismatch), False otherwise.
        """
        if len(alice_sifted_key) < sample_size or len(bob_sifted_key) < sample_size:
            sample_size = min(len(alice_sifted_key), len(bob_sifted_key))

        sample_indices = random.sample(range(len(alice_sifted_key)), sample_size)

        eavesdropping_detected = False
        for i in sample_indices:
            if alice_sifted_key[i] != bob_sifted_key[i]:
                eavesdropping_detected = True
                break
        return eavesdropping_detected

    def run_bb84(self):
        """
        Runs a full BB84 simulation.

        Returns:
            tuple: (shared_secret_key, eavesdropping_detected)
                   shared_secret_key is None if eavesdropping is detected.
        """
        alice_bits, alice_bases, prepared_photons = self.alice_sends()
        bob_bases, bob_measurements = self.bob_receives_and_measures(prepared_photons)

        alice_sifted_key, bob_sifted_key = self.sift_keys(
            alice_bases, bob_bases, alice_bits, bob_measurements
        )

        eavesdropping_detected = self.check_eavesdropping(alice_sifted_key, bob_sifted_key)

        if eavesdropping_detected:
            return None, True
        else:
            # In a real scenario, privacy amplification would be applied here.
            # For simulation, we'll just use the sifted key.
            # Ensure keys are identical after sifting and before returning
            if alice_sifted_key == bob_sifted_key:
                return "".join(map(str, alice_sifted_key)), False
            else:
                # This case should ideally not happen if no eavesdropping is detected
                # and sifting is done correctly. It implies a simulation error.
                return None, True # Treat as eavesdropping for safety

if __name__ == "__main__":
    print("Running BB84 Simulation Example:")
    simulator = BB84Simulator(key_length=256)
    shared_key, eavesdropping = simulator.run_bb84()

    if eavesdropping:
        print("Eavesdropping detected! Key exchange aborted.")
    else:
        print(f"Shared Secret Key: {shared_key}")
        print(f"Key Length: {len(shared_key) if shared_key else 0} bits")
