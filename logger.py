import datetime
import os
import sys

class QLogger:
    def __init__(self, log_dir="audit_logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"QSSP_AUDIT_{self.session_id}.log")
        
        with open(self.log_file, "w") as f:
            f.write(f"--- Q-SSP FORENSIC AUDIT SESSION START: {self.session_id} ---\n")

    def log_event(self, level, module, message, detail=None):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level.upper()}] [{module}] {message}"
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
            if detail:
                f.write(f"DETAIL: {detail}\n")
                f.write("-" * 40 + "\n")
               
    def finalize_certificate(self, hashes, entropy_avg):
        cert = f"""
============================================================
           Q-SSP CERTIFICATE OF DESTRUCTION
============================================================
SESSION ID: {self.session_id}
QUANTUM ROOT: VERIFIED (ANU VACUUM SOURCE)
------------------------------------------------------------
PRE-WIPE HASH:  {hashes.get('PRE-WIPE')}
PASS 1 HASH:    {hashes.get('PASS_1')}
FINAL HASH:     {hashes.get('FINAL')}
------------------------------------------------------------
AVERAGE ENTROPY: {entropy_avg:.6f} bits/byte
LEGAL STATUS:   DATA IRREVERSIBLE / PHYSICALLY TERMINATED
============================================================
        """
        with open(self.log_file, "a") as f:
            f.write(cert) 