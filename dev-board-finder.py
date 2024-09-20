#!/usr/bin/env python3

import argparse
import subprocess
import re
import sys
import time
import platform
import glob
import getpass
from tqdm import tqdm

# Known device families
DEVICE_FAMILIES = {
    "Arduino": ["Arduino"],
    "ESP": ["ESP32", "ESP8266"],
    "Raspberry": ["Raspberry Pi"],
    "FTDI": ["FT232R USB UART"],
    "CH340": ["USB-SERIAL CH340"],
    "CP210x": ["CP210x UART Bridge"]
}

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {e}", file=sys.stderr)
        return ""

def get_device_family(device_info):
    for family, keywords in DEVICE_FAMILIES.items():
        if any(keyword in device_info for keyword in keywords):
            return family
    return "Unknown"

def is_dev_board(device, device_types, os_type):
    if os_type == "Windows":
        # Windows-specific device check
        output = run_command(["wmic", "path", "Win32_PnPEntity", "get", "Caption"])
    elif os_type == "Darwin":  # macOS
        output = run_command(["system_profiler", "SPUSBDataType"])
    else:  # Linux
        output = run_command(["udevadm", "info", "-n", device])
    
    if not device_types:
        return any(board in output for family in DEVICE_FAMILIES.values() for board in family)
    return any(board in output for family in device_types for board in DEVICE_FAMILIES.get(family, []))

def set_permissions(device, os_type):
    if os_type == "Windows":
        print(f"✅ No need to set permissions on Windows for {device}")
        return
    
    with tqdm(total=100, desc=f"🔧 Setting permissions for {device}", bar_format="{l_bar}{bar}", leave=False) as pbar:
        for i in range(5):
            time.sleep(0.1)  # Simulate work
            pbar.update(20)

    if os_type == "Darwin" or os_type == "Linux":
        try:
            # Request sudo password
            password = getpass.getpass("Enter your sudo password: ")

            # Ensure the device path is correct (add '/dev/' if not present)
            if not device.startswith("/dev/"):
                device = f"/dev/{device}"
            
            # Construct the sudo command and pass the password via stdin
            command = f"echo {password} | sudo -S chmod 777 {device}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Permissions set successfully for {device}")
            else:
                print(f"❌ Error setting permissions for {device}: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error executing sudo command: {e}", file=sys.stderr)


def find_devices(device_types, os_type):
    found_devices = []
    
    if os_type == "Windows":
        command = ["wmic", "path", "Win32_PnPEntity", "get", "Caption"]
        all_devices = run_command(command).splitlines()
    elif os_type == "Darwin":  # macOS
        all_devices = glob.glob("/dev/tty.*")  # Use glob to list /dev/tty.*
    else:  # Linux
        all_devices = glob.glob("/dev/tty*")  # Use glob to list /dev/tty*

    with tqdm(total=len(all_devices), desc="🔍 Searching for devices", bar_format="{l_bar}{bar}", leave=False) as pbar:
        for device in all_devices:
            time.sleep(0.1)  # Simulate work
            if is_dev_board(device, device_types, os_type):
                if os_type == "Windows":
                    device_info = device
                    family = get_device_family(device_info)
                    pbar.set_description(f"🎉 Found: {device} ({family})")
                    found_devices.append((device, family, "N/A", "N/A"))
                else:
                    if os_type == "Darwin":
                        device_info = run_command(["system_profiler", "SPUSBDataType"])
                    else:  # Linux
                        device_info = run_command(["udevadm", "info", "-a", "-n", device])
                    family = get_device_family(device_info)
                    pbar.set_description(f"🎉 Found: {device} ({family})")
                    vendor = re.search(r"idVendor.*", device_info, re.MULTILINE)
                    product = re.search(r"idProduct.*", device_info, re.MULTILINE)
                    found_devices.append((device, family, vendor.group() if vendor else "N/A", product.group() if product else "N/A"))
            pbar.update(1)
    
    return found_devices

def main():
    os_type = platform.system()
    
    parser = argparse.ArgumentParser(description="🚀 Find and manage USB devices for development.", add_help=False)
    parser.add_argument("--help", "-h", action="help", help="Show this help message and exit")
    if os_type != "Windows":
        parser.add_argument("--enable-port", "-ep", nargs="?", const="all", help="Enable the port (all devices if not specified)")
    parser.add_argument("--device", "-d", nargs="*", choices=DEVICE_FAMILIES.keys(), help="Filter by device type")
    args = parser.parse_args()

    print("🔍 Searching for USB devices...")
    found_devices = find_devices(args.device, os_type)

    if found_devices:
        print("\n🎉 Devices found:")
        for device, family, vendor, product in found_devices:
            print(f"  📌 {device} - Family: {family}")
            if vendor != "N/A":
                print(f"    📊 {vendor}")
            if product != "N/A":
                print(f"    📊 {product}")
            print("    ---")
    else:
        print("😕 No devices found.")

    if os_type != "Windows" and args.enable_port:
        if args.enable_port == "all":
            print("\n🔧 Enabling all found ports...")
            for device, _, _, _ in found_devices:
                set_permissions(device, os_type)
        else:
            specific_device = next((d for d, _, _, _ in found_devices if args.enable_port in d), None)
            if specific_device:
                print(f"\n🔧 Enabling port {specific_device}...")
                set_permissions(specific_device, os_type)
            else:
                print(f"\n❌ Device {args.enable_port} not found.")

    print("\n🏁 Operation completed!")

if __name__ == "__main__":
    main()