import platform
import psutil
import os
import socket
from datetime import datetime


def format_bytes(value):

    if value < 1024:
        return f"{value} B"

    if value < 1024 ** 2:
        return f"{value / 1024:.2f} KB"

    if value < 1024 ** 3:
        return f"{value / 1024 ** 2:.2f} MB"

    if value < 1024 ** 4:
        return f"{value / 1024 ** 3:.2f} GB"

    return f"{value / 1024 ** 4:.2f} TB"


def show_system_info():

    print("\n" + "=" * 60)
    print("              SYSTEM INFORMATION")
    print("=" * 60)

    # Operating system
    print("\n[ OPERATING SYSTEM ]")

    print(f"OS           : {platform.system()}")
    print(f"Version      : {platform.version()}")
    print(f"Release      : {platform.release()}")
    print(f"Architecture : {platform.machine()}")

    # Computer
    print("\n[ COMPUTER ]")

    print(f"Computer Name: {socket.gethostname()}")
    print(f"Processor    : {platform.processor()}")

    # CPU
    print("\n[ CPU ]")

    print(f"Physical Cores: {psutil.cpu_count(logical=False)}")
    print(f"Logical Cores : {psutil.cpu_count(logical=True)}")
    print(f"CPU Usage     : {psutil.cpu_percent(interval=1)}%")

    # RAM
    print("\n[ MEMORY ]")

    memory = psutil.virtual_memory()

    print(f"Total RAM : {format_bytes(memory.total)}")
    print(f"Used RAM  : {format_bytes(memory.used)}")
    print(f"Free RAM  : {format_bytes(memory.available)}")
    print(f"Usage     : {memory.percent}%")

    # Disk
    print("\n[ DISK ]")

    disk = psutil.disk_usage(os.getcwd())

    print(f"Total : {format_bytes(disk.total)}")
    print(f"Used  : {format_bytes(disk.used)}")
    print(f"Free  : {format_bytes(disk.free)}")
    print(f"Usage : {disk.percent}%")

    # Network
    print("\n[ NETWORK ]")

    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        print(f"Hostname : {hostname}")
        print(f"IP       : {ip}")

    except Exception:
        print("Network information unavailable.")

    # Time
    print("\n[ TIME ]")

    print(
        datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )
    )

    print("\n" + "=" * 60)


def main():

    print("=" * 60)
    print("          PYTHON SYSTEM INFORMATION TOOL")
    print("=" * 60)

    while True:

        command = input(
            "\nPress ENTER to scan your system or type 'exit': "
        ).strip()

        if command.lower() in ["exit", "quit", "q"]:
            print("\nGoodbye!")
            break

        show_system_info()

        print("\nWaiting for next scan...")


if __name__ == "__main__":
    main()