# macchanger_pro 🛡️

**A safe, production‑style MAC address manager for Linux**

`macchanger_pro` is a professional, security‑focused Python utility that lets you **view, change, randomize, back up, and restore MAC addresses** on Linux systems — safely, predictably, and transparently.

This project is built for **learning, privacy testing, wireless security labs, and authorized system administration**. It follows modern Linux networking practices and avoids fragile or unsafe shortcuts.

---

## Tested example:

```
┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ chmod +x macchanger_pro.py

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ sudo python3 macchanger_pro.py --list
Interfaces and MACs:
  eth0: 00:17:5d:39:2b:3b

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ sudo python3 macchanger_pro.py --interface eth0 --show
eth0 current MAC: 00:17:5d:39:2b:3b

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ sudo python3 macchanger_pro.py -i eth0 --set aa:bb:cc:dd:ee:ff
Apply MAC aa:bb:cc:dd:ee:ff to interface eth0? [y/N]: y
2026-01-28 13:18:34,425 [INFO] Setting MAC for eth0 -> aa:bb:cc:dd:ee:ff
MAC successfully changed for eth0. New MAC: aa:bb:cc:dd:ee:ff
2026-01-28 13:18:34,444 [INFO] Operation completed.

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ sudo python3 macchanger_pro.py --interface eth0 --show
eth0 current MAC: aa:bb:cc:dd:ee:ff

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ sudo python3 macchanger_pro.py -i eth0 --random
Apply MAC 8a:12:2e:76:8a:36 to interface eth0? [y/N]: y
2026-01-28 13:19:00,269 [INFO] Setting MAC for eth0 -> 8a:12:2e:76:8a:36
MAC successfully changed for eth0. New MAC: 8a:12:2e:76:8a:36
2026-01-28 13:19:00,289 [INFO] Operation completed.

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ sudo python3 macchanger_pro.py --interface eth0 --show
eth0 current MAC: 8a:12:2e:76:8a:36

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ sudo python3 macchanger_pro.py -i eth0 --restore
Restore original MAC for eth0? [y/N]: y
2026-01-28 13:19:17,765 [INFO] Restoring MAC for eth0 -> 00:17:5d:39:2b:3b
Restored original MAC for eth0. Current: 00:17:5d:39:2b:3b

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ sudo python3 macchanger_pro.py --interface eth0 --show
eth0 current MAC: 00:17:5d:39:2b:3b

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ sudo python3 macchanger_pro.py -i eth0 -r -y
2026-01-28 13:19:46,170 [INFO] Setting MAC for eth0 -> 8a:7e:11:78:6c:a4
MAC successfully changed for eth0. New MAC: 8a:7e:11:78:6c:a4
2026-01-28 13:19:46,187 [INFO] Operation completed.

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ sudo python3 macchanger_pro.py -i eth0
Selected interface: eth0 (current MAC: 8a:7e:11:78:6c:a4)
Enter new MAC (or 'random' to generate, 'restore' to restore original): --show
2026-01-28 13:21:04,283 [ERROR] Invalid MAC format: --show

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ sudo python3 macchanger_pro.py -i eth0
Selected interface: eth0 (current MAC: 8a:7e:11:78:6c:a4)
Enter new MAC (or 'random' to generate, 'restore' to restore original): restore
2026-01-28 13:21:21,594 [INFO] Restoring MAC for eth0 -> 00:17:5d:39:2b:3b
Restored original MAC for eth0. Current: 00:17:5d:39:2b:3b

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ cat /var/lib/macchanger/eth0.orig
cat: /var/lib/macchanger/eth0.orig: Permission denied

┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/GitHub Clone/MAC-Address_Changer_Script]
└─$ sudo cat /var/lib/macchanger/eth0.orig
00:17:5d:39:2b:3b
```

## 🚀 Why This Project Exists

Many MAC‑changing scripts online are:

- hardcoded to `wlan0`
- dependent on deprecated tools only
- unsafe (no backup, no validation)
- unclear about what they actually do

**`macchanger_pro` fixes all of that.**

It behaves like a **real system utility**, not a throwaway script.

---

## ✨ Key Features (At a Glance)

- ✅ Dynamic interface detection (no hardcoding)
- ✅ Uses modern `ip` (iproute2) commands
- ✅ Automatic backup of original MAC addresses
- ✅ Safe restore mechanism
- ✅ Locally‑administered & unicast random MAC generator
- ✅ Strict MAC address validation
- ✅ CLI + interactive fallback
- ✅ Root‑only enforcement
- ✅ Clear logging and error handling
- ✅ Designed for learning & authorized testing

---

## 🧠 What You Can Do With It

- Inspect MAC addresses of your network interfaces
- Change an interface MAC to a **specific value**
- Generate and apply a **standards‑correct random MAC**
- Restore the **original factory MAC**
- Learn **how professional Linux networking tools are built**
- Use it safely in **cybersecurity labs & coursework**

---

## 📦 Requirements

### System

- Linux (tested on Kali/Ubuntu/Debian‑based systems)
- Root privileges (`sudo`)

### Software

- Python **3.8+**
- `ip` command (from `iproute2`) — typically installed by default

Optional fallback (legacy systems only):

- `ifconfig`

---

## 🛠 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/macchanger_pro.git
cd macchanger_pro
```

Make the script executable (optional but convenient):

```bash
chmod +x macchanger_pro.py
```

---

## 📖 Usage Guide

> The main script is [macchanger_pro.py](macchanger_pro.py). You can run it directly with `python3`.

### 1️⃣ List Available Network Interfaces

```bash
sudo python3 macchanger_pro.py --list
```

Example output:

```
Interfaces and MACs:
	wlan0: 00:11:22:33:44:55
	eth0: 3c:52:82:aa:bb:cc
```

---

### 2️⃣ Show Current MAC Address

```bash
sudo python3 macchanger_pro.py --interface eth0 --show
```

---

### 3️⃣ Set a Custom MAC Address

```bash
sudo python3 macchanger_pro.py -i eth0 --set aa:bb:cc:dd:ee:ff
```

✔ Format is strictly validated
✔ Original MAC is backed up automatically

---

### 4️⃣ Apply a Random MAC Address (Recommended)

```bash
sudo python3 macchanger_pro.py -i eth0 --random
```

The generated MAC is:

- **Locally‑administered**
- **Unicast**
- Standards‑compliant

This avoids vendor conflicts and network issues.

---

### 5️⃣ Restore the Original MAC Address

```bash
sudo python3 macchanger_pro.py -i eth0 --restore
```

✔ Restores the backed‑up hardware MAC
✔ No guessing or hardcoding

---

### 6️⃣ Non‑Interactive Mode (Automation)

```bash
sudo python3 macchanger_pro.py -i eth0 -r -y
```

Perfect for:

- scripts
- labs
- CI environments

---

### 7️⃣ Interactive Mode (If You Skip Flags)

If you run the tool without `--set`, `--random`, or `--restore`, it will guide you:

```bash
sudo python3 macchanger_pro.py -i eth0
```

You’ll be prompted to enter a MAC, type `random`, or type `restore`.

---

## 💾 How Backup & Restore Works

Original MAC addresses are saved **once**, on first change.

Location:

```
/var/lib/macchanger/<interface>.orig
```

Example:

```
/var/lib/macchanger/eth0.orig
```

Security:

- Owner: `root`
- File permissions: `600`
- Directory permissions: `700`

This ensures:

- ✔ Safety
- ✔ Reversibility
- ✔ No accidental overwrites

---

## 🧪 How Random MACs Are Generated

This tool **does not generate unsafe MACs**.

It enforces:

- **Locally‑Administered Address (LAA)** bit set
- **Unicast** bit set correctly

This is the same standard used by:

- NetworkManager
- Professional pentesting tools
- Privacy‑focused systems

---

## ⚠️ Important Notes (Read This)

- Network managers (NetworkManager, systemd‑networkd) may **override MAC changes**
- If the MAC reverts:
  - disconnect/reconnect the interface
  - or temporarily stop the network manager
- MAC changes are **temporary by design**
- Persistence across reboots is intentionally **not automatic**

---

## 🔍 How It Works (Internals in Plain English)

1. **Root check**: exits if not run with `sudo`
2. **Interface detection**: reads `/sys/class/net` (fallback: `ip -o link show`)
3. **Backup**: saves original MAC on first change
4. **Change**: uses `ip link set` (fallback: `ifconfig` if needed)
5. **Restore**: reads the stored backup and re‑applies it

Every step is logged with clear messages so you can see exactly what happened.

---

## ⚖️ Legal & Ethical Disclaimer

This tool is provided **for educational and authorized use only**.

You **must**:

- own the device **or**
- have explicit permission to modify the network interface

Unauthorized MAC spoofing may violate:

- local laws
- network policies
- institutional rules

**You are responsible for how you use this tool.**

---

## 🎓 Learning Value

This project demonstrates:

- real Linux networking workflows
- secure system scripting
- defensive programming
- proper CLI tool design
- cybersecurity‑oriented thinking

It is **portfolio‑ready** and **interview‑safe** when explained correctly.

---

## 🧾 Project Status

- ✅ Stable
- ✅ Actively usable
- ✅ Designed for extension

Possible future enhancements:

- NetworkManager persistence support
- systemd service integration
- Unit tests
- Packaging as a pip module

---

## 📂 Project Structure

- [macchanger_pro.py](macchanger_pro.py) — the complete MAC management tool
- [README.md](README.md) — full documentation (this file)

---

## 👤 Author

**Sagar Biswas**
Cybersecurity & Computer Science Enthusiast

> Built to learn how real security tools should behave — not just how to make them work.

---

## ⭐ Final Note

If you understand this README,
you understand **the entire project**.

That’s intentional.
