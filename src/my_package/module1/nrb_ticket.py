import asyncio
import os

from colorama import Fore, Style, init


async def get_nrb_ticket():
    """Get the first NRB .docx file on the Desktop"""
    init(autoreset=True)

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    max_attempts = 5
    delay = 1  # Start with 1 second delay

    for attempt in range(1, max_attempts + 1):
        # List NRB .docx files on Desktop
        docx_files = [
            f
            for f in os.listdir(desktop_path)
            if f.startswith("NRB") and f.endswith(".docx")
        ]

        if docx_files:
            return docx_files[0]  # Return the first found file

        print(
            Fore.CYAN
            + f"Attempt {attempt}: No NRB .docx found. Retrying in {delay}s..."
        )
        await asyncio.sleep(delay)
        delay = min(delay * 1, 5)  # Exponential backoff (capped at 5s)

    print(Style.BRIGHT + "No NRB .docx file found after 10 attempts. Exiting.")
    return None  # Return None if no file found
