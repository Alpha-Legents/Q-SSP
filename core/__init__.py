def __init__(self):
        # Using TrueColor (24-bit) sequences for that 'HD' look
        # Format: \033[38;2;R;G;Bm
        self.cyan   = "\033[38;2;0;255;255m"   # Neon Electric Cyan
        self.green  = "\033[38;2;50;255;50m"   # Radioactive Green
        self.yellow = "\033[38;2;255;225;0m"   # Cyberpunk Yellow
        self.red    = "\033[38;2;255;50;50m"   # High-Voltage Red
        self.white  = "\033[38;2;255;255;255m" # Pure White
        self.reset  = "\033[0m"
        self.bold   = "\033[1m"
        self.dim    = "\033[38;2;110;110;110m" # Deep Grey for separators