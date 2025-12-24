import requests # type: ignore
import sys
import time
from ui import Q_UI

class QuantumIngestor:
    # Use the specific API endpoint for bytes
    API_URL = "https://qrng.anu.edu.au/API/jsonI.php?length=32&type=uint8"

    @staticmethod
    def get_quantum_seed():
        ui = Q_UI() # Initialize once
        max_retries = 3
        
        # Create a session to handle connection pooling
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json'
        })

        for i in range(max_retries):
            # Cleanly draw the attempt without messy overlaps
            sys.stdout.write(f"\r{ui.dim}[*] Q-SSP: Quantum Handshake (ANU Lab) | Attempt {i+1}...{ui.reset}")
            sys.stdout.flush()
            
            try:
                # Use the session with a slightly shorter timeout for faster retries
                r = session.get(QuantumIngestor.API_URL, timeout=8)
                
                if r.status_code == 200:
                    data = r.json()
                    if data.get('success'):
                        q_bytes = bytes(data['data'])
                        # Print success on a new line to keep the progress bar clean
                        print(f"\n{ui.cyan}[+] QUANTUM ROOT ESTABLISHED: {q_bytes.hex()[:32]}...{ui.reset}")
                        return q_bytes
                
                # If status code isn't 200, wait and try again
                time.sleep(2)
                
            except Exception as e:
                # Log specific error for debugging if needed, then sleep
                time.sleep(2)
        
        # FINAL FAILURE - Hard exit as requested (Only Quantum or Nothing)
        print(f"\n{ui.red}[!] CRITICAL: Quantum Link Failure. Lab unresponsive.{ui.reset}")
        print(f"{ui.dim}>>> Check internet connection or ANU Lab status at qrng.anu.edu.au{ui.reset}")
        sys.exit(1)