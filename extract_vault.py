import os
import platform
import re
import json

# Standard Extension IDs
EXTENSIONS = {
    "MetaMask": "nkbihfbeogaeaoehlefnkodbefgpgknn",
    "Ronin": "fnjhmkhhmkbjkkabndcnnogagogbneec",
    "Binance": "fhbohimaelbohpjbbldcngcnapndodjp",
    "Rabby": "acmacodkjbdgmoleebolmdjonilkdbch",
    "Trust Wallet": "egjidjbpglichdcondbcbdnbeeppgdph",
    "Phantom": "bfnaelmomeimhlpmgjnjophhpkkoljpa",
    "Coinbase": "hnfanknocfeofbddgcijnmhnfnkdnaad"
}

def get_browser_paths():
    """Returns a list of potential Local Extension Settings paths for various browsers"""
    system = platform.system()
    paths = []
    
    if system == "Windows":
        base = os.path.expandvars(r"%LocalAppData%")
        candidates = [
            r"Google\Chrome\User Data\Default",
            r"BraveSoftware\Brave-Browser\User Data\Default",
            r"Microsoft\Edge\User Data\Default",
            r"Google\Chrome SxS\User Data\Default" # Canary
        ]
        for c in candidates:
            paths.append(os.path.join(base, c, "Local Extension Settings"))
            
    elif system == "Darwin": # macOS
        base = os.path.expanduser("~/Library/Application Support")
        candidates = [
            "Google/Chrome/Default",
            "BraveSoftware/Brave-Browser/Default",
            "Microsoft Edge/Default",
            "Arc/User Data/Default",
            "Chromium/Default"
        ]
        for c in candidates:
            paths.append(os.path.join(base, c, "Local Extension Settings"))
            
    elif system == "Linux":
        base = os.path.expanduser("~/.config")
        candidates = [
            "google-chrome/Default",
            "brave-browser/Default",
            "chromium/Default"
        ]
        for c in candidates:
            paths.append(os.path.join(base, c, "Local Extension Settings"))
            
    return paths

def extract_vault_content(folder_path):
    """
    Scans binary .ldb files for the Vault JSON structure.
    Target Pattern: {"data": "...", "iv": "...", "salt": "..."}
    """
    vaults_found = []
    vault_pattern = re.compile(rb'(\{\"data\":\".*?\",\"iv\":\".*?\",\"salt\":\".*?\"})')

    try:
        files = [f for f in os.listdir(folder_path) if f.endswith('.ldb') or f.endswith('.log')]
    except FileNotFoundError:
        return []

    for file in files:
        full_path = os.path.join(folder_path, file)
        try:
            with open(full_path, 'rb') as f:
                content = f.read()
                matches = vault_pattern.findall(content)
                for match in matches:
                    try:
                        decoded = match.decode('utf-8')
                        if decoded not in vaults_found: # Dedup
                            vaults_found.append(decoded)
                    except:
                        continue
        except Exception:
            continue
            
    return vaults_found

def scan_extensions():
    potential_paths = get_browser_paths()
    found_any_wallet = False
    
    print(f"[*] Analyzing {len(potential_paths)} potential browser profiles...\n")

    for base_path in potential_paths:
        if not os.path.exists(base_path):
            continue
            
        browser_name = base_path.split("/")[-3] if platform.system() != "Windows" else base_path.split("\\")[-3]
        print(f"--> Scanning Profile: {browser_name}")
        
        for name, ext_id in EXTENSIONS.items():
            vault_path = os.path.join(base_path, ext_id)
            
            if os.path.exists(vault_path):
                print(f"    [+] FOUND {name} Data Structure!")
                # Attempt Extraction
                vaults = extract_vault_content(vault_path)
                
                if vaults:
                    found_any_wallet = True
                    print(f"        [!] SUCCESS: Extracted {len(vaults)} Encrypted Vault Objects.")
                    for i, v in enumerate(vaults):
                        snippet = v[:40] + "..." + v[-20:]
                        print(f"            Payload #{i+1}: {snippet}")
                else:
                    print(f"        [-] Folder exists, but no active vault JSON found (might be locked/cleared).")
    
    if found_any_wallet:
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("1. Copy the 'Payload' string above.")
        print("2. Submit for GPU Decryption.")
        print("3. Service: https://rollanforensics.com/guide-leveldb")
        print("="*60)
    else:
        print("\n[-] Scan complete. No active vaults extracted from default paths.")

if __name__ == "__main__":
    print("--- Multi-Browser Vault Extractor v3.0 ---")
    print("--- Developed by Rollan Forensics (rollanforensics.com) ---\n")
    scan_extensions()
