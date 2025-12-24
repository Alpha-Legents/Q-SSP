import subprocess, os, hashlib

class Win32Disk:
    def get_drive_list(self):
        cmd = "powershell -Command \"Get-PhysicalDisk | Select-Object DeviceId, Model, Size | ConvertTo-Json\""
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        import json
        try:
            data = json.loads(res.stdout)
            if isinstance(data, dict): data = [data]
            return [{'index': str(d['DeviceId']), 'model': d['Model'], 'size': d['Size']} for d in data]
        except: return []

    def get_drive_hash(self, index):
        path = f"\\\\.\\PhysicalDrive{index}"
        try:
            with open(path, "rb", buffering=0) as f:
                return hashlib.sha256(f.read(1024*1024)).hexdigest()
        except: return "READ_ERROR"

    def run_diskpart(self, commands, logger=None):
        script = ".tmp_diskpart.txt"
        with open(script, "w") as f: f.write(commands)
        res = subprocess.run(['diskpart', '/s', script], capture_output=True, text=True)
        
        if logger:
            logger.log_event("EXEC", "DISKPART", f"CMD: {commands.splitlines()[0]}...", detail=res.stdout)
        
        if os.path.exists(script): os.remove(script)
        
        # If diskpart returns 0, the task was successful
        return res.returncode == 0
    
    def get_drive_total_bytes(self, index):
        """Refined diskpart parsing to ensure capacity is captured."""
        try:
            cmd = f"select disk {index}\ndetail disk"
            output = self.run_diskpart(cmd)
            
            for line in output.split('\n'):
                # We look for the 'Size' line and clean it up
                if "Size" in line and ":" in line:
                    # Example: "  Size : 28 GB"
                    size_text = line.split(':')[1].strip().upper()
                    # Extract the numerical part (e.g., "28")
                    value = float(size_text.split()[0])
                    
                    if "GB" in size_text:
                        return int(value * 1024 * 1024 * 1024)
                    elif "MB" in size_text:
                        return int(value * 1024 * 1024)
                    elif "TB" in size_text:
                        return int(value * 1024 * 1024 * 1024 * 1024)
            
            # Fallback: If diskpart detail fails, try list disk parsing
            list_output = self.run_diskpart("list disk")
            for line in list_output.split('\n'):
                if f"Disk {index}" in line:
                    # Example: "Disk 3    Online         28 GB    0 B"
                    parts = line.split()
                    # The size is usually at index 3
                    value = float(parts[3])
                    unit = parts[4].upper()
                    if "GB" in unit: return int(value * 1024**3)
                    if "MB" in unit: return int(value * 1024**2)
            
            return 0
        except Exception:
            return 0