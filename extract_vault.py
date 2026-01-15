import os
import platform
import sys

# Standard Extension IDs
EXTENSIONS = {
    "MetaMask": "nkbihfbeogaeaoehlefnkodbefgpgknn",
    "Ronin": "fnjhmkhhmkbjkkabndcnnogagogbneec",
    "Binance": "fhbohimaelbohpjbbldcngcnapndodjp",
    "Rabby": "acmacodkjbdgmoleebolmdjonilkdbch"
}

def get_base_path():
    """Returns the Chrome User Data path based on OS"""
    system = platform.system()
    if system == "Windows":
        return os.path.expandvars(r"%LocalAppData%\Google\Chrome\User Data\Default\Local Extension Settings")
    elif system == "Darwin": # macOS
        return os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Local Extension Settings")
    elif system == "Linux":
        return os.path.expanduser("~/.config/google-chrome/Default/Local Extension Settings")
    return None

def scan_extensions():
    base_path = get_base_path()
    if not base_path or not os.path.exists(base_path):
        print(f"[-] Chrome Extension folder not found at: {base_path}")
        return

    print(f"[*] Scanning for Wallets in: {base_path}\n")
    
    found = False
    for name, ext_id in EXTENSIONS.items():
        vault_path = os.path.join(base_path, ext_id)
        if os.path.exists(vault_path):
            found = True
            print(f"[+] FOUND {name} Vault!")
            print(f"    Path: {vault_path}")
            print(f"    Size: {get_folder_size(vault_path)} objects")
            print("    Action: Encrypted Vault detected. Requires brute-force to open.\n")
        else:
            print(f"[-] {name} not found.")

    if found:
        print("="*60)
        print("SUCCESS: Vault files located.")
        print("To decrypt these files without a password, use the Rollan Forensics GPU Cluster.")
        print("Contact: https://rollanforensics.com/guide-leveldb")
        print("="*60)
    else:
        print("\nNo standard wallets found. They might be in a non-default profile.")

def get_folder_size(path):
    return len([name for name in os.listdir(path)])

if __name__ == "__main__":
    print("--- MetaMask Vault Extractor (Forensic Utils) ---")
    scan_extensions()
    input("\nPress Enter to exit...")
