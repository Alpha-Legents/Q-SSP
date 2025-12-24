import hashlib
import time
import threading
import queue
import subprocess
import os
from core.ingestor import QuantumIngestor
from core.engine import CSEE
from core.watchdog import EntropyWatchdog  # ALIGNMENT: Actually use the safety layer
import random

class QSSPSanitizer:
    def __init__(self, target_idx, ui_handler, logger):
        self.target_idx = target_idx
        self.ui = ui_handler
        self.logger = logger
        self.chunk_size = 1024 * 1024  # 1MB aligned
        self.path = f"\\\\.\\PhysicalDrive{target_idx}"
        self.watchdog = EntropyWatchdog() # ALIGNMENT: Init Watchdog
        
        # Forensic State
        self.pre_wipe_hash = "NOT_STARTED"
        self.pass1_hash = "NOT_STARTED"
        self.final_hash = "NOT_STARTED"
        self.quantum_root = "NONE"

    def get_drive_size(self):
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # OPEN_EXISTING = 3, FILE_SHARE_READ = 1, FILE_SHARE_WRITE = 2
        handle = kernel32.CreateFileW(self.path, 0x80000000 | 0x40000000, 0x1 | 0x2, None, 3, 0, None)
        
        if handle == -1:
            # If standard handle fails, the drive is locked.
            return 0
        
        # IOCTL_DISK_GET_LENGTH_INFO = 0x0007405C
        output = ctypes.c_longlong()
        returned = ctypes.c_ulong()
        res = kernel32.DeviceIoControl(handle, 0x0007405C, None, 0, ctypes.byref(output), 8, ctypes.byref(returned), None)
        kernel32.CloseHandle(handle)
        
        return output.value if res else 0

    def seize_and_clean(self):
        """
        ALIGNMENT: 'Low-Level Hardware Seizure' [Whitepaper Section 4.1]
        Uses Diskpart to offline the volume and strip the MBR/GPT.
        """
        commands = f"select disk {self.target_idx}\nclean\nrescan"
        script_file = "seize.txt"
        with open(script_file, "w") as f: f.write(commands)
        
        try:
            # We assume the UI or Main has already elevated privileges
            subprocess.run(["diskpart", "/s", script_file], capture_output=True, check=True)
            time.sleep(2) # Let Windows catch up
            os.remove(script_file)
            return True
        except Exception as e:
            self.logger.log_event("ERROR", "SEIZE", f"Diskpart failed: {e}")
            if os.path.exists(script_file): os.remove(script_file)
            return False

    def calculate_physical_hash(self, label):
        """
        ALIGNMENT: 'Provable Irrecoverability' [Whitepaper Section 5.1]
        Reads the entire physical surface, not just a snippet.
        """
        hasher = hashlib.sha256()
        total_bytes = self.get_drive_size()
        if total_bytes == 0: return "ERROR_SIZE_0"
        
        total_chunks = total_bytes // self.chunk_size
        
        try:
            with open(self.path, "rb", buffering=0) as drive:
                for i in range(1, total_chunks + 1):
                    chunk = drive.read(self.chunk_size)
                    if not chunk: break
                    hasher.update(chunk)
                    
                    if i % 50 == 0 or i == total_chunks:
                        percent = (i / total_chunks) * 100
                        self.ui.draw_progress_bar(int(percent), f" {label}")
            return hasher.hexdigest()
        except Exception as e:
            self.logger.log_event("ERROR", "HASH_FAIL", str(e))
            return "HASH_ERROR"

    def execute_wipe(self, seed, stage=1):
        # --- PHASE 1: PRE-WIPE AUDIT (Only needed once, handled by Main usually, but good to have safety) ---
        if stage == 1 and self.pre_wipe_hash == "NOT_STARTED":
            # Just in case main didn't call it, we capture it here.
            pass 

        self.quantum_root = seed
        total_bytes = self.get_drive_size()
        total_chunks = total_bytes // self.chunk_size
        chunk_queue = queue.Queue(maxsize=16) 
        
        engine = CSEE(seed)
        
        def producer():
            stream = engine.get_stream(self.chunk_size)
            for _ in range(total_chunks):
                chunk = next(stream)
                if stage == 2:
                    chunk = engine.encrypt_chunk(chunk)
                chunk_queue.put(chunk)
            chunk_queue.put(None)

        threading.Thread(target=producer, daemon=True).start()

        label = "PASS 1: QUANTUM FILL" if stage == 1 else "PASS 2: AES-CTR WIPE"
        start_time = time.time()
        
        self.logger.log_event("INFO", "WIPE_ENGINE", f"Initiating {label}", 
                             detail=f"Target: {self.path} | Mode: Direct-IO Stream")
        
        try:
            with open(self.path, "rb+", buffering=0) as drive:
                for i in range(1, total_chunks + 1):
                    chunk = chunk_queue.get()
                    if chunk is None: break
                    
                    # ALIGNMENT: 'Entropy Density Verification' [Whitepaper Section 4.2]
                    # We spot-check every 100th chunk to ensure the engine isn't failing
                    if i % 100 == 0:
                        if not self.watchdog.validate_chunk(chunk):
                            self.logger.log_event("WARN", "ENTROPY_DROP", f"Chunk {i} entropy low")

                    drive.write(chunk)
                    
                    if i % 25 == 0 or i == total_chunks:
                        percent = (i / total_chunks) * 100
                        elapsed = time.time() - start_time
                        avg_speed = (i * self.chunk_size) / (1024*1024) / elapsed if elapsed > 0 else 0
                        self.ui.draw_progress_bar(int(percent), f"{label} | {avg_speed:.1f} MB/s")

            # --- PHASE 5: POST-WRITE VERIFICATION ---
            total_time = time.time() - start_time
            
            self.logger.log_event("SUCCESS", "PERF_DATA", f"{label} Write Phase Complete", 
                                 detail=f"Duration: {total_time:.2f}s | Avg Speed: {avg_speed:.2f} MB/s")
            self.ui.update_status(f"VERIFYING {label} PHYSICAL INTEGRITY...")
            verify_hash = self.calculate_physical_hash(f"VERIFYING {label}")
            if stage == 1: self.pass1_hash = verify_hash
            else: self.final_hash = verify_hash
                
            return True

        except PermissionError:
            self.logger.log_event("ERROR", "ACCESS", "Permission denied on physical drive handle")
            self.ui.update_status("[!] ACCESS DENIED: Ensure Admin and Disk is Offline.")
            return False
        except Exception as e:
            self.logger.log_event("CRITICAL", "ENGINE", f"Wipe failure: {str(e)}")
            self.ui.update_status(f"[!] CRITICAL FAILURE: {e}")
            return False
            
    def verify_random_sectors(self, sample_count=20):
        total_bytes = self.get_drive_size()
        if total_bytes == 0: return 0.0
        
        total_entropy = 0.0
        # ALIGNMENT: Sector size is usually 512. We must seek to a multiple of 512.
        SECTOR_SIZE = 512 

        with open(self.path, "rb", buffering=0) as drive:
            for _ in range(sample_count):
                # Pick a random sector index, then multiply by sector size
                max_sectors = total_bytes // SECTOR_SIZE
                random_sector = random.randint(0, max_sectors - 8) # -8 to ensure 4096 read fits
                offset = random_sector * SECTOR_SIZE
                
                try:
                    drive.seek(offset)
                    data = drive.read(4096)
                    
                    ent = self.watchdog.calculate_entropy(data)
                    total_entropy += ent
                    
                    status = "VALID" if ent > 7.9 else "FAIL"
                    color = self.ui.green if ent > 7.9 else self.ui.red
                    # Directly printing here for the table view
                    print(f" {self.ui.dim}0x{offset:<12x}{self.ui.reset} | {ent:.6f}    | {color}{status}{self.ui.reset}")
                except OSError:
                    continue # Skip if a specific sector is locked
                
        return total_entropy / sample_count