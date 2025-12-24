from logging import log
import sys
import os
import time
from ui import Q_UI
from hardware import Win32Disk
from logger import QLogger
from core.ingestor import QuantumIngestor
from core.sanitizer import QSSPSanitizer

def main():
    ui = Q_UI()
    hw = Win32Disk()
    log = QLogger()
    avg_entropy = 0.0  
    hashes = {'PRE-WIPE': 'N/A', 'PASS_1': 'N/A', 'FINAL': 'N/A'}
    if sys.platform == "win32": os.system('color')
    ui.draw_banner(animate=True)

    # 1. HARDWARE SELECTION
    disks = hw.get_drive_list()
    if not disks:
        print(f"{ui.red}[!] No physical disks detected. Run as Administrator.{ui.reset}")
        return

    disks.sort(key=lambda x: int(x['index']))
    
    try:
        target_idx = ui.select_disk_interactive(disks)
        print("\n" * 2) 
    except KeyboardInterrupt:
        return
    
    target_disk = next((d for d in disks if d['index'] == target_idx), None)
    log.log_event("INFO", "HARDWARE", f"Target selected: {target_disk['model']} ({int(target_disk['size'])/(1024**3):.2f} GB)")

    # 2. SAFETY GATES
    ui.draw_warning_header(target_idx)
    confirm = input(f"{ui.yellow}[?] PROCEED WITH FULL DISK SANITIZATION? (y/n): {ui.reset}").lower().strip()
    if confirm != 'y':
        print(f"{ui.dim}[*] Protocol disarmed.{ui.reset}")
        return

    # 3. SETUP SANITIZER EARLY (Needed for Seizure & Hashing)
    sanitizer = QSSPSanitizer(target_idx, ui, log)
    
    # 4. CAPTURE PRE-WIPE STATE (THE REAL FULL HASH)
    ui.update_status("INITIALIZING FORENSIC CHAIN...", centered=False)
    # ALIGNMENT: Using the sanitizer's full read, not the hardware's 1MB read
    pre_wipe = sanitizer.calculate_physical_hash("CAPTURING PRE-WIPE STATE")
    print("")
    sanitizer.pre_wipe_hash = pre_wipe
    print(f"    >>> HASH: {pre_wipe}")
    log.log_event("INFO", "FORENSIC", f"Initial state hash: {pre_wipe}")

    # 5. QUANTUM HANDSHAKE
    seed = QuantumIngestor.get_quantum_seed()
    log.log_event("INFO", "QUANTUM", f"Root seed generated via ANU Vacuum Source: {seed.hex()}")

    # 6. SEIZE HARDWARE
    print(f"{ui.yellow}[*] Seizing Hardware Control (Diskpart)...{ui.reset}")
    if not sanitizer.seize_and_clean():
        print(f"{ui.red}[!] Failed to seize drive. Check permissions.{ui.reset}")
        return

    # 7. EXECUTION
    total_size = sanitizer.get_drive_size()
    print(f"\n[*] Target Capacity: {total_size / (1024**3):.2f} GB")

    # Pass 1
    ui.update_status("ENGAGING PASS 1: QUANTUM VACUUM FILL...")
    if sanitizer.execute_wipe(seed, stage=1):
    
        
        # Pass 2
        ui.update_status("ENGAGING PASS 2: AES-256-CTR (QUANTUM NONCES)...")
        if sanitizer.execute_wipe(seed, stage=2):
            
            # 8. FINAL AUDIT TABLE
            hashes = {
                'PRE-WIPE': sanitizer.pre_wipe_hash,
                'PASS_1': sanitizer.pass1_hash,
                'FINAL': sanitizer.final_hash
            }
            
            print(f"\n\n{ui.bold}PHYSICAL DATA EVOLUTION (SHA-256 CHAIN){ui.reset}")
            print(f"{ui.dim}———————————————————————————————————————————————————————————————————————————{ui.reset}")
            print(f"{ui.cyan}PRE-WIPE (ORIGINAL)       {ui.reset}| {hashes['PRE-WIPE']}")
            print(f"{ui.cyan}POST-PASS 1 (QUANTUM)     {ui.reset}| {hashes['PASS_1']}")
            print(f"{ui.cyan}POST-PASS 2 (FINAL)       {ui.reset}| {hashes['FINAL']}")
            print(f"{ui.dim}———————————————————————————————————————————————————————————————————————————{ui.reset}")
            
            hashes = {
            'PRE-WIPE': sanitizer.pre_wipe_hash,
                'PASS_1': sanitizer.pass1_hash,
                'FINAL': sanitizer.final_hash
            }
            log.finalize_certificate(hashes, avg_entropy)
            # Deep Sector Interrogation
            print(f"\n{ui.cyan}[*] STARTING DEEP SECTOR INTERROGATION...{ui.reset}")
            avg_entropy = sanitizer.verify_random_sectors(sample_count=20)
            
            # 9. COMPLETION
            print(f"\n{ui.yellow}[?] SANITIZATION COMPLETE. End-state selection:{ui.reset}")
            print(" [1] LEAVE AS GHOST (Uninitialized/RAW - Recommended for Forensics)")
            print(" [2] RE-INITIALIZE (GPT/NTFS - Ready for OS)")
            
            choice = input(f"{ui.bold}>> Selection [1/2]: {ui.reset}")
            if choice == "2":
                print(f"\n{ui.cyan}{ui.bold}[*] INITIATING HARDWARE RECONSTRUCTION PROTOCOL...{ui.reset}")
                
                # Define the sequence of tasks
                tasks = [
                    ("Initializing Partition Table (GPT)", f"select disk {target_idx}\nclean\nconvert gpt"),
                    ("Seizing Primary Partition", f"select disk {target_idx}\ncreate partition primary"),
                    ("Mounting Logical Volume", f"select disk {target_idx}\nselect partition 1\nassign"),
                    ("NTFS Bit-Stream Initialization", f"select disk {target_idx}\nselect partition 1\nformat fs=ntfs quick"),
                    ("Finalizing Explorer Visibility", "rescan")
                ]

                for task_name, command in tasks:
                    # Print the pending state
                    sys.stdout.write(f" {ui.dim}→ {task_name:<40} {ui.reset}")
                    sys.stdout.flush()
                    
                    # Execute specific step
                    success = hw.run_diskpart(command, log)
                    
                    if success:
                        print(f"[{ui.cyan} SUCCESS {ui.reset}]")
                    else:
                        print(f"[{ui.red} FAILED  {ui.reset}]")
                

                print(f"\n{ui.cyan}{ui.bold}[+] RECONSTRUCTION COMPLETE: Volume is now visible in Windows Explorer.{ui.reset}")
                
            else:
                print(f"\n{ui.yellow}[*] Drive left in RAW Quantum state (Uninitialized).{ui.reset}")
                
            print(f"\n{ui.cyan}>>> Q-SSP SUCCESS. CERTIFICATE SAVED: {log.log_file}{ui.reset}")
                
                
    # Memory Purge
    if 'seed' in locals():
        seed = b'\x00' * len(seed)
        del seed
        print("\n[+] Memory Purged: Quantum Seed Zeroed.")

if __name__ == "__main__":
    main()