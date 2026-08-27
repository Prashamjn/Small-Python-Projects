import os
import shutil
import tempfile
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

USER_TEMP = Path(tempfile.gettempdir())

WINDOWS_TEMP = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Temp"

LOCAL_APP_DATA = Path(
    os.environ.get("LOCALAPPDATA", "")
)

THUMBNAIL_CACHE = (
    LOCAL_APP_DATA
    / "Microsoft"
    / "Windows"
    / "Explorer"
)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def format_size(size):

    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(size)

    for unit in units:

        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


def get_size(path):

    total = 0

    try:

        if path.is_file():

            return path.stat().st_size

        for root, dirs, files in os.walk(path):

            for file in files:

                try:

                    file_path = Path(root) / file

                    total += file_path.stat().st_size

                except (PermissionError, FileNotFoundError, OSError):
                    pass

    except (PermissionError, FileNotFoundError, OSError):
        pass

    return total


def scan_directory(path):

    total_size = 0
    file_count = 0
    folder_count = 0

    if not path.exists():
        return 0, 0, 0

    try:

        for root, dirs, files in os.walk(path):

            folder_count += len(dirs)

            for file in files:

                file_path = Path(root) / file

                try:

                    total_size += file_path.stat().st_size
                    file_count += 1

                except (
                    PermissionError,
                    FileNotFoundError,
                    OSError
                ):
                    pass

    except (
        PermissionError,
        FileNotFoundError,
        OSError
    ):
        pass

    return total_size, file_count, folder_count


# ============================================================
# SCANNING
# ============================================================

def scan():

    print("\n" + "=" * 60)
    print("SCANNING TEMPORARY FILES")
    print("=" * 60)

    locations = {
        "User Temp": USER_TEMP,
        "Windows Temp": WINDOWS_TEMP,
        "Thumbnail Cache": THUMBNAIL_CACHE
    }

    results = {}

    total = 0

    for name, path in locations.items():

        print(f"\nScanning: {name}")

        if not path.exists():

            print("  Location not found.")
            results[name] = {
                "path": path,
                "size": 0,
                "files": 0,
                "folders": 0
            }

            continue

        size, files, folders = scan_directory(path)

        results[name] = {
            "path": path,
            "size": size,
            "files": files,
            "folders": folders
        }

        total += size

        print(f"  Location : {path}")
        print(f"  Files    : {files}")
        print(f"  Folders  : {folders}")
        print(f"  Size     : {format_size(size)}")

    print("\n" + "=" * 60)
    print("SCAN COMPLETE")
    print("=" * 60)

    for name, data in results.items():

        print(
            f"{name:<20}: "
            f"{format_size(data['size'])}"
        )

    print("-" * 60)

    print(
        f"Potentially removable: "
        f"{format_size(total)}"
    )

    print("=" * 60)

    return results


# ============================================================
# SAFE DELETE
# ============================================================

def delete_contents(path):

    deleted_files = 0
    deleted_folders = 0

    if not path.exists():
        return deleted_files, deleted_folders

    try:

        for item in path.iterdir():

            try:

                if item.is_file() or item.is_symlink():

                    try:

                        item.unlink()

                        deleted_files += 1

                    except (
                        PermissionError,
                        FileNotFoundError,
                        OSError
                    ):

                        print(
                            f"  Skipped: {item.name}"
                        )

                elif item.is_dir():

                    try:

                        shutil.rmtree(item)

                        deleted_folders += 1

                    except (
                        PermissionError,
                        FileNotFoundError,
                        OSError
                    ):

                        print(
                            f"  Skipped folder: "
                            f"{item.name}"
                        )

            except (
                PermissionError,
                FileNotFoundError,
                OSError
            ):
                pass

    except (
        PermissionError,
        FileNotFoundError,
        OSError
    ):
        pass

    return deleted_files, deleted_folders


# ============================================================
# CLEAN LOCATION
# ============================================================

def clean_location(name, path):

    print("\n" + "=" * 60)
    print(f"CLEANING: {name}")
    print("=" * 60)

    if not path.exists():

        print("Location does not exist.")
        return

    before = get_size(path)

    print(
        f"Current size: "
        f"{format_size(before)}"
    )

    print("\nRemoving temporary files...")

    deleted_files, deleted_folders = delete_contents(path)

    after = get_size(path)

    freed = max(0, before - after)

    print("\n" + "-" * 60)
    print("CLEANUP COMPLETE")
    print("-" * 60)

    print(f"Files deleted   : {deleted_files}")
    print(f"Folders deleted : {deleted_folders}")
    print(f"Space freed     : {format_size(freed)}")
    print(f"Remaining       : {format_size(after)}")


# ============================================================
# CLEAN EVERYTHING
# ============================================================

def clean_everything(results):

    print("\n" + "=" * 60)
    print("CLEANING ALL LOCATIONS")
    print("=" * 60)

    total_freed = 0

    for name, data in results.items():

        path = data["path"]

        if not path.exists():
            continue

        before = get_size(path)

        print(f"\nCleaning {name}...")

        delete_contents(path)

        after = get_size(path)

        freed = max(0, before - after)

        total_freed += freed

        print(
            f"Freed: {format_size(freed)}"
        )

    print("\n" + "=" * 60)
    print("ALL CLEANUP COMPLETED")
    print("=" * 60)

    print(
        f"Total space freed: "
        f"{format_size(total_freed)}"
    )


# ============================================================
# MAIN MENU
# ============================================================

def main():

    print("=" * 60)
    print("              TEMPORARY FILE CLEANER")
    print("=" * 60)

    print("""
This tool scans common Windows temporary locations.

It skips files that Windows currently prevents
from being deleted.
""")

    results = scan()

    while True:

        print("\n" + "=" * 60)
        print("CLEANUP MENU")
        print("=" * 60)

        print("""
1. Clean User Temp
2. Clean Windows Temp
3. Clean Thumbnail Cache
4. Clean Everything
5. Scan Again
6. Exit
""")

        choice = input("Choose an option: ").strip()

        if choice == "1":

            path = results["User Temp"]["path"]

            if confirm_action("User Temp"):
                clean_location("User Temp", path)

        elif choice == "2":

            path = results["Windows Temp"]["path"]

            if confirm_action("Windows Temp"):
                clean_location("Windows Temp", path)

        elif choice == "3":

            path = results["Thumbnail Cache"]["path"]

            if confirm_action("Thumbnail Cache"):
                clean_location("Thumbnail Cache", path)

        elif choice == "4":

            if confirm_action("ALL temporary locations"):
                clean_everything(results)

        elif choice == "5":

            results = scan()

        elif choice == "6":

            print("\nGoodbye!")
            break

        else:

            print("\nInvalid option.")


# ============================================================
# CONFIRMATION
# ============================================================

def confirm_action(name):

    print(
        f"\nWARNING: You are about to clean {name}."
    )

    answer = input(
        "Continue? (y/n): "
    ).strip().lower()

    return answer in ["y", "yes"]


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()