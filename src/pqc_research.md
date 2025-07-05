# PQC Algorithm Research Findings

This document will serve as a repository for research findings on Post-Quantum Cryptography (PQC) algorithms, specifically focusing on NIST PQC Round 3/4 finalists and candidates.

## 0.1 Deep Dive into PQC Algorithms

### NIST PQC Candidates to Research:

*   **Key Encapsulation Mechanisms (KEMs):**
    *   Kyber (Lattice-based)
    *   Classic McEliece (Code-based)
    *   BIKE (Code-based)
    *   HQC (Code-based)

*   **Digital Signature Algorithms (DSAs):**
    *   Dilithium (Lattice-based)
    *   Falcon (Lattice-based)
    *   SPHINCS+ (Hash-based)

### Research Areas for Each Algorithm:

1.  **Official NIST Documentation & Academic Papers:**
    *   Summarize the core concepts and design principles.
    *   Note any specific security claims or proofs.

2.  **Underlying Mathematical Principles:**
    *   Briefly explain the mathematical hard problem it relies on (e.g., Learning With Errors for lattice-based, decoding random linear codes for code-based).

3.  **Security Analysis:**
    *   Discuss known attack vectors (classical and quantum).
    *   Review any cryptanalysis results.

4.  **Performance Characteristics:**
    *   **Key Sizes:** Public key, private key sizes.
    *   **Ciphertext/Signature Sizes:** Size of encapsulated keys or signatures.
    *   **Computational Speed:** Encryption/decryption, signing/verification speeds (qualitative initially, quantitative with benchmarks later).
    *   **Memory Usage:** Memory footprint during operations.

### Initial Findings (To be populated):

*   **Kyber:**
    *   *Summary:*
    *   *Math Principles:*
    *   *Security:*
    *   *Performance:*

*   **Dilithium:**
    *   *Summary:*
    *   *Math Principles:*
    *   *Security:*
    *   *Performance:*

*   **Falcon:**
    *   *Summary:*
    *   *Math Principles:*
    *   *Security:*
    *   *Performance:*

*   **SPHINCS+:**
    *   *Summary:*
    *   *Math Principles:*
    *   *Security:*
    *   *Performance:*

*   **Classic McEliece:**
    *   *Summary:*
    *   *Math Principles:*
    *   *Security:*
    *   *Performance:*

---

**Next Steps:** Populate this document with detailed research for each algorithm, focusing on the outlined areas.