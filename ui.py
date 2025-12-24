import sys
import msvcrt
import time
import os
import random

class Q_UI:
    def __init__(self):
        # Professional Industrial Palette
        self.logo_color = "\033[1;38;2;88;166;255m"  # Steel Blue (Logo)
        self.cyan       = "\033[1;38;2;63;185;80m"   # Emerald Green (Progress/Success)
        self.yellow     = "\033[1;38;2;210;153;34m"  # Harvest Gold (Prompts/Warnings)
        self.red        = "\033[1;38;2;248;81;73m"   # Crimson (Critical/Delete)
        self.white      = "\033[1;38;2;201;209;217m" # Off-White (Text)
        self.dim        = "\033[38;2;72;82;92m"      # Slate Grey (Separators/Inactive)
        self.reset      = "\033[0m"
        self.bold       = "\033[1m"
        self.hide       = "\033[?25l"
        self.show       = "\033[?25h"
        
        # Compatibility fix
        self.green      = self.cyan 
        
        # Initialize terminal state
        sys.stdout.write(self.hide)
        sys.stdout.flush()

    def draw_banner(self, animate=False):
        logo = [
            "  ██████╗         ███████╗███████╗██████╗ ",
            " ██╔═══██╗         ██╔════╝██╔════╝██╔══██╗",
            " ██║   ██║  █████╗ ███████╗███████╗██████╔╝",
            " ██║▄▄ ██║  ╚════╝ ╚════██║╚════██║██╔═══╝ ",
            " ╚██████╔╝         ███████║███████║██║     ",
            "  ╚══▀▀═╝          ╚══════╝╚══════╝╚═╝     "
        ]
        
        try:
            term_width = os.get_terminal_size().columns
        except:
            term_width = 120

        def print_centered(text, color="", effect=False):
            padding = max(0, (term_width - len(text)) // 2)
            if effect:
                noise = "".join(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?") if c != " " else " " for c in text)
                sys.stdout.write(" " * padding + f"{self.dim}{noise}{self.reset}\n")
            else:
                sys.stdout.write(" " * padding + f"{color}{text}{self.reset}\n")
                
        # 1. Clear screen to ensure we start at (0,0) for the animation
        os.system('cls' if os.name == 'nt' else 'clear')

        if animate:
            # Phase 1: Glitch (Static / Pin to top)
            for _ in range(10):
                sys.stdout.write("\033[H") # <--- PINS ANIMATION TO TOP (No scrolling jank)
                sys.stdout.write("\n" * 2)
                for line in logo:
                    color = self.logo_color if random.random() > 0.8 else self.dim
                    print_centered(line, color=color, effect=True)
                sys.stdout.flush()
                time.sleep(0.04)
            
            # Phase 2: Reveal (Static / Pin to top)
            for i in range(len(logo) + 1):
                sys.stdout.write("\033[H") # <--- KEEPS IT SMOOTH
                sys.stdout.write("\n" * 2)
                for j, line in enumerate(logo):
                    if j == i: print_centered(line, color="\033[1;37m")
                    elif j < i: print_centered(line, color=self.logo_color + self.bold)
                    else: print_centered(line, effect=True)
                sys.stdout.flush()
                time.sleep(0.06)
                        
        # 2. FINAL RENDER: RELEASE THE CURSOR
        # We clear the screen one last time to remove any animation artifacts.
        os.system('cls' if os.name == 'nt' else 'clear') 
        
        # Now we print normally (without \033[H). 
        # This pushes the banner into the scrollback history so you can scroll up later.
        sys.stdout.write("\n" * 2)
        for line in logo:
            print_centered(line, color=self.logo_color + self.bold)
            
        subtext = "QUANTUM-STABLE SANITIZATION PROTOCOL | v1.0"
        sub_padding = max(0, (term_width - len(subtext)) // 2)
        sys.stdout.write("\n" + " " * sub_padding + f"{self.dim}{subtext}{self.reset}\n")
        
        sep = "—" * 80
        sep_padding = max(0, (term_width - len(sep)) // 2)
        sys.stdout.write(" " * sep_padding + f"{self.dim}{sep}{self.reset}\n\n")
        sys.stdout.flush()

    def update_status(self, message, centered=False):
        """Prints a status message. Clears the line first to prevent 'staircase' drift."""
        try:
            term_width = os.get_terminal_size().columns
        except:
            term_width = 120
        
        
        sys.stdout.write("\r\033[2K") 
        
        clean_msg = message.strip().replace("[*]", "").strip()
        formatted_msg = f"[*] {clean_msg}"
        
        if centered:
            # Only use this for the main banner/headers
            padding = max(0, (term_width - len(formatted_msg)) // 2)
            sys.stdout.write(" " * padding + f"{self.cyan}{formatted_msg}{self.reset}\n")
        else:
            # Left-aligned (Professional Log Style)
            sys.stdout.write(f"{self.cyan}{formatted_msg}{self.reset}\n")
        
        sys.stdout.flush()

    def draw_progress_bar(self, percentage, prefix=""):
        width = 40
        flux = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        anim = flux[int(time.time() * 10) % len(flux)]
        done = int(width * percentage / 100)
        
        bar = f"{self.cyan}█{self.reset}" * done + f"{self.dim}░{self.reset}" * (width - done)
        clean_prefix = prefix.replace("[*]", "").strip()
        
        # Aligned to match update_status exactly
        content = f"[*] {clean_prefix[:25]:<25} {bar} {percentage:>3}% {self.yellow}{anim}{self.reset}"
        
        # Clear line and print from the left
        sys.stdout.write("\r\033[2K" + content)
        sys.stdout.flush()
        
        if percentage >= 100:
            sys.stdout.write("\n")
            sys.stdout.flush()
        
        # Only print newline when done, so the NEXT status update starts fresh
        if percentage >= 100:
            sys.stdout.write("\n") 
            sys.stdout.flush()

    def select_disk_interactive(self, disks):
        idx = 0
        num_disks = len(disks)
        while True:
            # Re-draw clear
            sys.stdout.write(f"\r{self.yellow}[?] NAVIGATE TO TARGET DEVICE (Arrows + Enter):{self.reset}\n")
            for i, d in enumerate(disks):
                pointer = f"{self.cyan}{self.bold}  >> {self.reset}" if i == idx else "     "
                color = self.bold if i == idx else self.dim
                sys.stdout.write(f"{pointer}{color}[{d['index']}] {d['model'][:30]:<30} | {int(d['size'])/(1024**3):.2f} GB{self.reset}\n")
            
            key = msvcrt.getch()
            if key == b'\r': return disks[idx]['index']
            elif key == b'H' or key == b'w': idx = (idx - 1) % num_disks
            elif key == b'P' or key == b's': idx = (idx + 1) % num_disks
            
            # Move cursor back up to overwrite on next frame
            sys.stdout.write(f"\033[{num_disks + 1}A")

    def draw_warning_header(self, target_idx):
        print(f"\n{self.red}{self.bold}»» TERMINATION PROTOCOL ARMED : DISK {target_idx}{self.reset}")
        print(f"{self.dim}{'-' * 50}{self.reset}")