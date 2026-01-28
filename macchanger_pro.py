#!/usr/bin/env python3
"""
macchanger_pro.py — A production-quality MAC address tool

Features:
- List network interfaces and current MACs
- Set a specific MAC address
- Generate a locally-administered random MAC
- Backup original MAC and restore it later
- Uses `ip` (iproute2) when available
- Saves backups at /var/lib/macchanger/<iface>.orig
- Argument-based CLI with interactive fallback

Author: Produced for Sagar (educational / authorized testing only)
"""

from __future__ import annotations
import argparse
import logging
import os
import random
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

# ---- Configuration ----
BACKUP_DIR = Path("/var/lib/macchanger")
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
MAC_REGEX = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")

# ---- Logging ----
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("macchanger_pro")


# ---- Utilities ----
def require_root() -> None:
    """Abort if not run as root."""
    if os.geteuid() != 0:
        logger.error("This tool requires root privileges. Re-run with sudo.")
        sys.exit(2)


def check_dependency(cmd: str) -> bool:
    """Return True if command exists in PATH."""
    return shutil.which(cmd) is not None


def run_cmd(args: List[str]) -> subprocess.CompletedProcess:
    """Run a command and raise on error (captures stdout/stderr)."""
    logger.debug("Running command: %s", " ".join(args))
    return subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


# ---- MAC helpers ----
def validate_mac(mac: str) -> bool:
    """Return True if mac is in canonical 6-octet hex format (AA:BB:CC:DD:EE:FF)."""
    return bool(MAC_REGEX.match(mac.strip()))


def normalize_mac(mac: str) -> str:
    """Normalize input to lowercase, canonical format."""
    return mac.strip().lower()


def generate_locally_administered_unicast_mac() -> str:
    """
    Generate a locally-administered unicast MAC address:
    - locally-administered bit (bit 1 of first octet) = 1
    - multicast bit (bit 0 of first octet) = 0
    """
    first_octet = random.randint(0, 255)
    # Clear the two least significant bits, then set LAA bit (0b10)
    first_octet = (first_octet & 0b11111100) | 0b00000010
    octets = [first_octet] + [random.randint(0, 255) for _ in range(5)]
    return ":".join(f"{octet:02x}" for octet in octets)


# ---- Interface helpers ----
def list_interfaces() -> List[str]:
    """Return list of network interfaces from /sys/class/net (excluding loopback)."""
    net_path = Path("/sys/class/net")
    if not net_path.exists():
        # Fallback: parse `ip -o link show`
        try:
            out = run_cmd(["ip", "-o", "link", "show"]).stdout
            names = []
            for line in out.splitlines():
                # lines like: "1: lo: <...>"
                parts = line.split(":")
                if len(parts) >= 2:
                    name = parts[1].strip()
                    if name and name != "lo":
                        names.append(name)
            return names
        except Exception:
            return []
    return [p.name for p in net_path.iterdir() if p.is_dir() and p.name != "lo"]


def get_interface_mac(interface: str) -> Optional[str]:
    """Read the current MAC address for an interface from sysfs."""
    addr_file = Path(f"/sys/class/net/{interface}/address")
    try:
        return addr_file.read_text().strip().lower()
    except Exception:
        return None


# ---- Backup / Restore ----
def ensure_backup_dir() -> None:
    """Create backup dir with secure permissions (root only)."""
    try:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        # Set permissions to 0700
        BACKUP_DIR.chmod(0o700)
    except PermissionError:
        logger.error("Unable to create or chmod backup directory %s", BACKUP_DIR)
        sys.exit(3)


def backup_original_mac(interface: str) -> None:
    """Store the current MAC for an interface if not already backed up."""
    ensure_backup_dir()
    current = get_interface_mac(interface)
    if not current:
        logger.error("Cannot read current MAC for interface %s", interface)
        raise RuntimeError("Could not read current MAC address")
    backup_file = BACKUP_DIR / f"{interface}.orig"
    if backup_file.exists():
        logger.debug("Backup for %s already exists at %s", interface, backup_file)
        return
    backup_file.write_text(current + "\n")
    # Make backup root-only readable
    backup_file.chmod(0o600)
    logger.info("Saved original MAC for %s to %s", interface, backup_file)


def read_backup(interface: str) -> Optional[str]:
    """Return the backed-up MAC for an interface, or None."""
    backup_file = BACKUP_DIR / f"{interface}.orig"
    if backup_file.exists():
        return backup_file.read_text().strip().lower()
    return None


# ---- Core operations ----
def ip_set_mac(interface: str, new_mac: str) -> None:
    """Use `ip` to set MAC address (down -> set -> up)."""
    run_cmd(["ip", "link", "set", "dev", interface, "down"])
    run_cmd(["ip", "link", "set", "dev", interface, "address", new_mac])
    run_cmd(["ip", "link", "set", "dev", interface, "up"])


def ifconfig_set_mac(interface: str, new_mac: str) -> None:
    """Fallback to ifconfig if ip is not present (legacy systems)."""
    run_cmd(["ifconfig", interface, "down"])
    # 3rd-party tools sometimes required; try builtin change:
    run_cmd(["ifconfig", interface, "hw", "ether", new_mac])
    run_cmd(["ifconfig", interface, "up"])


def set_mac(interface: str, new_mac: str) -> None:
    """Set MAC using the best available method."""
    if not validate_mac(new_mac):
        raise ValueError("Invalid MAC address format")
    logger.info("Setting MAC for %s -> %s", interface, new_mac)
    # Backup before changing
    backup_original_mac(interface)
    try:
        if check_dependency("ip"):
            ip_set_mac(interface, new_mac)
        elif check_dependency("ifconfig"):
            ifconfig_set_mac(interface, new_mac)
        else:
            logger.error("No suitable tool found (need 'ip' or 'ifconfig'). Install iproute2.")
            raise RuntimeError("Missing network command")
    except subprocess.CalledProcessError as e:
        logger.error("Command failed: %s", e)
        raise


def restore_mac(interface: str) -> None:
    """Restore backed-up original MAC for an interface."""
    orig = read_backup(interface)
    if not orig:
        logger.error("No backup found for interface %s at %s", interface, BACKUP_DIR)
        raise RuntimeError("No backup found")
    logger.info("Restoring MAC for %s -> %s", interface, orig)
    try:
        if check_dependency("ip"):
            ip_set_mac(interface, orig)
        elif check_dependency("ifconfig"):
            ifconfig_set_mac(interface, orig)
        else:
            raise RuntimeError("Missing network command")
    except subprocess.CalledProcessError as e:
        logger.error("Restore command failed: %s", e)
        raise


# ---- CLI ----
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="macchanger_pro: safe, production-ready MAC tool")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--set", "-s", metavar="MAC", help="Set the MAC address to MAC (format: aa:bb:cc:dd:ee:ff)")
    group.add_argument("--random", "-r", action="store_true", help="Set a locally-administered random MAC")
    group.add_argument("--restore", "-R", action="store_true", help="Restore previously backed-up original MAC")
    parser.add_argument("--interface", "-i", metavar="IFACE", help="Network interface (e.g. wlan0). If omitted, prompt or show list.")
    parser.add_argument("--list", "-l", action="store_true", help="List non-loopback interfaces and current MACs")
    parser.add_argument("--show", action="store_true", help="Show current MAC for the selected interface")
    parser.add_argument("--yes", "-y", action="store_true", help="Automatic yes to prompts")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()


def choose_interface(cli_iface: Optional[str]) -> str:
    """Return a chosen interface, either from CLI or interactively."""
    if cli_iface:
        if cli_iface not in list_interfaces():
            logger.error("Interface %s not found. Available: %s", cli_iface, ", ".join(list_interfaces()))
            sys.exit(4)
        return cli_iface
    interfaces = list_interfaces()
    if not interfaces:
        logger.error("No network interfaces found.")
        sys.exit(5)
    # If only one non-loopback interface, pick it
    if len(interfaces) == 1:
        return interfaces[0]
    # Else ask user to pick
    print("Available interfaces:")
    for idx, iface in enumerate(interfaces, start=1):
        mac = get_interface_mac(iface) or "unknown"
        print(f"  {idx}. {iface}  (MAC: {mac})")
    while True:
        try:
            choice = input("Select interface by number: ").strip()
            idx = int(choice)
            if 1 <= idx <= len(interfaces):
                return interfaces[idx - 1]
        except (ValueError, EOFError):
            pass
        print("Invalid selection. Try again.")


def main() -> None:
    args = parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    require_root()

    # Quick list display
    if args.list:
        ifaces = list_interfaces()
        if not ifaces:
            print("No non-loopback interfaces found.")
            return
        print("Interfaces and MACs:")
        for iface in ifaces:
            print(f"  {iface}: {get_interface_mac(iface) or 'unknown'}")
        return

    # Choose interface
    iface = choose_interface(args.interface)

    # Show current MAC if requested
    if args.show:
        mac = get_interface_mac(iface)
        print(f"{iface} current MAC: {mac or 'unknown'}")
        return

    # Handle restore
    if args.restore:
        if not args.yes:
            confirm = input(f"Restore original MAC for {iface}? [y/N]: ").strip().lower()
            if confirm not in ("y", "yes"):
                print("Aborted.")
                return
        try:
            restore_mac(iface)
            print(f"Restored original MAC for {iface}. Current: {get_interface_mac(iface)}")
        except Exception as e:
            logger.error("Failed to restore MAC: %s", e)
            sys.exit(6)
        return

    # Handle set/random
    if args.random:
        new_mac = generate_locally_administered_unicast_mac()
    elif args.set:
        if not validate_mac(args.set):
            logger.error("Invalid MAC format: %s", args.set)
            sys.exit(7)
        new_mac = normalize_mac(args.set)
    else:
        # Interactive prompt if nothing given
        print(f"Selected interface: {iface} (current MAC: {get_interface_mac(iface)})")
        choice = input("Enter new MAC (or 'random' to generate, 'restore' to restore original): ").strip().lower()
        if choice == "random":
            new_mac = generate_locally_administered_unicast_mac()
        elif choice == "restore":
            # Forward to restore path
            try:
                restore_mac(iface)
                print(f"Restored original MAC for {iface}. Current: {get_interface_mac(iface)}")
                return
            except Exception as e:
                logger.error("Restore failed: %s", e)
                sys.exit(6)
        else:
            if not validate_mac(choice):
                logger.error("Invalid MAC format: %s", choice)
                sys.exit(7)
            new_mac = normalize_mac(choice)

    # Confirm unless automatic
    if not args.yes:
        confirm = input(f"Apply MAC {new_mac} to interface {iface}? [y/N]: ").strip().lower()
        if confirm not in ("y", "yes"):
            print("Aborted.")
            return

    # Apply change
    try:
        set_mac(iface, new_mac)
        print(f"MAC successfully changed for {iface}. New MAC: {get_interface_mac(iface)}")
        logger.info("Operation completed.")
    except Exception as e:
        logger.error("Failed to change MAC: %s", e)
        sys.exit(8)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted by user. Exiting.")
        sys.exit(1)
