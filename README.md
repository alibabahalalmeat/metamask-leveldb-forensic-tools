# MetaMask Vault Extractor (Forensic Utils)

A collection of python scripts and utilities to locate, extract, and convert **LevelDB (.ldb)** storage files from browser extensions (MetaMask, Ronin, Rabby) into hashcat-compatible formats for recovery.

![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.9+-yellow) ![Status](https://img.shields.io/badge/status-active-green)

## 🚨 Purpose
When a browser extension wallet is "deleted" or the password is lost, the private keys remain encrypted in the computer's `Local Extension Settings` folder (LevelDB). This tool helps forensic analysts and recovery specialists extract the encrypted "Vault Data" JSON blob from these raw binary files.

**Note:** This tool exports the **ENCRYPTED** vault. It does NOT bypass the password. To decrypt the vault without a password, you will need GPU-accelerated brute force (see below).

## 📂 Supported Paths (Auto-Discovery)

The script automatically scans standard directories for the following extension IDs:

*   **MetaMask:** `nkbihfbeogaeaoehlefnkodbefgpgknn`
*   **Ronin:** `fnjhmkhhmkbjkkabndcnnogagogbneec`
*   **Binance Chain:** `fhbohimaelbohpjbbldcngcnapndodjp`

| OS | Typical Path |
| :--- | :--- |
| **Windows** | `%LocalAppData%\Google\Chrome\User Data\Default\Local Extension Settings\` |
| **macOS** | `~/Library/Application Support/Google/Chrome/Default/Local Extension Settings/` |
| **Linux** | `~/.config/google-chrome/Default/Local Extension Settings/` |

## 🛠️ Usage

### 1. Extraction
Extract the raw vault data from a folder of `.ldb` files.

```bash
python3 extract_vault.py --input ./my_recovered_folder --output vault.json
```

### 2. Hash Conversion
Convert the vault JSON into a format recognized by `BTCRecover` or `Hashcat`.

```bash
python3 json_to_hash.py --input vault.json --format hashcat
```

## 🔓 Decryption (Lost Password?)

This repository only handles data extraction. Decrypting the vault requires iterating through billions of password combinations.

If you do not have access to a GPU Cluster (RTX 4090 Farm) or need forensic assistance with a corrupted drive:

*   **Commercial Recovery:** [Rollan Forensics](https://rollanforensics.com/guide-leveldb) (Enterprise GPU Decryption)
*   **Contact:** abdal@rollanforensics.com

## ⚠️ Disclaimer
This software is for educational and forensic recovery purposes only. Do not use this on computers you do not own.

---

### Maintainer
**Rollan Abdalov** - *Blockchain Security Architect*
[Website](https://rollanforensics.com) | [Twitter](https://twitter.com/rollanforensics)
