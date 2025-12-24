import math
from collections import Counter

class EntropyWatchdog:
    """
    The Safety Layer of Q-SSP.
    Monitors the data stream to ensure it remains non-deterministic.
    """

    @staticmethod
    def calculate_entropy(data: bytes) -> float:
        """
        Calculates Shannon Entropy. 
        8.0 = True Random, 0.0 = All bytes are the same.
        """
        if not data:
            return 0.0
        
        # Count frequency of each byte (0-255)
        counts = Counter(data)
        entropy = 0.0
        
        for count in counts.values():
            # Probability of this byte appearing
            p = count / len(data)
            # Shannon entropy formula: H = -sum(p * log2(p))
            entropy -= p * math.log2(p)
            
        return entropy

    def validate_chunk(self, data: bytes, threshold: float = 7.9) -> bool:
        """
        Checks if a chunk of data is safe to use for sanitization.
        """
        score = self.calculate_entropy(data)
        if score >= threshold:
            return True
        else:
            print(f"[!!!] SAFETY TRIGGER: Entropy dropped to {score:.4f}!")
            return False

# --- Testing the Watchdog ---
if __name__ == "__main__":
    dog = EntropyWatchdog()
    
    # Test 1: Random data (should pass)
    import os
    good_data = os.urandom(1024)
    print(f"Random Data Score: {dog.calculate_entropy(good_data):.4f}")
    
    # Test 2: Repeating data (should fail)
    bad_data = b"\x00" * 1024
    print(f"Bad Data Score: {dog.calculate_entropy(bad_data):.4f}")