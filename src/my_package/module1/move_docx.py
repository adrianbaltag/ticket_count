import asyncio
import os
import shutil

from colorama import Back, Fore, Style, init

from src.my_package.module1.nrb_ticket import get_nrb_ticket


async def move_docx(file_name=None):
    """Move a .docx file from Desktop to WORK_IN_PROGRESS folder"""
    init(autoreset=True)

    # If no file_name is passed, get it asynchronously
    if not file_name:
        file_name = await get_nrb_ticket()
        if not file_name:  # If still None, exit
            print(Fore.RED + "No file found to move.")
            return

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    work_in_progress_path = os.path.join(desktop_path, "WORK_IN_PROGRESS")

    # Ensure the WORK_IN_PROGRESS folder exists
    os.makedirs(work_in_progress_path, exist_ok=True)

    file_path = os.path.join(desktop_path, file_name)
    dest_path = os.path.join(work_in_progress_path, file_name)

    try:
        # Check if the file exists before moving
        if os.path.exists(file_path) and file_name.endswith(".docx"):
            await asyncio.to_thread(shutil.move, file_path, dest_path)
            print(Style.BRIGHT + f"Moved: {file_name} → {work_in_progress_path}")
        else:
            print(Fore.RED + f"File '{file_name}' not found on the desktop.")
    except PermissionError:
        print(
            f"{Back.RED}{Fore.WHITE}Permission denied: '{file_name}'. Please close the file and try again."
        )
    except FileNotFoundError:
        print(Fore.RED + f"File '{file_name}' not found.")
    except OSError as e:
        print(Fore.RED + f"Error moving file '{file_name}': {e}")
