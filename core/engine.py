import hashlib
from typing import Generator
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class CSEE:
    """
    Cryptographically Secure Expansion Engine (CSEE).
    ALIGNMENT: 'Cryptographically Secure Expansion Engine' [Whitepaper Section 4.2]
    """
    def __init__(self, seed: bytes):
        if not isinstance(seed, bytes):
            raise TypeError("Quantum seed must be bytes")
        self.seed = seed
        self.counter = 0

    def get_stream(self, chunk_size: int = 1024 * 1024) -> Generator[bytes, None, None]:
        """
        Squeezes SHAKE-256 to generate infinite entropy.
        """
        while True:
            # ALIGNMENT: 'Block Mixing and Salting' [Whitepaper Section 5.2]
            salt = self.counter.to_bytes(8, 'big')
            hasher = hashlib.shake_256(self.seed + salt)
            yield hasher.digest(chunk_size)
            self.counter += 1

    def encrypt_chunk(self, chunk: bytes) -> bytes:
        """
        ALIGNMENT: 'Encrypted Overwrite' [Whitepaper Section 4.3]
        """
        # Unique nonce per chunk derived from quantum root + counter
        nonce_material = hashlib.sha256(self.seed + self.counter.to_bytes(8, 'big')).digest()
        nonce = nonce_material[:16]
        
        # Derive a transient key (never stored)
        key = hashlib.sha256(self.seed + b"TRANSIENT_KEY_GEN").digest()
        
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        
        self.counter += 1
        return encryptor.update(chunk) + encryptor.finalize()